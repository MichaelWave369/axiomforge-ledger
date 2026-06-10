import hashlib, json, uuid
from datetime import datetime, timezone

class MissingAssumptionsError(RuntimeError): pass

def _canonical(obj): return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
def compute_hash(receipt): return hashlib.sha256(_canonical({k:v for k,v in receipt.items() if k!='receipt_sha256'}).encode()).hexdigest()
def verify_receipt(receipt): return receipt.get('receipt_sha256') == compute_hash(receipt)

def build_receipt(*, original_claim, parsed_claim, assumptions, classification, formalization, lean_result, units_check, counterexample_report, simulation_results, status, confidence_notes, claim_id=None):
    if not assumptions: raise MissingAssumptionsError('empty assumption chain refused')
    r={'claim_id':claim_id or 'AXF-'+uuid.uuid4().hex[:12], 'original_claim':original_claim, 'parsed_claim':parsed_claim, 'assumptions':assumptions, 'classification':classification, 'formalization_attempt':formalization, 'lean_result':lean_result, 'units_check':units_check, 'counterexample_attempts':counterexample_report, 'simulation_results':simulation_results, 'current_status':status.value if hasattr(status,'value') else status, 'confidence_notes':confidence_notes, 'timestamp':datetime.now(timezone.utc).isoformat(), 'schema_version':'1.0'}
    r['receipt_sha256']=compute_hash(r); return r

def render_conclusion(r):
    if not r.get('assumptions'): raise MissingAssumptionsError('conclusion display refused without assumptions')
    return f"CLAIM {r['claim_id']}: {r['original_claim']}\nSTATUS: {r['current_status']}\nASSUMPTIONS THIS RESTS ON:\n" + '\n'.join('- '+a for a in r['assumptions'])

def receipt_to_markdown(r):
    return f"## {r['claim_id']}\n\n> {r['original_claim']}\n\n- **Status:** `{r['current_status']}`\n- **Classification:** {', '.join(r['classification'].get('labels', []))}\n- **Receipt SHA-256:** `{r['receipt_sha256']}`\n"

def assumption_entries(r):
    return [{'assumption_id':f"{r['claim_id']}-A{i+1}", 'claim_id':r['claim_id'], 'text':a, 'downstream_status':r['current_status']} for i,a in enumerate(r['assumptions'])]
