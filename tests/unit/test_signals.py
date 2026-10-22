import time
import pytest
from src.context_auditor.models import AuditInput, Message, Document, ToolEvent, Role
from src.context_auditor.signals import (
    extract_deterministic_signals,
    estimate_tokens,
    compute_compression_redundancy,
    compute_pairwise_ncd,
    analyze_positional_bias,
    audit_prefix_stability,
    track_tool_state_drift,
)


def get_base_input():
    return AuditInput(
        schema_version="1.0.0",
        messages=[
            Message(id="m1", role=Role.SYSTEM, content="A" * 40),
            Message(id="m2", role=Role.USER, content="B" * 40),
            Message(id="m3", role=Role.ASSISTANT, content="C" * 40),
            Message(id="m4", role=Role.USER, content="D" * 40),
        ],
        documents=[],
        tool_events=[],
    )


def test_estimate_tokens():
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("a" * 400) == 100
    assert estimate_tokens("") == 0


def test_signal_message_counts():
    data = get_base_input()
    signals = extract_deterministic_signals(data)
    assert signals["message_count"] == 4
    assert signals["user_turns"] == 2
    assert signals["assistant_turns"] == 1
    assert signals["messages_since_last_user_turn"] == 0


def test_signal_token_estimation():
    data = get_base_input()
    signals = extract_deterministic_signals(data)
    assert signals["estimated_tokens"] == 40
    assert signals["context_utilization_ratio"] == round(40 / 128000, 4)


def test_signal_document_duplication():
    data = get_base_input()
    data.documents = [
        Document(id="d1", content="same info", source="docA"),
        Document(id="d2", content="same info", source="docB"),
        Document(id="d3", content="different info", source="docA"),
    ]
    signals = extract_deterministic_signals(data)
    assert signals["document_count"] == 3
    assert signals["unique_sources"] == 2
    assert signals["exact_document_duplicates"] == 1


def test_signal_id_integrity():
    data = get_base_input()
    data.messages.append(Message(id="m1", role=Role.USER, content="test"))
    signals = extract_deterministic_signals(data)
    assert signals["duplicate_ids_found"] == 1


def test_signal_tool_replacement():
    data = get_base_input()
    data.tool_events = [
        ToolEvent(id="t1", tool_name="get_weather", parameters={"loc": "NY"}, result="Rain"),
        ToolEvent(id="t2", tool_name="get_weather", parameters={"loc": "NY"}, result="Sun"),
    ]
    signals = extract_deterministic_signals(data)
    assert signals["superseded_tool_results"] == 1


def test_signal_last_objective_recency():
    data = get_base_input()
    data.messages.append(Message(id="m5", role=Role.ASSISTANT, content="Wait"))
    data.messages.append(Message(id="m6", role=Role.ASSISTANT, content="Here"))
    signals = extract_deterministic_signals(data)
    assert signals["messages_since_last_user_turn"] == 2


# --- New Tests for FEP-001 ---

def test_compression_redundancy_and_latency():
    # Empty string should yield 0.0
    assert compute_compression_redundancy("") == 0.0

    # Highly repetitive string should yield high redundancy
    repetitive = "Hello world repetitive text pattern here! " * 2000
    ratio = compute_compression_redundancy(repetitive)
    assert 0.80 <= ratio <= 1.0

    # High entropy / random string should yield lower redundancy
    low_redundancy = "".join(chr((i * 37) % 94 + 32) for i in range(10000))
    low_ratio = compute_compression_redundancy(low_redundancy)
    assert low_ratio < ratio


def test_compute_pairwise_ncd():
    # Identical texts should have low NCD (~0.0 - 0.1)
    text1 = "The quick brown fox jumps over the lazy dog repeatedly in the forest."
    text2 = "The quick brown fox jumps over the lazy dog repeatedly in the forest."
    ncd_same = compute_pairwise_ncd(text1, text2)
    assert ncd_same < 0.20

    # Completely different texts
    text_diff = "Quantum mechanics and nuclear physics dictate the behaviour of subatomic particles."
    ncd_diff = compute_pairwise_ncd(text1, text_diff)
    assert ncd_diff > ncd_same

    # Edge cases
    assert compute_pairwise_ncd("", "") == 0.0
    assert compute_pairwise_ncd("abc", "") == 1.0
    # Length pre-filter (>20% difference returns 1.0 without compression)
    assert compute_pairwise_ncd("a" * 10, "a" * 50) == 1.0


