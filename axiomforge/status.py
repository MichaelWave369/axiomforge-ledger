from enum import Enum

class Status(str, Enum):
    UNTESTED = 'untested'
    NOT_FORMALIZABLE = 'not_formalizable'
    NEEDS_HUMAN_REVIEW = 'needs_human_review'
    PROOF_ATTEMPTED_FAILED = 'proof_attempted_but_failed'
    NOT_FALSIFIED_IN_TEST = 'not_falsified_in_this_test'
    BLOCKED_UNIT_MISMATCH = 'blocked_unit_mismatch'
    FALSIFIED = 'falsified_by_counterexample'
    PROVEN = 'proven'

_RANK = {Status.FALSIFIED:0, Status.BLOCKED_UNIT_MISMATCH:1, Status.NOT_FORMALIZABLE:2, Status.PROOF_ATTEMPTED_FAILED:3, Status.NEEDS_HUMAN_REVIEW:4, Status.UNTESTED:5, Status.NOT_FALSIFIED_IN_TEST:6, Status.PROVEN:7}

def downgrade(current: Status, new: Status) -> Status:
    return current if _RANK[current] <= _RANK[new] else new

def can_mark_proven(*, proof_verified_by_backend: bool, backend_is_stub: bool, unit_check_passed: bool | None, counterexample_found: bool):
    if counterexample_found:
        return False, 'a counterexample exists; claim is falsified'
    if unit_check_passed is False:
        return False, 'dimensional analysis failed; physics claim blocked'
    if backend_is_stub:
        return False, 'only the stub prover backend is configured; PROVEN requires a real machine-verified proof'
    if not proof_verified_by_backend:
        return False, 'no machine-verified proof on record'
    return True, 'machine-verified proof with consistent units and no counterexample'
