from dataclasses import dataclass, field
import re

_METAPHOR_MARKERS = ['standing wave of', 'universal resonance', 'is like', 'sacred', 'vibration']
_WORD_UNITS = {'joules':'J','joule':'J','newtons':'N','newton':'N','kilograms':'kg','kilogram':'kg','meters per second':'m/s','metres per second':'m/s','meters':'m','meter':'m','seconds':'s','second':'s'}

@dataclass
class ParsedClaim:
    original_text: str
    definitions: list = field(default_factory=list)
    assumptions: list = field(default_factory=list)
    variables: dict = field(default_factory=dict)
    relationships: list = field(default_factory=list)
    equations: list = field(default_factory=list)
    quantifiers: list = field(default_factory=list)
    testability: str = 'unknown'
    testability_rationale: str = ''
    parser_confidence: str = 'heuristic parse; human review advised'
    def to_dict(self):
        return self.__dict__.copy()

def _unit(u):
    u = u.strip().lower()
    return _WORD_UNITS.get(u, u if u != 'joules' else 'J')

def parse_claim(text: str) -> ParsedClaim:
    text = text.strip()
    p = ParsedClaim(text)
    for m in re.finditer(r'([A-Za-z]\w*)\s+is\s+(?:the\s+)?([\w\s]{1,50}?)\s+in\s+([A-Za-z][\w/\^\s]*?)(?=[,.;]|$|\s+and\b)', text, re.I):
        p.variables[m.group(1)] = {'description': m.group(2).strip(), 'unit': _unit(m.group(3))}
    for m in re.finditer(r'([A-Za-z]\w*\s*=\s*[A-Za-z0-9_\s\*\+/\-\^\.]+?)(?=[,.;]|$|\s+where\b)', text):
        p.equations.append(m.group(1).strip())
    for m in re.finditer(r'if\s+(.+?)\s*,?\s*then\s+(.+?)(?:[.;]|$)', text, re.I):
        p.relationships.append({'kind':'implies','terms':[m.group(1).strip(), m.group(2).strip()]})
    for q in re.findall(r'\b(all|every|any|always|never)\b', text, re.I):
        p.quantifiers.append(q.lower())
    for m in re.finditer(r'\b(?:assuming|given that|suppose(?: that)?)\s+([^.;]+)', text, re.I):
        p.assumptions.append(m.group(1).strip())
    t = text.lower()
    if any(x in t for x in _METAPHOR_MARKERS):
        p.testability, p.testability_rationale = 'none', 'metaphorical language without operational definitions'
    elif any(x in t for x in ['integer','prime','even','odd','square','sum','product']):
        p.testability, p.testability_rationale = 'formal', 'mathematical objects detected'
    elif any(x in t for x in ['network','entropy','coherence','perturbation','noise','drift']):
        p.testability, p.testability_rationale = 'simulation', 'dynamic system behavior detected'
    elif p.variables or p.equations or any(x in t for x in ['energy','mass','force','velocity']):
        p.testability, p.testability_rationale = 'empirical', 'physical quantities detected'
    if p.quantifiers:
        p.assumptions.append('universal quantifier taken at face value over the natural domain')
    if p.variables:
        p.assumptions.append('stated units are correct and quantities are classical point values')
    if p.equations:
        p.assumptions.append('equation symbols refer to parsed variables')
    if not p.assumptions:
        p.assumptions.append('no explicit assumptions stated; claim read literally as written')
    return p
