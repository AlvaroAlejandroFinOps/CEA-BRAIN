import json
import subprocess
from unittest.mock import patch, MagicMock
import pytest

from src.context_auditor.adapters.antigravity import AntigravityAdapter
from src.context_auditor.adapters.base import AdapterExecutionError
from src.context_auditor.adapters.gemini import GeminiAdapter
from src.context_auditor.cli import resolve_adapter
from src.context_auditor.models import AuditInput, Message, Role


@pytest.fixture
def sample_audit_input():
    return AuditInput(
        messages=[
            Message(id="msg-1", role=Role.USER, content="Hello, audit this context."),
            Message(id="msg-2", role=Role.ASSISTANT, content="Analyzing now.")
        ],
        documents=[],
        tool_events=[]
    )


@pytest.fixture
def sample_signals():
    return {
        "message_count": 2,
        "document_count": 0,
        "instruction_count": 1,
        "repetition_ratio": 0.0,
        "stale_tool_drift": False
    }


def test_antigravity_adapter_init():
    adapter = AntigravityAdapter()
    assert adapter.model == "gemini-3.7-flash"
    assert adapter.agy_path == "agy.exe"
    assert adapter.timeout == 120
    assert "gemini-3.7-flash" in adapter.SUPPORTED_MODELS
    assert "gemini-3.1-pro" in adapter.SUPPORTED_MODELS

    custom_adapter = AntigravityAdapter(model="gemini-3.1-pro", agy_path="/usr/local/bin/agy", timeout=60)
    assert custom_adapter.model == "gemini-3.1-pro"
    assert custom_adapter.agy_path == "/usr/local/bin/agy"
    assert custom_adapter.timeout == 60


@patch("subprocess.run")
def test_antigravity_adapter_success(mock_run, sample_audit_input, sample_signals):
    mock_response = {
        "confidence": 0.92,
        "evidence_coverage": 1.0,
        "dimension_scores": {
            "instruction_conflict": 0,
            "task_ambiguity": 25,
            "context_contamination": 0,
            "evidence_quality": 0,
            "state_integrity": 0,
            "redundancy_pressure": 0
        },
        "findings": [
            {
                "dimension": "task_ambiguity",
                "severity": 25,
                "epistemic_category": "observed",
                "evidence": "Brief prompt without clear format constraint",
                "remediation": "Specify output format"
            }
        ],
        "recommended_actions": [],
        "limitations": []
    }

    mock_run.return_value = MagicMock(
        returncode=0,
        stdout=json.dumps(mock_response),
        stderr=""
    )

    adapter = AntigravityAdapter(model="gemini-3.7-flash")
    result = adapter.evaluate_context(sample_audit_input, sample_signals)

    assert result["confidence"] == 0.92
    assert result["dimension_scores"]["task_ambiguity"] == 25
    assert len(result["findings"]) == 1
    assert result["findings"][0]["dimension"] == "task_ambiguity"

    mock_run.assert_called_once()
    called_cmd = mock_run.call_args[0][0]
    assert called_cmd[0] == "agy.exe"
    assert "--model" in called_cmd
    assert "gemini-3.7-flash" in called_cmd


@patch("subprocess.run")
def test_antigravity_adapter_markdown_code_fences(mock_run, sample_audit_input, sample_signals):
    raw_payload = {
        "confidence": 0.88,
        "evidence_coverage": 0.9,
        "dimension_scores": {
            "instruction_conflict": 0,
            "task_ambiguity": 0,
            "context_contamination": 0,
            "evidence_quality": 0,
            "state_integrity": 0,
            "redundancy_pressure": 25
        },
        "findings": [],
        "recommended_actions": [],
        "limitations": []
    }
    wrapped_output = f"```json\n{json.dumps(raw_payload, indent=2)}\n```"

    mock_run.return_value = MagicMock(
        returncode=0,
        stdout=wrapped_output,
        stderr=""
    )

    adapter = AntigravityAdapter(model="gemini-3.8-flash")
    result = adapter.evaluate_context(sample_audit_input, sample_signals)

    assert result["confidence"] == 0.88
    assert result["dimension_scores"]["redundancy_pressure"] == 25


