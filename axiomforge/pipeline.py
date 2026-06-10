from . import intake, classify as classify_mod, formalize, lean_stub, units, counterexample, simulate
from .receipts import build_receipt, assumption_entries
from .status import Status, downgrade, can_mark_proven

def process_claim(text, store=None, run_simulations=True, seed=369):
    parsed=intake.parse_claim(text); existing=store.list_receipts() if store else []
    classification=classify_mod.classify(parsed, existing); form=formalize.formalize(parsed); lean=lean_stub.attempt_proof(form); unit=units.check_claim_units(parsed); ce=counterexample.search_counterexamples(parsed, seed); sims=[]
    if run_simulations and 'simulation_candidate' in classification['labels']:
        name=simulate.match_simulation(text)
        if name: sims.append(simulate.SIMULATIONS[name](seed=seed))
    status,notes=_decide_status(classification,form,lean,unit,ce,sims)
    r=build_receipt(original_claim=text, parsed_claim=parsed.to_dict(), assumptions=parsed.assumptions, classification=classification, formalization=form, lean_result=lean, units_check=unit, counterexample_report=ce, simulation_results=sims, status=status, confidence_notes=notes)
    if store: store.save_receipt(r, assumption_entries(r))
    return r

def _decide_status(classification, form, lean, unit, ce, sims):
    notes=[]; status=Status.UNTESTED; evidence=False
    if ce.get('performed'):
        evidence=True
        if ce.get('counterexample_found'):
            return Status.FALSIFIED, ['counterexample found; terminal downgrade']
        status=Status.NOT_FALSIFIED_IN_TEST; notes.append('counterexample sweep found none; not proof')
    if unit.get('applicable'):
        if unit.get('all_passed') is False: return downgrade(status, Status.BLOCKED_UNIT_MISMATCH), ['unit mismatch blocks proof']
        if unit.get('all_passed') is True: notes.append('units pass; necessary, not sufficient')
    if sims:
        evidence=True; status = status if status != Status.UNTESTED else Status.NOT_FALSIFIED_IN_TEST
        notes += [f"simulation {s['simulation']}: {s['finding']}. {s['scope_note']}" for s in sims]
        if any('decreased at some step' in s['finding'] or 'did NOT' in s['finding'] for s in sims): status=downgrade(status, Status.NEEDS_HUMAN_REVIEW)
    if not form.get('formalizable'):
        if 'metaphor' in classification['labels']: return downgrade(status if evidence else Status.NOT_FORMALIZABLE, Status.NOT_FORMALIZABLE), notes+['metaphor not formalized']
        if not evidence: return Status.NEEDS_HUMAN_REVIEW, notes+['not formalizable and no test ran']
    if lean.get('attempted'):
        ok,reason=can_mark_proven(proof_verified_by_backend=lean.get('verified',False), backend_is_stub=lean_stub.get_backend().is_stub, unit_check_passed=unit.get('all_passed'), counterexample_found=ce.get('counterexample_found',False))
        notes.append('proven withheld: '+reason)
        if not evidence: status=Status.PROOF_ATTEMPTED_FAILED
    if status==Status.UNTESTED: notes.append('no executable proof/test/simulation applied')
    return status, notes
