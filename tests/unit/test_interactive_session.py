import json
import pytest
from pathlib import Path
from src.context_auditor.interactive import BenchmarkSession
from src.context_auditor.models import AuditResult, AuditScope, DimensionScores


@pytest.fixture
def temp_benchmark_session(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    session = BenchmarkSession(session_name="Test_Session", initial_model="gemini-3.7-flash", initial_effort="medium")
    return session


def test_benchmark_session_message_and_token_tracking(temp_benchmark_session):
    session = temp_benchmark_session
    
    msg1 = session.add_message(role="user", content="Test message 1 with some words.")
    msg2 = session.add_message(role="assistant", content="Response message.", model_used="gemini-3.1-pro")
    
    assert len(session.messages) == 2
    assert msg1 == "msg-1"
    assert msg2 == "msg-2"
    assert "gemini-3.7-flash" in session.models_used
    assert "gemini-3.1-pro" in session.models_used


def test_benchmark_session_record_and_save_artifacts(temp_benchmark_session):
    session = temp_benchmark_session
    session.add_message(role="user", content="Hello")
    session.add_document(content="Some document data", source="doc.txt")
    session.add_tool_event(tool_name="test_tool", parameters={"arg": 1}, result="result_str")

    dim_scores = DimensionScores(
        instruction_conflict=0,
        task_ambiguity=0,
        context_contamination=0,
        evidence_quality=0,
        state_integrity=0,
        redundancy_pressure=0
    )

    mock_audit_result = AuditResult(
        schema_version="1.0.0",
        audit_version="0.1.0",
        audit_id="audit-test-1",
        overall_status="stable",
        risk_score=0.0,
        confidence=0.95,
        evidence_coverage=1.0,
        scope=AuditScope(messages_observed=1, documents_observed=1, tool_outputs_observed=1),
        dimension_scores=dim_scores,
        findings=[],
        recommended_actions=[],
        triggered_rules=[],
        limitations=[]
    )

    session.record_turn_audit(turn_index=1, audit_result=mock_audit_result, latency_sec=1.5)

    assert len(session.timeline) == 1
    assert session.timeline[0]["risk_score"] == 0.0

    # Verify physical artifacts created atomically without leaving .tmp files
    assert (session.logs_dir / "session_meta.json").exists()
    assert (session.logs_dir / "conversation.json").exists()
    assert (session.logs_dir / "timeline.json").exists()
    assert (session.logs_dir / "summary_report.md").exists()
    assert not (session.logs_dir / "session_meta.json.tmp").exists()

    meta = json.loads((session.logs_dir / "session_meta.json").read_text(encoding="utf-8"))
    assert meta["session_name"] == "Test_Session"
    assert meta["turns_count"] == 1


def test_atomic_save_snapshot_and_prefix_hash(temp_benchmark_session):
    session = temp_benchmark_session
    session.add_message(role="system", content="System instruction.")
    session.add_message(role="user", content="User prompt.")

    # Set last prefix hash
    session.last_prefix_hash = "abc123hash"
    audit_input = session.build_audit_input()
    assert audit_input.runtime_telemetry.get("previous_prefix_hash") == "abc123hash"

    # Save snapshot executes atomically
    session.save_snapshot()
    assert (session.logs_dir / "session_meta.json").exists()
    assert not (session.logs_dir / "session_meta.json.tmp").exists()
