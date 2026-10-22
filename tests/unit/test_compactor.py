import pytest
from src.context_auditor.models import AuditInput, Message, Document, ToolEvent, Role
from src.context_auditor.compactor import ContextCompactor
from src.context_auditor.validators import validate_input


@pytest.fixture
def base_compactor_input():
    return AuditInput(
        schema_version="1.0.0",
        messages=[
            Message(id="m1", role=Role.SYSTEM, content="Base system instructions for the agent."),
            Message(id="m2", role=Role.USER, content="Query 1"),
            Message(id="m3", role=Role.TOOL, content='{"status": "ok", "value": 1}'),
            Message(id="m4", role=Role.ASSISTANT, content="Step 1 complete."),
            Message(id="m5", role=Role.USER, content="Query 2"),
        ],
        documents=[
            Document(id="d1", content="Reference doc A"),
            Document(id="d2", content="Reference doc A"), # Exact duplicate
            Document(id="d3", content="Reference doc A with slight variance"), # Near duplicate
            Document(id="d4", content="Completely distinct information about quantum astrophysics"),
        ],
        tool_events=[
            ToolEvent(id="m3", tool_name="fetch_status", parameters={}, result='{"status": "ok", "value": 1}'),
            ToolEvent(id="t2", tool_name="calc_value", parameters={}, result="val_2"),
            ToolEvent(id="t3", tool_name="calc_value", parameters={}, result="val_3"),
            ToolEvent(id="t4", tool_name="calc_value", parameters={}, result="val_4"),
            ToolEvent(id="t5", tool_name="calc_value", parameters={}, result="val_5"),
        ]
    )


def test_prune_stale_tools_immutability_and_sync(base_compactor_input):
    compactor = ContextCompactor()
    original_input = base_compactor_input
    original_tool_count = len(original_input.tool_events)
    original_msg_content = original_input.messages[2].content

    # Keep only the 2 most recent tool events
    compacted = compactor.prune_stale_tools(original_input, keep_recent=2)

    # Invariant INV-03: Original object is NOT mutated
    assert len(original_input.tool_events) == original_tool_count
    assert original_input.messages[2].content == original_msg_content
    assert id(compacted) != id(original_input)

    # Stale tool events are compacted
    assert len(compacted.tool_events) == 5
    assert "[RESULT_COMPACTED_BY_CEA" in compacted.tool_events[0].result
    assert "[RESULT_COMPACTED_BY_CEA" in compacted.tool_events[1].result
    assert "[RESULT_COMPACTED_BY_CEA" in compacted.tool_events[2].result
    # Most recent 2 remain untouched
    assert compacted.tool_events[3].result == "val_4"
    assert compacted.tool_events[4].result == "val_5"

    # Synchronized Role.TOOL message (id="m3") is also compacted
    assert "[RESULT_COMPACTED_BY_CEA" in compacted.messages[2].content

    # Invariant INV-04: Compacted output matches schema
    validate_input(compacted.model_dump(mode="json", exclude_none=True))


def test_deduplicate_documents_exact_and_ncd(base_compactor_input):
    compactor = ContextCompactor()
    original_input = base_compactor_input

    compacted = compactor.deduplicate_documents(original_input, ncd_threshold=0.20)

    # Invariant INV-03: Original object is NOT mutated
    assert len(original_input.documents) == 4
    assert id(compacted) != id(original_input)

    # Retained docs should be fewer (exact and near duplicates removed)
    assert len(compacted.documents) < 4
    # The completely distinct doc must remain
    assert any("quantum astrophysics" in d.content for d in compacted.documents)

    # Invariant INV-04: Compacted output matches schema
    validate_input(compacted.model_dump(mode="json", exclude_none=True))


def test_reanchor_instructions_before_last_user(base_compactor_input):
    compactor = ContextCompactor()
    original_input = base_compactor_input

    compacted = compactor.reanchor_instructions(original_input)

    assert id(compacted) != id(original_input)
    assert len(compacted.messages) == len(original_input.messages) + 1

    # Check insertion immediately before the last user turn (which was m5)
    last_msg = compacted.messages[-1]
    second_to_last = compacted.messages[-2]

    assert last_msg.id == "m5"
    assert second_to_last.id == "sys_reanchor_cea"
    assert second_to_last.role == Role.SYSTEM
    assert "[REANCHORED_SYSTEM_DIRECTIVES]" in second_to_last.content

    # Invariant INV-04: Compacted output matches schema
    validate_input(compacted.model_dump(mode="json", exclude_none=True))


def test_generate_handoff_payload_valid_schema(base_compactor_input):
    compactor = ContextCompactor()
    original_input = base_compactor_input

    handoff = compactor.generate_handoff_payload(original_input, state_summary="Phase 1 complete. Next: execute Phase 2.")

    assert id(handoff) != id(original_input)
    assert handoff.messages[0].id == "m1"
    assert handoff.messages[-1].id == "msg_handoff_checkpoint"
    assert "[SESSION_HANDOFF_CHECKPOINT]" in handoff.messages[-1].content
    assert len(handoff.tool_events) == 0

    # Invariant INV-04: Compacted output matches schema
    validate_input(handoff.model_dump(mode="json", exclude_none=True))