@patch("subprocess.run")
def test_antigravity_adapter_cli_envelope(mock_run, sample_audit_input, sample_signals):
    audit_data = {
        "confidence": 0.95,
        "evidence_coverage": 1.0,
        "dimension_scores": {
            "instruction_conflict": 0,
            "task_ambiguity": 0,
            "context_contamination": 0,
            "evidence_quality": 0,
            "state_integrity": 0,
            "redundancy_pressure": 0
        },
        "findings": [],
        "recommended_actions": [],
        "limitations": []
    }
    cli_envelope = {
        "conversation_id": "c34ce090-810a-42cc-b656-bfa3d288c850",
        "status": "SUCCESS",
        "response": f"```json\n{json.dumps(audit_data, indent=2)}\n```"
    }

    mock_run.return_value = MagicMock(
        returncode=0,
        stdout=json.dumps(cli_envelope),
        stderr=""
    )

    adapter = AntigravityAdapter(model="gemini-3.7-flash", effort="medium")
    result = adapter.evaluate_context(sample_audit_input, sample_signals)

    assert result["confidence"] == 0.95
    assert result["dimension_scores"]["instruction_conflict"] == 0


@patch("subprocess.run")
def test_antigravity_adapter_cli_failure(mock_run, sample_audit_input, sample_signals):
    mock_run.return_value = MagicMock(
        returncode=1,
        stdout="",
        stderr="Authentication failed or CLI error"
    )

    adapter = AntigravityAdapter()
    with pytest.raises(AdapterExecutionError) as excinfo:
        adapter.evaluate_context(sample_audit_input, sample_signals)

    assert "Antigravity CLI execution failed" in str(excinfo.value)
    assert "Authentication failed" in str(excinfo.value)


@patch("subprocess.run")
def test_antigravity_adapter_not_found(mock_run, sample_audit_input, sample_signals):
    mock_run.side_effect = FileNotFoundError("Executable not found")

    adapter = AntigravityAdapter(agy_path="nonexistent_agy.exe")
    with pytest.raises(AdapterExecutionError) as excinfo:
        adapter.evaluate_context(sample_audit_input, sample_signals)

    assert "was not found" in str(excinfo.value)


@patch("subprocess.run")
def test_antigravity_adapter_timeout(mock_run, sample_audit_input, sample_signals):
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="agy.exe", timeout=10)

    adapter = AntigravityAdapter(timeout=10)
    with pytest.raises(AdapterExecutionError) as excinfo:
        adapter.evaluate_context(sample_audit_input, sample_signals)

    assert "timed out after 10 seconds" in str(excinfo.value)


@patch("subprocess.run")
def test_antigravity_adapter_invalid_json(mock_run, sample_audit_input, sample_signals):
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="Fatal error: could not connect to local server",
        stderr=""
    )

    adapter = AntigravityAdapter()
    with pytest.raises(AdapterExecutionError) as excinfo:
        adapter.evaluate_context(sample_audit_input, sample_signals)

    assert "Failed to decode JSON" in str(excinfo.value)


def test_resolve_adapter_options():
    # Explicit antigravity
    adapter_ag = resolve_adapter(adapter_name="antigravity", model="gemini-3.1-pro")
    assert isinstance(adapter_ag, AntigravityAdapter)
    assert adapter_ag.model == "gemini-3.1-pro"

    # Explicit gemini
    adapter_gem = resolve_adapter(adapter_name="gemini", model="gemini-2.5-flash")
    assert isinstance(adapter_gem, GeminiAdapter)
    assert adapter_gem.model_name == "gemini-2.5-flash"

    # Explicit local_endpoint
    from src.context_auditor.adapters.local_endpoint import LocalEndpointAdapter
    adapter_loc = resolve_adapter(adapter_name="local_endpoint", model="qwen2.5:14b", endpoint_url="http://localhost:8000/v1")
    assert isinstance(adapter_loc, LocalEndpointAdapter)
    assert adapter_loc.model == "qwen2.5:14b"
    assert adapter_loc.base_url == "http://localhost:8000/v1"


@patch("subprocess.run")
def test_antigravity_adapter_stderr_isolation(mock_run, sample_audit_input, sample_signals):
    audit_data = {
        "confidence": 0.90,
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
        "limitations": [],
    }

    # Stderr contains warning, stdout contains clean JSON
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout=json.dumps(audit_data),
        stderr="WARNING: GPU memory low, falling back to CPU."
    )

    adapter = AntigravityAdapter()
    result = adapter.evaluate_context(sample_audit_input, sample_signals)
    assert result["confidence"] == 0.90
    assert result["dimension_scores"]["instruction_conflict"] == 0
