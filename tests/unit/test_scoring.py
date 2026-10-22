import pytest
from unittest.mock import MagicMock
from src.context_auditor.models import DimensionScores, OverallStatus, GateRoute, AuditInput, Message, Role
from src.context_auditor.scoring import (
    compute_irc,
    quantize_to_schema_enum,
    synthesize_l1_dimension_scores,
    compute_l1_gate,
)
from src.context_auditor.auditor import ContextAuditor
from src.context_auditor.adapters.base import BaseLLMAdapter


def test_compute_irc_perfect_score():
    dimensions = DimensionScores(
        instruction_conflict=0,
        task_ambiguity=0,
        context_contamination=0,
        evidence_quality=0,
        state_integrity=0,
        redundancy_pressure=0,
    )
    score, status, rules = compute_irc(dimensions, evidence_coverage=1.0)
    assert score == 0.0
    assert status == OverallStatus.STABLE
    assert len(rules) == 0


def test_compute_irc_moderate():
    dimensions = DimensionScores(
        instruction_conflict=25,
        task_ambiguity=50,
        context_contamination=25,
        evidence_quality=25,
        state_integrity=0,
        redundancy_pressure=75,
    )
    score, status, rules = compute_irc(dimensions, evidence_coverage=1.0)
    assert score == 31.25
    assert status == OverallStatus.MODERATE


def test_override_instruction_conflict():
    dimensions = DimensionScores(
        instruction_conflict=100,
        task_ambiguity=0,
        context_contamination=0,
        evidence_quality=0,
        state_integrity=0,
        redundancy_pressure=0,
    )
    score, status, rules = compute_irc(dimensions, evidence_coverage=1.0)
    assert score == 20.0
    assert status == OverallStatus.HIGH
    assert "critical_conflict_high_risk" in rules


def test_override_evidence_quality_factual():
    dimensions = DimensionScores(
        instruction_conflict=0,
        task_ambiguity=0,
        context_contamination=0,
        evidence_quality=100,
        state_integrity=0,
        redundancy_pressure=0,
    )
    score, status, rules = compute_irc(dimensions, evidence_coverage=1.0, task_requires_factual=True)
    assert score == 15.0
    assert status == OverallStatus.CRITICAL
    assert "critical_evidence_critical_risk" in rules


def test_override_low_coverage():
    dimensions = DimensionScores(
        instruction_conflict=0,
        task_ambiguity=0,
        context_contamination=0,
        evidence_quality=0,
        state_integrity=0,
        redundancy_pressure=0,
    )
    score, status, rules = compute_irc(dimensions, evidence_coverage=0.20)
    assert score == 0.0
    assert status == OverallStatus.MODERATE
    assert "low_coverage_warning" in rules
    assert "low_coverage_prevented_stable" in rules


# --- New Tests for FEP-003 ---

def test_synthesize_l1_dimension_scores_quantization():
    signals = {
        "mid_context_penalty": 30,
        "user_turns": 2,
        "messages_since_last_user_turn": 5,
        "context_utilization_ratio": 0.85,
        "duplicate_ids_found": 0,
        "document_count": 2,
        "unique_sources": 2,
        "stale_tool_drift_detected": False,
        "superseded_tool_results": 0,
        "phantom_tool_refs": [],
        "redundancy_ratio": 0.32,
        "exact_document_duplicates": 0,
        "near_duplicate_documents": 0,
        "volatile_header_tokens": 10,
        "static_prefix_volatility_detected": True,
    }

    dim_scores = synthesize_l1_dimension_scores(signals)

    # Every one of the 6 primary dimensions must be in {0, 25, 50, 75, 100} [AR-001]
    allowed_enums = {0, 25, 50, 75, 100}
    assert dim_scores.instruction_conflict in allowed_enums
    assert dim_scores.task_ambiguity in allowed_enums
    assert dim_scores.context_contamination in allowed_enums
    assert dim_scores.evidence_quality in allowed_enums
    assert dim_scores.state_integrity in allowed_enums
    assert dim_scores.redundancy_pressure in allowed_enums

    # Sub-metrics can be continuous
    assert 0 <= dim_scores.lexical_redundancy <= 100
    assert 0 <= dim_scores.positional_decay <= 100
    assert 0 <= dim_scores.prefix_volatility <= 100


