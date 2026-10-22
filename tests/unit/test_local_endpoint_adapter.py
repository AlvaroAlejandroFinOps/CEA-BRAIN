import json
import urllib.error
from unittest.mock import patch, MagicMock
import pytest

from src.context_auditor.adapters.local_endpoint import LocalEndpointAdapter
from src.context_auditor.adapters.base import AdapterExecutionError
from src.context_auditor.models import AuditInput, Message, Role


@pytest.fixture
def sample_audit_input():
    return AuditInput(
        messages=[
            Message(id="m1", role=Role.USER, content="Hello local endpoint")
        ],
        documents=[],
        tool_events=[]
    )


@pytest.fixture
def sample_signals():
    return {
        "message_count": 1,
        "document_count": 0,
        "redundancy_ratio": 0.0
    }


@patch("urllib.request.urlopen")
def test_local_endpoint_success(mock_urlopen, sample_audit_input, sample_signals):
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
    chat_response = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": json.dumps(audit_data)
                }
            }
        ]
    }

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(chat_response).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    adapter = LocalEndpointAdapter(base_url="http://localhost:11434/v1", model="qwen2.5:7b")
    result = adapter.evaluate_context(sample_audit_input, sample_signals)

    assert result["confidence"] == 0.95
    assert result["dimension_scores"]["instruction_conflict"] == 0
    mock_urlopen.assert_called_once()


@patch("urllib.request.urlopen")
def test_local_endpoint_markdown_fence_extraction(mock_urlopen, sample_audit_input, sample_signals):
    audit_data = {
        "confidence": 0.88,
        "evidence_coverage": 0.90,
        "dimension_scores": {
            "instruction_conflict": 25,
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
    fenced_content = f"Here is the evaluation:\n```json\n{json.dumps(audit_data, indent=2)}\n```"
    chat_response = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": fenced_content
                }
            }
        ]
    }

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(chat_response).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    adapter = LocalEndpointAdapter()
    result = adapter.evaluate_context(sample_audit_input, sample_signals)

    assert result["confidence"] == 0.88
    assert result["dimension_scores"]["instruction_conflict"] == 25


@patch("urllib.request.urlopen")
def test_local_endpoint_http_error(mock_urlopen, sample_audit_input, sample_signals):
    mock_err = urllib.error.HTTPError(
        url="http://localhost:11434/v1/chat/completions",
        code=500,
        msg="Internal Server Error",
        hdrs={},
        fp=None
    )
    mock_urlopen.side_effect = mock_err

    adapter = LocalEndpointAdapter()
    with pytest.raises(AdapterExecutionError) as exc_info:
        adapter.evaluate_context(sample_audit_input, sample_signals)

    assert "HTTP error 500" in str(exc_info.value)


@patch("urllib.request.urlopen")
def test_local_endpoint_url_error(mock_urlopen, sample_audit_input, sample_signals):
    mock_err = urllib.error.URLError(reason="Connection refused")
    mock_urlopen.side_effect = mock_err

    adapter = LocalEndpointAdapter()
    with pytest.raises(AdapterExecutionError) as exc_info:
        adapter.evaluate_context(sample_audit_input, sample_signals)

    assert "Failed to connect to local endpoint" in str(exc_info.value)
