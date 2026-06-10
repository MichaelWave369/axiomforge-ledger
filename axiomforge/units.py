from dataclasses import dataclass
import re

BASE=('M','L','T','I','Th','N','J')
@dataclass(frozen=True)
class Dim:
    vec: tuple
    def __mul__(self,o): return Dim(tuple(a+b for a,b in zip(self.vec,o.vec)))
    def __truediv__(self,o): return Dim(tuple(a-b for a,b in zip(self.vec,o.vec)))
    def __pow__(self,k): return Dim(tuple(a*k for a in self.vec))
    def __str__(self):
        return ' '.join(f'{b}^{e:g}' for b,e in zip(BASE,self.vec) if e) or 'dimensionless'

def _d(**kw): return Dim(tuple(float(kw.get(b,0)) for b in BASE))
DIMENSIONLESS=_d()
UNIT={'kg':_d(M=1),'g':_d(M=1),'m':_d(L=1),'s':_d(T=1),'n':_d(M=1,L=1,T=-2),'j':_d(M=1,L=2,T=-2),'w':_d(M=1,L=2,T=-3),'hz':_d(T=-1),'1':DIMENSIONLESS,'':DIMENSIONLESS}

def parse_unit(unit: str):
    u=unit.strip().replace(' ','*')
    if not u: return DIMENSIONLESS
    dim=DIMENSIONLESS
    for i,chunk in enumerate(u.split('/')):
        cd=DIMENSIONLESS
        for factor in filter(None,chunk.split('*')):
            m=re.fullmatch(r'([A-Za-z]+)(?:\^(-?\d+))?', factor)
            if not m: raise ValueError(f'bad unit {factor}')
            sym=m.group(1).lower(); exp=float(m.group(2) or 1)
            if sym not in UNIT: raise ValueError(f'unknown unit symbol {m.group(1)}')
            cd=cd*(UNIT[sym]**exp)
        dim=dim*cd if i==0 else dim/cd
    return dim

def _var_dims(vars): return {k:parse_unit(v.get('unit','')) for k,v in vars.items() if v.get('unit')}
def _eval(expr, dims):
    expr=expr.replace('^','**').strip()
    expr=re.sub(r'(?<=[A-Za-z\)])\s+(?=[A-Za-z\(])','*',expr)
    for name,dim in dims.items(): expr=re.sub(rf'\b{name}\b', f'dims[{name!r}]', expr)
    return eval(expr, {'__builtins__':{}}, {'dims':dims})

def check_equation(equation, variables):
    out={'equation':equation,'checked':False,'passed':None,'detail':''}
    try:
        lhs,rhs=equation.split('=',1); dims=_var_dims(variables); L=_eval(lhs,dims); R=_eval(rhs,dims)
        out.update({'checked':True,'passed':L==R,'detail':f'LHS [{L}] {"==" if L==R else "!="} RHS [{R}]' + ('' if L==R else ' — unit mismatch')})
    except Exception as e: out['detail']=f'could not complete dimensional check: {e}'
    return out

def check_claim_units(parsed):
    if not parsed.equations or not parsed.variables: return {'applicable':False,'results':[],'all_passed':None,'note':'not applicable'}
    results=[check_equation(e, parsed.variables) for e in parsed.equations]
    checked=[r for r in results if r['checked']]
    return {'applicable':True,'results':results,'all_passed': all(r['passed'] for r in checked) if checked else None,'note':'necessary, not sufficient'}
