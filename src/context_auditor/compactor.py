import hashlib
from typing import List, Set
from src.context_auditor.models import AuditInput, Message, Document, ToolEvent, Role
from src.context_auditor.signals import compute_pairwise_ncd
from src.context_auditor.validators import validate_input


class ContextCompactor:
    """
    Immutable Context Compactor engine.
    Never modifies input AuditInput in-place (INV-03).
    Always validates output against audit-input.schema.json (INV-04).
    """

    def prune_stale_tools(self, audit_input: AuditInput, keep_recent: int = 3) -> AuditInput:
        """
        Compacts older tool event outputs into lightweight tombstone markers
        and synchronizes corresponding Role.TOOL messages.
        """
        cloned = audit_input.model_copy(deep=True)

        if len(cloned.tool_events) <= keep_recent:
            validate_input(cloned.model_dump(mode="json", exclude_none=True))
            return cloned

        stale_events = cloned.tool_events[:-keep_recent]
        stale_map = {t.id: t.tool_name for t in stale_events}

        for t in stale_events:
            t.result = f"[RESULT_COMPACTED_BY_CEA: id={t.id}, tool={t.tool_name}]"

        for m in cloned.messages:
            if (m.role == Role.TOOL or m.role == "tool") and m.id in stale_map:
                tool_name = stale_map[m.id]
                m.content = f"[RESULT_COMPACTED_BY_CEA: id={m.id}, tool={tool_name}]"

        validate_input(cloned.model_dump(mode="json", exclude_none=True))
        return cloned

    def deduplicate_documents(self, audit_input: AuditInput, ncd_threshold: float = 0.15) -> AuditInput:
        """
        Removes exact SHA-256 duplicate documents and near-duplicate documents
        having Normalized Compression Distance (NCD) below ncd_threshold.
        """
        cloned = audit_input.model_copy(deep=True)

        retained: List[Document] = []
        seen_hashes: Set[str] = set()

        for doc in cloned.documents:
            doc_hash = hashlib.sha256(doc.content.encode("utf-8")).hexdigest()
            if doc_hash in seen_hashes:
                continue

            # Check pairwise NCD against already retained documents
            is_near_dup = False
            for ret in retained:
                if compute_pairwise_ncd(doc.content, ret.content) < ncd_threshold:
                    is_near_dup = True
                    break

            if not is_near_dup:
                seen_hashes.add(doc_hash)
                retained.append(doc)

        cloned.documents = retained
        validate_input(cloned.model_dump(mode="json", exclude_none=True))
        return cloned

    def reanchor_instructions(self, audit_input: AuditInput) -> AuditInput:
        """
        Extracts foundational system directives and re-anchors them by inserting
        a sys_reanchor_cea reminder immediately before the last user turn.
        Preserves prompt caching prefix alignment.
        """
        cloned = audit_input.model_copy(deep=True)

        system_messages = [m for m in cloned.messages if m.role == Role.SYSTEM or m.role == "system"]
        if not system_messages:
            validate_input(cloned.model_dump(mode="json", exclude_none=True))
            return cloned

        first_sys = system_messages[0]
        anchor_content = (
            f"[REANCHORED_SYSTEM_DIRECTIVES]\n"
            f"Preserve core constraints: {first_sys.content[:400]}"
        )

        reanchor_msg = Message(
            id="sys_reanchor_cea",
            role=Role.SYSTEM,
            content=anchor_content
        )

        # Locate last user turn
        last_user_idx = -1
        for i in range(len(cloned.messages) - 1, -1, -1):
            if cloned.messages[i].role == Role.USER or cloned.messages[i].role == "user":
                last_user_idx = i
                break

        if last_user_idx >= 0:
            cloned.messages.insert(last_user_idx, reanchor_msg)
        else:
            cloned.messages.append(reanchor_msg)

        validate_input(cloned.model_dump(mode="json", exclude_none=True))
        return cloned

    def generate_handoff_payload(self, audit_input: AuditInput, state_summary: str) -> AuditInput:
        """
        Builds a clean checkpoint AuditInput preserving initial system instructions,
        deduplicated documents, and an authoritative state summary message.
        """
        cloned = self.deduplicate_documents(audit_input)

        # Retain initial system instructions
        retained_messages: List[Message] = []
        for m in cloned.messages:
            if m.role == Role.SYSTEM or m.role == "system":
                retained_messages.append(m)
            else:
                break

        checkpoint_msg = Message(
            id="msg_handoff_checkpoint",
            role=Role.SYSTEM,
            content=f"[SESSION_HANDOFF_CHECKPOINT]\n{state_summary}"
        )
        retained_messages.append(checkpoint_msg)

        cloned.messages = retained_messages
        cloned.tool_events = []
        validate_input(cloned.model_dump(mode="json", exclude_none=True))
        return cloned
