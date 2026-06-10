from axiomforge.pipeline import process_claim
from axiomforge.status import Status, can_mark_proven
from axiomforge.receipts import verify_receipt
from axiomforge.units import check_equation


def test_counterexample_falsifies():
    r=process_claim('All prime numbers are odd.', run_simulations=False)
    assert r['current_status']==Status.FALSIFIED.value
    assert r['counterexample_attempts']['counterexample_found'] is True


def test_surviving_sweep_not_proven():
    r=process_claim('The sum of two even integers is even.', run_simulations=False)
    assert r['current_status'] != Status.PROVEN.value
    assert r['assumptions'] and verify_receipt(r)


def test_stub_can_never_prove():
    ok, reason = can_mark_proven(proof_verified_by_backend=True, backend_is_stub=True, unit_check_passed=True, counterexample_found=False)
    assert not ok and 'stub' in reason


def test_unit_mismatch_blocks():
    r=process_claim('F = m * v, where F is force in N, m is mass in kg, and v is velocity in m/s.', run_simulations=False)
    assert r['current_status']==Status.BLOCKED_UNIT_MISMATCH.value


def test_emc2_units_pass_but_not_proven():
    r=process_claim('E = m * c^2, where E is energy in joules, m is mass in kg, and c is the speed of light in m/s.', run_simulations=False)
    assert r['units_check']['all_passed'] is True
    assert r['current_status'] != Status.PROVEN.value


def test_metaphor_not_formalizable():
    r=process_claim('Consciousness is a standing wave of universal resonance.', run_simulations=False)
    assert r['current_status']==Status.NOT_FORMALIZABLE.value


def test_unit_checker_direct():
    res=check_equation('E = m * c^2', {'E':{'unit':'J'}, 'm':{'unit':'kg'}, 'c':{'unit':'m/s'}})
    assert res['checked'] and res['passed'] is True
