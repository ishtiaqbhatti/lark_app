from typing import Dict, Set

# Defines the valid states an opportunity can transition *to* from a given state.
VALID_TRANSITIONS: Dict[str, Set[str]] = {
    'review': {'validated', 'rejected', 'running', 'in_progress'},
    'validated': {'analyzed', 'paused_for_approval', 'running', 'in_progress', 'rejected'},
    'analyzed': {'running', 'in_progress', 'generated', 'rejected'},
    'paused_for_approval': {'running', 'in_progress', 'generated', 'rejected'},
    'failed': {'running', 'in_progress', 'validated', 'rejected'},
    'rejected': {'validated', 'pending'}, # From manual override
    'generated': {'published', 'rejected'},
}

def is_valid_transition(from_status: str, to_status: str) -> bool:
    """Checks if a state transition is allowed."""
    return to_status in VALID_TRANSITIONS.get(from_status, set())