def test_compute_l1_gate_routes():
    config = {
        "l1_gate_thresholds": {
            "redundancy_ratio": 0.85,
            "mid_context_penalty": 50,
            "stale_tool_drift": True,
            "objective_recency_turns": 15,
            "context_utilization_warning": 0.80,
        }
    }

    # Clean signal -> GateRoute.PASS
    clean_signals = {
        "mid_context_penalty": 0,
        "user_turns": 2,
        "messages_since_last_user_turn": 0,
        "context_utilization_ratio": 0.10,
        "duplicate_ids_found": 0,
        "document_count": 1,
        "unique_sources": 1,
        "stale_tool_drift_detected": False,
        "superseded_tool_results": 0,
        "phantom_tool_refs": [],
        "redundancy_ratio": 0.10,
        "exact_document_duplicates": 0,
        "near_duplicate_documents": 0,
        "volatile_header_tokens": 0,
        "static_prefix_volatility_detected": False,
        "observed_prefix_churn": False,
    }
    verdict_pass = compute_l1_gate(clean_signals, config)
    assert verdict_pass.route == GateRoute.PASS
    assert len(verdict_pass.triggers) == 0

    # Extreme redundancy -> GateRoute.REMEDIATE_FIRST
    extreme_signals = dict(clean_signals, redundancy_ratio=0.92)
    verdict_rem = compute_l1_gate(extreme_signals, config)
    assert verdict_rem.route == GateRoute.REMEDIATE_FIRST
    assert "extreme_lexical_redundancy" in verdict_rem.triggers

    # Drift -> GateRoute.FORCE_L2_AUDIT
    drift_signals = dict(clean_signals, stale_tool_drift_detected=True)
    verdict_force = compute_l1_gate(drift_signals, config)
    assert verdict_force.route == GateRoute.FORCE_L2_AUDIT
    assert "stale_tool_drift_detected" in verdict_force.triggers


def test_auditor_l1_pass_bypasses_llm_adapter():
    mock_adapter = MagicMock(spec=BaseLLMAdapter)
    auditor = ContextAuditor(llm_adapter=mock_adapter)

    clean_payload = {
        "schema_version": "1.0.0",
        "messages": [
            {"id": "m1", "role": "system", "content": "You are a concise assistant."},
            {"id": "m2", "role": "user", "content": "What is 2 + 2?"},
            {"id": "m3", "role": "assistant", "content": "4."},
        ],
        "documents": [],
        "tool_events": [],
    }

    result = auditor.audit(clean_payload)

    # In clean payload with GateRoute.PASS, LLM adapter is NOT called
    mock_adapter.evaluate_context.assert_not_called()
    assert result.l1_verdict is not None
    assert result.l1_verdict.route == GateRoute.PASS
    assert result.overall_status == OverallStatus.STABLE
    assert "L1 Fast Gate" in result.limitations[0]


def test_auditor_force_semantic_invokes_llm_adapter():
    mock_adapter = MagicMock(spec=BaseLLMAdapter)
    mock_adapter.evaluate_context.return_value = {
        "confidence": 0.95,
        "evidence_coverage": 1.0,
        "dimension_scores": {
            "instruction_conflict": 0,
            "task_ambiguity": 0,
            "context_contamination": 0,
            "evidence_quality": 0,
            "state_integrity": 0,
            "redundancy_pressure": 0,
        },
        "findings": [],
        "recommended_actions": [],
        "limitations": ["Evaluated by mock LLM."],
    }
    auditor = ContextAuditor(llm_adapter=mock_adapter)

    clean_payload = {
        "schema_version": "1.0.0",
        "messages": [
            {"id": "m1", "role": "user", "content": "Hello"},
        ],
    }

    # Explicit force_semantic=True forces LLM execution even on clean payload
    result = auditor.audit(clean_payload, force_semantic=True)

    mock_adapter.evaluate_context.assert_called_once()
    assert result.limitations == ["Evaluated by mock LLM."]
