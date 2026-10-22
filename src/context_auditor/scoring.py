import os
import yaml
from typing import Dict, Any, Tuple, List
from src.context_auditor.models import DimensionScores, OverallStatus, GateRoute, L1GateVerdict


def load_scoring_config() -> Dict[str, Any]:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(base_dir, "config", "scoring_defaults.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def quantize_to_schema_enum(value: float) -> int:
    """
    Quantizes a continuous score [0, 100] to the nearest schema enum {0, 25, 50, 75, 100}.
    """
    clamped = max(0.0, min(100.0, float(value)))
    return int(min((0, 25, 50, 75, 100), key=lambda b: abs(b - clamped)))


def synthesize_l1_dimension_scores(signals: Dict[str, Any]) -> DimensionScores:
    """
    Synthesizes L1 deterministic signals into the 6 quantized primary dimensions
    and populates optional continuous sub-metrics [0, 100].
    """
    # 1. Instruction Conflict: mid-context penalty
    mid_pen = signals.get("mid_context_penalty", 0)
    conflict_val = quantize_to_schema_enum(mid_pen)

    # 2. Task Ambiguity: user turn recency / distance
    user_turns = signals.get("user_turns", 0)
    recency = signals.get("messages_since_last_user_turn", 0)
    ambiguity_raw = 0
    if user_turns == 0:
        ambiguity_raw = 100
    elif recency > 15:
        ambiguity_raw = 75
    elif recency > 8:
        ambiguity_raw = 50
    elif recency > 4:
        ambiguity_raw = 25
    ambiguity_val = quantize_to_schema_enum(ambiguity_raw)

    # 3. Context Contamination: context utilization ratio + duplicate IDs
    util_ratio = signals.get("context_utilization_ratio", 0.0)
    dup_ids = signals.get("duplicate_ids_found", 0)
    contam_raw = 0
    if util_ratio >= 0.95:
        contam_raw += 75
    elif util_ratio >= 0.80:
        contam_raw += 50
    elif util_ratio >= 0.60:
        contam_raw += 25
    if dup_ids > 0:
        contam_raw += 25
    contamination_val = quantize_to_schema_enum(contam_raw)

    # 4. Evidence Quality: unique sources vs documents
    doc_count = signals.get("document_count", 0)
    unique_sources = signals.get("unique_sources", 0)
    evidence_raw = 0
    if doc_count > 0 and unique_sources == 0:
        evidence_raw = 50
    evidence_val = quantize_to_schema_enum(evidence_raw)

    # 5. State Integrity: tool state drift & superseded results
    stale_drift = signals.get("stale_tool_drift_detected", False)
    superseded = signals.get("superseded_tool_results", 0)
    phantom_refs = len(signals.get("phantom_tool_refs", []))
    state_raw = 0
    if stale_drift:
        state_raw += 50
    state_raw += superseded * 25 + phantom_refs * 25
    state_val = quantize_to_schema_enum(state_raw)

    # 6. Redundancy Pressure: lexical compression ratio + duplicate docs
    redundancy_ratio = signals.get("redundancy_ratio", 0.0)
    exact_dups = signals.get("exact_document_duplicates", 0)
    near_dups = signals.get("near_duplicate_documents", 0)
    red_raw = (redundancy_ratio * 100.0) + (exact_dups * 25) + (near_dups * 20)
    redundancy_val = quantize_to_schema_enum(red_raw)

    # Sub-metrics (continuous int 0-100)
    lex_redundancy = int(round(max(0.0, min(100.0, redundancy_ratio * 100.0))))
    pos_decay = int(max(0, min(100, mid_pen)))
    vol_tokens = signals.get("volatile_header_tokens", 0)
    pref_vol = int(min(100, vol_tokens * 5)) if signals.get("static_prefix_volatility_detected") else 0

    return DimensionScores(
        instruction_conflict=conflict_val,
        task_ambiguity=ambiguity_val,
        context_contamination=contamination_val,
        evidence_quality=evidence_val,
        state_integrity=state_val,
        redundancy_pressure=redundancy_val,
        lexical_redundancy=lex_redundancy,
        positional_decay=pos_decay,
        prefix_volatility=pref_vol,
    )


def compute_l1_gate(signals: Dict[str, Any], config: Dict[str, Any]) -> L1GateVerdict:
    """
    Evaluates L1 deterministic triggers and produces GateRoute and L1 risk score.
    """
    thresholds = config.get("l1_gate_thresholds", {
        "redundancy_ratio": 0.85,
        "mid_context_penalty": 50,
        "stale_tool_drift": True,
        "objective_recency_turns": 15,
        "context_utilization_warning": 0.80,
    })

    triggers: List[str] = []

    redundancy_ratio = signals.get("redundancy_ratio", 0.0)
    if redundancy_ratio >= thresholds.get("redundancy_ratio", 0.85):
        triggers.append("extreme_lexical_redundancy")

    exact_dups = signals.get("exact_document_duplicates", 0)
    if exact_dups >= 3:
        triggers.append("multiple_exact_duplicate_documents")

    mid_penalty = signals.get("mid_context_penalty", 0)
    if mid_penalty >= thresholds.get("mid_context_penalty", 50):
        triggers.append("mid_context_instruction_decay")

    if signals.get("stale_tool_drift_detected", False):
        triggers.append("stale_tool_drift_detected")

    recency = signals.get("messages_since_last_user_turn", 0)
    if recency >= thresholds.get("objective_recency_turns", 15):
        triggers.append("stale_objective_recency")

    if signals.get("observed_prefix_churn") is True:
        triggers.append("prefix_cache_churn_detected")

    util_ratio = signals.get("context_utilization_ratio", 0.0)
    if util_ratio >= thresholds.get("context_utilization_warning", 0.80):
        triggers.append("high_context_utilization")

    # Synthesize scores to get estimated L1 risk
    dim_scores = synthesize_l1_dimension_scores(signals)
    l1_risk, _, _ = compute_irc(dim_scores, evidence_coverage=1.0)

    # Determine route
    if "extreme_lexical_redundancy" in triggers or exact_dups >= 3:
        route = GateRoute.REMEDIATE_FIRST
    elif len(triggers) > 0 or l1_risk >= 25.0:
        route = GateRoute.FORCE_L2_AUDIT
    else:
        route = GateRoute.PASS

    return L1GateVerdict(
        route=route,
        l1_risk_score=l1_risk,
        triggers=triggers,
        latency_ms=0.0,
    )


def compute_base_status(score: float, thresholds: Dict[str, float]) -> OverallStatus:
    if score <= thresholds["stable"]:
        return OverallStatus.STABLE
    elif score <= thresholds["moderate"]:
        return OverallStatus.MODERATE
    elif score <= thresholds["high"]:
        return OverallStatus.HIGH
    else:
        return OverallStatus.CRITICAL


def compute_irc(
    dimensions: DimensionScores,
    evidence_coverage: float,
    task_requires_factual: bool = False
) -> Tuple[float, OverallStatus, list[str]]:
    config = load_scoring_config()
    weights = config["weights"]

    # 1. Compute base score
    raw_score = (
        dimensions.instruction_conflict * weights["instruction_conflict"] +
        dimensions.task_ambiguity * weights["task_ambiguity"] +
        dimensions.context_contamination * weights["context_contamination"] +
        dimensions.evidence_quality * weights["evidence_quality"] +
        dimensions.state_integrity * weights["state_integrity"] +
        dimensions.redundancy_pressure * weights["redundancy_pressure"]
    )

    # 2. Determine base status
    status = compute_base_status(raw_score, config["thresholds"])
    triggered_rules = []

    # 3. Apply override rules
    rules = config.get("override_rules", {})

    # Rule: Critical Conflict
    if dimensions.instruction_conflict == 100:
        if status in [OverallStatus.STABLE, OverallStatus.MODERATE]:
            status = OverallStatus.HIGH
            triggered_rules.append("critical_conflict_high_risk")

    # Rule: Critical State Integrity
    if dimensions.state_integrity == 100:
        if status in [OverallStatus.STABLE, OverallStatus.MODERATE]:
            status = OverallStatus.HIGH
            triggered_rules.append("critical_state_high_risk")

    # Rule: Critical Evidence Quality on Factual Tasks
    if dimensions.evidence_quality == 100 and task_requires_factual:
        status = OverallStatus.CRITICAL
        triggered_rules.append("critical_evidence_critical_risk")

    # Rule: Low Coverage Warning
    if evidence_coverage < 0.30:
        triggered_rules.append("low_coverage_warning")
        if status == OverallStatus.STABLE:
            triggered_rules.append("low_coverage_prevented_stable")
            status = OverallStatus.MODERATE

    return round(raw_score, 2), status, triggered_rules
