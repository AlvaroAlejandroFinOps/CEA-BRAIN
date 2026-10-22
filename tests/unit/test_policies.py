import pytest
from src.context_auditor.models import RecommendedAction
from src.context_auditor.policies import (
    PolicyEngine,
    PolicyMode,
    SESSION_HANDOFF_CHECKPOINT,
    PRUNE_STALE_TOOL_OUTPUTS,
    DEDUPLICATE_DOCUMENTS,
)

def test_policy_audit_only():
    engine = PolicyEngine(mode=PolicyMode.AUDIT_ONLY)
    actions = [
        RecommendedAction(action="summarize", reason="too long", requires_policy_approval=False, destructive=False)
    ]
    processed = engine.process_actions(actions)
    assert len(processed) == 0

def test_policy_recommend():
    engine = PolicyEngine(mode=PolicyMode.RECOMMEND)
    actions = [
        RecommendedAction(action="summarize", reason="too long", requires_policy_approval=False, destructive=False),
        RecommendedAction(action="delete", reason="stale", requires_policy_approval=False, destructive=True)
    ]
    processed = engine.process_actions(actions)
    assert len(processed) == 2
    assert processed[0].requires_policy_approval == False
    assert processed[1].requires_policy_approval == True

def test_policy_human_review():
    engine = PolicyEngine(mode=PolicyMode.HUMAN_REVIEW)
    actions = [
        RecommendedAction(action="summarize", reason="too long", requires_policy_approval=False, destructive=False)
    ]
    processed = engine.process_actions(actions)
    assert len(processed) == 1
    assert processed[0].requires_policy_approval == True

def test_can_execute_compaction_modes():
    act = RecommendedAction(
        action=PRUNE_STALE_TOOL_OUTPUTS,
        reason="Test compaction",
        requires_policy_approval=True,
        destructive=True
    )

    # AUDIT_ONLY -> never allowed
    engine_audit = PolicyEngine(mode=PolicyMode.AUDIT_ONLY)
    assert engine_audit.can_execute_compaction(act, operator_confirmed=True) is False

    # DRY_RUN -> always allowed (simulated)
    engine_dry = PolicyEngine(mode=PolicyMode.DRY_RUN)
    assert engine_dry.can_execute_compaction(act, operator_confirmed=False) is True

    # RECOMMEND -> requires operator confirmation
    engine_rec = PolicyEngine(mode=PolicyMode.RECOMMEND)
    assert engine_rec.can_execute_compaction(act, operator_confirmed=False) is False
    assert engine_rec.can_execute_compaction(act, operator_confirmed=True) is True

    # HUMAN_REVIEW -> requires operator confirmation
    engine_hr = PolicyEngine(mode=PolicyMode.HUMAN_REVIEW)
    assert engine_hr.can_execute_compaction(act, operator_confirmed=False) is False
    assert engine_hr.can_execute_compaction(act, operator_confirmed=True) is True
