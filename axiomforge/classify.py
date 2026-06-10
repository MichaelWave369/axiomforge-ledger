from .intake import _METAPHOR_MARKERS

def classify(parsed, existing_claims=None):
    t = parsed.original_text.lower(); labels = {}
    if parsed.testability == 'formal': labels['theorem_candidate'] = 'formal/math structure detected'
    if parsed.testability == 'simulation': labels['simulation_candidate'] = 'system dynamics detected'
    if parsed.testability == 'empirical': labels['empirical_hypothesis'] = 'measurable physical quantities detected'
    if parsed.testability == 'none' or any(m in t for m in _METAPHOR_MARKERS): labels['metaphor'] = 'figurative language or no operational test path'
    if existing_claims:
        words = set(w for w in t.split() if len(w) > 4)
        for other in existing_claims:
            ot = other.get('original_claim','').lower()
            if len(words & set(ot.split())) >= 2 and (('always' in t and 'never' in ot) or ('never' in t and 'always' in ot)):
                labels['contradiction_candidate'] = f"possible tension with existing claim {other.get('claim_id','?')}"
                break
    if not labels: labels['unsupported_claim'] = 'no classification rule matched'
    return {'labels': sorted(labels), 'reasons': labels}
