from .status import Status

class StubLeanBackend:
    name = 'stub (no prover installed)'
    is_stub = True
    def verify(self, lean_source: str):
        return {'verified': False, 'log': 'Stub backend: source was not checked; no proof is granted.'}

_backend = StubLeanBackend()

def get_backend(): return _backend

def set_backend(backend):
    global _backend; _backend = backend

def attempt_proof(formalization: dict):
    if not formalization.get('formalizable'):
        return {'attempted': False, 'lean_statement': None, 'backend': _backend.name, 'verified': False, 'status': Status.NOT_FORMALIZABLE.value, 'notes': 'no formal statement available'}
    src = '-- Lean sketch only; stub backend never proves\n' + str(formalization.get('symbolic')) + '\n'
    res = _backend.verify(src)
    return {'attempted': True, 'lean_statement': src, 'backend': _backend.name, 'verified': False, 'status': Status.PROOF_ATTEMPTED_FAILED.value, 'notes': res['log']}