def test_analyze_positional_bias_middle_zone():
    # Create messages spanning beginning, middle, and end
    # Total characters: 1000 (~250 tokens)
    # Message at p ~ 0.5 with restrictive negative directive
    messages = [
        Message(id="m1", role=Role.USER, content="A" * 300),          # p in [0.0, 0.30]
        Message(id="m2", role=Role.SYSTEM, content="MUST NOT do X: " + "B" * 200), # p in [0.30, 0.50]
        Message(id="m3", role=Role.USER, content="C" * 200),          # p in [0.50, 0.70]
        Message(id="m4", role=Role.ASSISTANT, content="D" * 300),     # p in [0.70, 1.0]
    ]
    bias = analyze_positional_bias(messages, [])
    assert bias["mid_context_penalty"] > 0
    assert "m2" in bias["mid_context_refs"]


def test_audit_prefix_stability_with_and_without_prev_hash():
    # Message with timestamp (volatile header)
    messages = [
        Message(id="m1", role=Role.SYSTEM, content="System initialized at 2026-10-22T09:00:00Z with session 550e8400-e29b-41d4-a716-446655440000"),
        Message(id="m2", role=Role.USER, content="Hello"),
    ]

    # Without previous hash -> observed_prefix_churn MUST be None [INV-02]
    audit_no_prev = audit_prefix_stability(messages, runtime_telemetry={})
    assert audit_no_prev["static_prefix_volatility_detected"] is True
    assert audit_no_prev["observed_prefix_churn"] is None
    current_hash = audit_no_prev["current_prefix_hash"]

    # With same previous hash -> observed_prefix_churn is False
    audit_same = audit_prefix_stability(messages, runtime_telemetry={"previous_prefix_hash": current_hash})
    assert audit_same["observed_prefix_churn"] is False

    # With different previous hash -> observed_prefix_churn is True
    audit_diff = audit_prefix_stability(messages, runtime_telemetry={"previous_prefix_hash": "different_hash_1234"})
    assert audit_diff["observed_prefix_churn"] is True


def test_track_tool_state_drift_json_and_phantom_ids():
    messages = [
        Message(id="m1", role=Role.USER, content="Run check"),
        Message(id="m2", role=Role.ASSISTANT, content="Based on tool-999 and t42, everything is OK."),
    ]
    tool_events = [
        ToolEvent(id="tool-1", tool_name="fetch_status", parameters={}, result='{"code": 200, "status": "active"}'),
        ToolEvent(id="tool-2", tool_name="fetch_status", parameters={}, result='{"code": 500, "status": "down"}'),
    ]

    drift = track_tool_state_drift(messages, tool_events)
    assert drift["superseded_tool_results"] == 1
    assert drift["stale_tool_drift_detected"] is True
    assert "tool-999" in drift["phantom_tool_refs"]
    assert "t42" in drift["phantom_tool_refs"]
    assert "code" in drift["parsed_tool_keys"]["tool-1"]


def test_l1_latency_budget_512kb():
    # Construct a 512 KB payload (~128k tokens)
    large_payload_str = "Agent reasoning test block sentence for entropy auditor. " * 8800 # ~512 KB
    assert len(large_payload_str.encode("utf-8")) >= 500_000

    audit_input = AuditInput(
        schema_version="1.0.0",
        messages=[
            Message(id="m1", role=Role.SYSTEM, content="System prompt instructions."),
            Message(id="m2", role=Role.USER, content=large_payload_str[:250_000]),
            Message(id="m3", role=Role.ASSISTANT, content=large_payload_str[250_000:]),
        ],
        documents=[
            Document(id="d1", content="Reference knowledge document 1"),
            Document(id="d2", content="Reference knowledge document 2"),
        ],
        tool_events=[],
        runtime_telemetry={},
    )

    start_time = time.perf_counter()
    signals = extract_deterministic_signals(audit_input)
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    # INV-05: deterministic extraction must complete in <= 15ms on ~512 KB
    assert elapsed_ms < 15.0, f"L1 signal extraction took {elapsed_ms:.2f}ms (> 15.0ms)"
    assert signals["redundancy_ratio"] > 0.0
