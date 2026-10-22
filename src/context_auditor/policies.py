from enum import Enum
from typing import List, Dict, Any
from src.context_auditor.models import RecommendedAction

SESSION_HANDOFF_CHECKPOINT = "session_handoff_checkpoint"
SESSION_FORK_CLEAN = "session_fork_clean"
PRUNE_STALE_TOOL_OUTPUTS = "prune_stale_tool_outputs"
DEDUPLICATE_DOCUMENTS = "deduplicate_documents"
REANCHOR_SYSTEM_INSTRUCTIONS = "reanchor_system_instructions"


class PolicyMode(str, Enum):
    AUDIT_ONLY = "audit_only"
    RECOMMEND = "recommend"
    HUMAN_REVIEW = "human_review"
    DRY_RUN = "dry_run"


class PolicyEngine:
    def __init__(self, mode: PolicyMode = PolicyMode.RECOMMEND):
        self.mode = mode

    def process_actions(self, candidate_actions: List[RecommendedAction]) -> List[RecommendedAction]:
        """
        Filters and modifies actions based on the active policy mode.
        """
        if self.mode == PolicyMode.AUDIT_ONLY:
            return []

        processed_actions = []
        for action in candidate_actions:
            if action.destructive:
                action.requires_policy_approval = True

            if self.mode == PolicyMode.HUMAN_REVIEW:
                action.requires_policy_approval = True

            processed_actions.append(action)

        return processed_actions

    def can_execute_compaction(self, action: RecommendedAction, operator_confirmed: bool = False) -> bool:
        """
        Determines whether a compaction action can be physically executed.
        - In DRY_RUN mode: execution is allowed (simulated).
        - In RECOMMEND or HUMAN_REVIEW: requires explicit operator confirmation.
        - In AUDIT_ONLY: never permitted.
        """
        if self.mode == PolicyMode.AUDIT_ONLY:
            return False

        if self.mode == PolicyMode.DRY_RUN:
            return True

        if self.mode in (PolicyMode.RECOMMEND, PolicyMode.HUMAN_REVIEW):
            return bool(operator_confirmed)

        return False
