import re
from .intake import _METAPHOR_MARKERS

def formalize(parsed):
    t = parsed.original_text.lower()
    if parsed.testability == 'none' or any(m in t for m in _METAPHOR_MARKERS):
        return {'formalizable': False, 'symbolic': None, 'reason': 'metaphor or missing operational definitions; refusing to invent notation', 'caveat': 'non-formalizable here is not false'}
    patterns = [
        (r'sum of (?:any )?two even', '∀ a b : ℤ, Even a → Even b → Even (a + b)'),
        (r'all prime(?:s| numbers) are odd', '∀ p : ℕ, Prime p → Odd p'),
        (r'square of (?:any|every|a) (?:number|integer) is (?:greater|larger) than', '∀ n : ℝ, n^2 > n'),
        (r'product of two odd', '∀ a b : ℤ, Odd a → Odd b → Odd (a * b)'),
    ]
    for pat, sym in patterns:
        if re.search(pat, t):
            return {'formalizable': True, 'symbolic': sym, 'reason': 'matched known template', 'caveat': 'formalization is restatement, not evidence'}
    if parsed.equations:
        return {'formalizable': True, 'symbolic': '; '.join(parsed.equations), 'reason': 'equation carried over as written', 'caveat': 'writable equation is not proof'}
    if parsed.relationships:
        r = parsed.relationships[0]
        if r['kind'] == 'implies':
            return {'formalizable': True, 'symbolic': f"({r['terms'][0]}) → ({r['terms'][1]})", 'reason': 'if/then translated to implication', 'caveat': 'predicates are placeholders'}
    return {'formalizable': False, 'symbolic': None, 'reason': 'no mechanical formalization path detected'}
