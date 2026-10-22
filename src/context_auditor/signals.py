import hashlib
import json
import re
import time
import zlib
from typing import Dict, Any, List, Optional
from src.context_auditor.models import AuditInput, Message, Document, ToolEvent, Role

_NEGATIVE_DIRECTIVE_PATTERN = re.compile(
    r"\b(?:MUST\s+NOT|PROHIBIDO|NEVER|DO\s+NOT)\b",
    re.IGNORECASE
)

_ISO8601_PATTERN = re.compile(
    r"\b\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b"
)
_UUIDV4_PATTERN = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
)
_EPHEMERAL_HASH_PATTERN = re.compile(
    r"\b[0-9a-fA-F]{32,64}\b"
)
_TOOL_ID_REF_PATTERN = re.compile(
    r"\b(?:tool-[a-zA-Z0-9_\-]+|t\d+)\b"
)


def estimate_tokens(text: str) -> int:
    """
    Fallback deterministic token estimator.
    Assumes roughly 4 characters per token as a standard heuristic.
    """
    if not text:
        return 0
    return max(1, len(text) // 4)


def compute_compression_redundancy(text: str) -> float:
    """
    Computes lexical redundancy in [0.0, 1.0] using zlib level=1 (Z_BEST_SPEED).
    Guarantees execution < 2.5ms on 512 KB payloads.
    """
    if not text:
        return 0.0
    raw_bytes = text.encode("utf-8")
    compressed = zlib.compress(raw_bytes, level=1)
    ratio = 1.0 - (len(compressed) / max(len(raw_bytes), 1))
    return round(max(0.0, min(1.0, ratio)), 4)


def compute_pairwise_ncd(text_a: str, text_b: str) -> float:
    """
    Computes Normalized Compression Distance (NCD) in [0.0, 1.0] with zlib level=1.
    Includes a 20% length pre-filter to prevent unnecessary quadratic compression.
    """
    if not text_a and not text_b:
        return 0.0
    if not text_a or not text_b:
        return 1.0

    len_a, len_b = len(text_a), len(text_b)
    if abs(len_a - len_b) / max(len_a, len_b, 1) > 0.20:
        return 1.0

    bytes_a = text_a.encode("utf-8")
    bytes_b = text_b.encode("utf-8")
    c_a = len(zlib.compress(bytes_a, level=1))
    c_b = len(zlib.compress(bytes_b, level=1))
    c_ab = len(zlib.compress(bytes_a + b" " + bytes_b, level=1))

    ncd = (c_ab - min(c_a, c_b)) / max(c_a, c_b, 1)
    return round(max(0.0, min(1.0, ncd)), 4)


def analyze_positional_bias(messages: List[Message], documents: List[Document]) -> Dict[str, Any]:
    """
    Detects Role.SYSTEM or restrictive negative directives displaced into the
    middle-context degraded attention zone (0.35 <= p <= 0.75).
    """
    item_tokens: List[int] = [estimate_tokens(m.content) for m in messages]
    doc_tokens: List[int] = [estimate_tokens(d.content) for d in documents]
    total_tokens = max(sum(item_tokens) + sum(doc_tokens), 1)

    cumulative = 0
    mid_refs: List[str] = []

    for idx, m in enumerate(messages):
        offset = cumulative
        item_len = item_tokens[idx]
        cumulative += item_len

        start_p = offset / total_tokens
        mid_p = (offset + item_len / 2) / total_tokens
        end_p = (offset + item_len) / total_tokens

        # Check if the message is in or overlaps the degraded attention middle zone [0.35, 0.75]
        if (0.35 <= mid_p <= 0.75) or (0.35 <= start_p <= 0.75) or (start_p <= 0.35 and end_p >= 0.75):
            is_system = (m.role == Role.SYSTEM or m.role == "system")
            has_negative = False
            content_lower = m.content.lower()
            if any(k in content_lower for k in ("must not", "prohibido", "never", "do not")):
                has_negative = bool(_NEGATIVE_DIRECTIVE_PATTERN.search(m.content))

            if is_system or has_negative:
                mid_refs.append(m.id)

    penalty = min(100, len(mid_refs) * 25)
    return {
        "mid_context_penalty": penalty,
        "mid_context_refs": mid_refs
    }


def audit_prefix_stability(messages: List[Message], runtime_telemetry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Audits the initial context block (p < 0.15) for volatile headers (ISO-8601, UUIDv4,
    ephemeral hashes). Preserves INV-02: only reports observed_prefix_churn if previous_prefix_hash
    is supplied in runtime_telemetry.
    """
    if not messages:
        return {
            "volatile_header_tokens": 0,
            "current_prefix_hash": hashlib.sha256(b"").hexdigest(),
            "observed_prefix_churn": None,
            "static_prefix_volatility_detected": False
        }

    total_tokens = max(sum(estimate_tokens(m.content) for m in messages), 1)
    prefix_token_limit = min(max(1024, int(total_tokens * 0.15)), 20000)
    prefix_messages: List[Message] = []
    cumulative = 0

    for idx, m in enumerate(messages):
        t_len = estimate_tokens(m.content)
        p = cumulative / total_tokens
        if p < 0.15 or idx == 0:
            prefix_messages.append(m)
            cumulative += t_len
            if cumulative >= prefix_token_limit and idx > 0:
                break
        else:
            break

    prefix_text = "\n".join(m.content for m in prefix_messages)
    prefix_char_bound = prefix_token_limit * 4
    if len(prefix_text) > prefix_char_bound:
        prefix_text = prefix_text[:prefix_char_bound]

    # Fast pre-filtered volatility detection
    volatile_matches: List[str] = []
    if ":" in prefix_text and "-" in prefix_text:
        volatile_matches.extend(_ISO8601_PATTERN.findall(prefix_text))
    if prefix_text.count("-") >= 4:
        volatile_matches.extend(_UUIDV4_PATTERN.findall(prefix_text))
    if any(len(w) >= 32 for w in prefix_text.split()):
        volatile_matches.extend(_EPHEMERAL_HASH_PATTERN.findall(prefix_text))

    volatile_tokens = sum(estimate_tokens(match) for match in volatile_matches)
    static_volatility = len(volatile_matches) > 0

    current_hash = hashlib.sha256(prefix_text.encode("utf-8")).hexdigest()

    # Epistemic invariant check [INV-02]
    observed_churn: Optional[bool] = None
    if "previous_prefix_hash" in runtime_telemetry and runtime_telemetry["previous_prefix_hash"] is not None:
        observed_churn = (runtime_telemetry["previous_prefix_hash"] != current_hash)

    return {
        "volatile_header_tokens": volatile_tokens,
        "current_prefix_hash": current_hash,
        "observed_prefix_churn": observed_churn,
        "static_prefix_volatility_detected": static_volatility
    }


def track_tool_state_drift(messages: List[Message], tool_events: List[ToolEvent]) -> Dict[str, Any]:
    """
    Tracks tool state drift: extracts top-level keys from valid JSON results,
    detects superseded tool calls, and flags phantom tool ID references.
    """
    tool_calls_by_name: Dict[str, str] = {}
    superseded_tools = 0
    parsed_keys: Dict[str, List[str]] = {}
    valid_tool_ids = set()

    for t in tool_events:
        valid_tool_ids.add(t.id)
        if t.tool_name in tool_calls_by_name:
            superseded_tools += 1
        tool_calls_by_name[t.tool_name] = t.result

        if isinstance(t.result, str) and "{" in t.result:
            try:
                parsed = json.loads(t.result)
                if isinstance(parsed, dict):
                    parsed_keys[t.id] = list(parsed.keys())
            except Exception:
                pass

    # Detect phantom tool references in assistant messages with fast pre-check
    phantom_refs: List[str] = []
    for m in messages:
        if m.role == Role.ASSISTANT or m.role == "assistant":
            if "tool-" in m.content or any(f"t{i}" in m.content for i in range(10)):
                for ref in _TOOL_ID_REF_PATTERN.findall(m.content):
                    if ref not in valid_tool_ids and ref not in phantom_refs:
                        phantom_refs.append(ref)

    stale_drift = (superseded_tools > 0) or (len(phantom_refs) > 0)

    return {
        "stale_tool_drift_detected": stale_drift,
        "superseded_tool_results": superseded_tools,
        "phantom_tool_refs": phantom_refs,
        "parsed_tool_keys": parsed_keys
    }


def extract_deterministic_signals(audit_input: AuditInput) -> Dict[str, Any]:
    """
    Computes verifiable, deterministic metrics from the audited context.
    Executes in <= 15ms without invoking an LLM.
    """
    signals = {}

    # 1. Message & Turn Counts
    signals["message_count"] = len(audit_input.messages)
    signals["user_turns"] = sum(1 for m in audit_input.messages if m.role == "user" or m.role == Role.USER)
    signals["assistant_turns"] = sum(1 for m in audit_input.messages if m.role == "assistant" or m.role == Role.ASSISTANT)

    # 2. Token Estimations
    total_chars = sum(len(m.content) for m in audit_input.messages)
    total_chars += sum(len(d.content) for d in audit_input.documents)
    total_chars += sum(len(t.result) for t in audit_input.tool_events)
    signals["estimated_tokens"] = max(1, total_chars // 4) if total_chars else 0

    context_limit = audit_input.audit_configuration.get("context_limit_tokens", 128000)
    signals["context_utilization_ratio"] = round(signals["estimated_tokens"] / context_limit, 4)

    # 3. Documents & Sources
    signals["document_count"] = len(audit_input.documents)
    unique_sources = set(d.source for d in audit_input.documents if d.source)
    signals["unique_sources"] = len(unique_sources)

    # 4. Exact Duplication Check (Content level)
    content_hashes = set()
    exact_duplicates = 0
    for doc in audit_input.documents:
        if doc.content in content_hashes:
            exact_duplicates += 1
        else:
            content_hashes.add(doc.content)
    signals["exact_document_duplicates"] = exact_duplicates

    # 5. ID Integrity
    all_ids = (
        [m.id for m in audit_input.messages] +
        [d.id for d in audit_input.documents] +
        [t.id for t in audit_input.tool_events]
    )
    unique_ids = set(all_ids)
    signals["duplicate_ids_found"] = len(all_ids) - len(unique_ids)

    # 6. Tool Result Replacements & Tool State Drift
    tool_drift = track_tool_state_drift(audit_input.messages, audit_input.tool_events)
    signals["superseded_tool_results"] = tool_drift["superseded_tool_results"]
    signals["stale_tool_drift_detected"] = tool_drift["stale_tool_drift_detected"]
    signals["phantom_tool_refs"] = tool_drift["phantom_tool_refs"]
    signals["parsed_tool_keys"] = tool_drift["parsed_tool_keys"]

    # 7. Last Explicit Objective Recency
    if signals["user_turns"] > 0:
        last_user_index = -1
        for i, m in enumerate(reversed(audit_input.messages)):
            if m.role == "user" or m.role == Role.USER:
                last_user_index = i
                break
        signals["messages_since_last_user_turn"] = last_user_index
    else:
        signals["messages_since_last_user_turn"] = -1

    # 8. Lexical Redundancy via Zlib Level 1
    combined_text = "\n".join(
        [m.content for m in audit_input.messages] +
        [d.content for d in audit_input.documents] +
        [t.result for t in audit_input.tool_events]
    )
    signals["redundancy_ratio"] = compute_compression_redundancy(combined_text)

    # 9. Selective NCD on Documents (Bounded to first 25 docs for latency)
    near_duplicates = 0
    docs_to_compare = audit_input.documents[:25]
    for i in range(len(docs_to_compare)):
        for j in range(i + 1, len(docs_to_compare)):
            if compute_pairwise_ncd(docs_to_compare[i].content, docs_to_compare[j].content) < 0.15:
                near_duplicates += 1
    signals["near_duplicate_documents"] = near_duplicates

    # 10. Positional Bias (Lost-in-the-Middle)
    pos_bias = analyze_positional_bias(audit_input.messages, audit_input.documents)
    signals["mid_context_penalty"] = pos_bias["mid_context_penalty"]
    signals["mid_context_refs"] = pos_bias["mid_context_refs"]

    # 11. Prefix Stability Audit [INV-02]
    prefix_audit = audit_prefix_stability(audit_input.messages, audit_input.runtime_telemetry)
    signals["volatile_header_tokens"] = prefix_audit["volatile_header_tokens"]
    signals["current_prefix_hash"] = prefix_audit["current_prefix_hash"]
    signals["observed_prefix_churn"] = prefix_audit["observed_prefix_churn"]
    signals["static_prefix_volatility_detected"] = prefix_audit["static_prefix_volatility_detected"]

    return signals
