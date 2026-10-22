import time
import uuid
from typing import Dict, Any, Optional
from src.context_auditor.models import (
    AuditInput,
    AuditResult,
    AuditScope,
    DimensionScores,
    Finding,
    RecommendedAction,
    GateRoute,
    L1GateVerdict,
    EpistemicStatus,
)
from src.context_auditor.normalizers import normalize_input
from src.context_auditor.signals import extract_deterministic_signals
from src.context_auditor.scoring import (
    compute_irc,
    compute_l1_gate,
    synthesize_l1_dimension_scores,
    load_scoring_config,
)
from src.context_auditor.policies import PolicyEngine, PolicyMode
from src.context_auditor.adapters.base import BaseLLMAdapter
from src.context_auditor.validators import validate_result


class ContextAuditor:
    def __init__(self, llm_adapter: BaseLLMAdapter, policy_mode: PolicyMode = PolicyMode.RECOMMEND):
        self.llm_adapter = llm_adapter
        self.policy_engine = PolicyEngine(mode=policy_mode)

    def audit(
        self,
        raw_input: Dict[str, Any],
        task_requires_factual: bool = False,
        fast_gate_only: bool = False,
        force_semantic: bool = False,
    ) -> AuditResult:
        """
        Executes two-phase L1/L2 context audit.
        - Phase 1 (L1): Deterministic heuristics and gate evaluation (<= 15ms).
        - Phase 2 (L2): Semantic evaluation via LLM adapter if required.
        """
        # 1. Normalize and parse input
        audit_input = normalize_input(raw_input)

        # 2. Extract deterministic signals and evaluate L1 Gate
        t_l1_start = time.perf_counter()
        signals = extract_deterministic_signals(audit_input)
        config = load_scoring_config()
        l1_verdict = compute_l1_gate(signals, config)
        l1_latency_ms = (time.perf_counter() - t_l1_start) * 1000.0
        l1_verdict.latency_ms = round(l1_latency_ms, 2)

        # 3. Determine if L1 fast path can be taken
        is_l1_fast_path = (
            (l1_verdict.route == GateRoute.PASS or fast_gate_only)
            and not force_semantic
            and not task_requires_factual
        )

        if is_l1_fast_path:
            dim_scores = synthesize_l1_dimension_scores(signals)
            confidence = 0.90
            coverage = 1.0

            risk_score, overall_status, triggered_rules = compute_irc(
                dimensions=dim_scores,
                evidence_coverage=coverage,
                task_requires_factual=task_requires_factual,
            )

            findings: list[Finding] = []
            for trigger in l1_verdict.triggers:
                findings.append(Finding(
                    finding_id=f"f-l1-{uuid.uuid4().hex[:6]}",
                    dimension="redundancy_pressure" if "redundancy" in trigger else "state_integrity",
                    epistemic_status=EpistemicStatus.RUNTIME_MEASURED,
                    severity=25,
                    evidence_refs=["runtime_telemetry"],
                    explanation=f"Deterministic trigger observed: {trigger}",
                    confidence=0.90,
                ))

            raw_actions: list[RecommendedAction] = []
            if l1_verdict.route == GateRoute.REMEDIATE_FIRST:
                raw_actions.append(RecommendedAction(
                    action="prune_stale_context",
                    target_refs=[],
                    reason="Excessive lexical redundancy or duplicate documents detected in L1 gate.",
                    requires_policy_approval=True,
                    destructive=True,
                ))
            filtered_actions = self.policy_engine.process_actions(raw_actions)
            limitations = ["Evaluated deterministically via L1 Fast Gate without LLM semantic inference."]
        else:
            # Phase 2: Invoke semantic adapter
            llm_eval = self.llm_adapter.evaluate_context(audit_input, signals)

            dim_scores = DimensionScores(**llm_eval.get("dimension_scores", {}))
            if dim_scores.lexical_redundancy is None:
                dim_scores.lexical_redundancy = int(round(signals.get("redundancy_ratio", 0.0) * 100))
            if dim_scores.positional_decay is None:
                dim_scores.positional_decay = int(signals.get("mid_context_penalty", 0))
            if dim_scores.prefix_volatility is None:
                dim_scores.prefix_volatility = (
                    int(min(100, signals.get("volatile_header_tokens", 0) * 5))
                    if signals.get("static_prefix_volatility_detected")
                    else 0
                )

            confidence = llm_eval.get("confidence", 0.0)
            coverage = llm_eval.get("evidence_coverage", 0.0)

            risk_score, overall_status, triggered_rules = compute_irc(
                dimensions=dim_scores,
                evidence_coverage=coverage,
                task_requires_factual=task_requires_factual,
            )

            raw_actions = [RecommendedAction(**act) for act in llm_eval.get("recommended_actions", [])]
            filtered_actions = self.policy_engine.process_actions(raw_actions)
            findings = [Finding(**f) for f in llm_eval.get("findings", [])]
            limitations = llm_eval.get("limitations", [])

        # 4. Assemble final Audit Result
        result = AuditResult(
            schema_version="1.0.0",
            audit_version="0.1.0",
            audit_id=f"audit-{uuid.uuid4().hex[:8]}",
            overall_status=overall_status,
            risk_score=risk_score,
            confidence=confidence,
            evidence_coverage=coverage,
            scope=AuditScope(
                messages_observed=signals.get("message_count"),
                documents_observed=signals.get("document_count"),
                tool_outputs_observed=len(audit_input.tool_events),
            ),
            dimension_scores=dim_scores,
            findings=findings,
            recommended_actions=filtered_actions,
            triggered_rules=triggered_rules,
            limitations=limitations,
            l1_verdict=l1_verdict,
        )

        # 5. Validate output against JSON schema
        validate_result(result.model_dump())

        return result
