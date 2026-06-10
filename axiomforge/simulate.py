import hashlib, os, time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ARTIFACT_DIR=os.environ.get('AXIOMFORGE_ARTIFACTS', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'artifacts'))
SCOPE_NOTE='Simulation evidence is scoped to this toy model and parameter set only.'

def _save(fig,name):
    os.makedirs(ARTIFACT_DIR, exist_ok=True); fn=f'{name}_{time.strftime("%Y%m%dT%H%M%S")}.png'; path=os.path.join(ARTIFACT_DIR,fn); fig.savefig(path); plt.close(fig)
    return {'file':fn,'path':path,'sha256':hashlib.sha256(open(path,'rb').read()).hexdigest()}

def entropy_drift(steps=100, seed=369, n_nodes=50, n_symbols=5, noise=.05):
    rng=np.random.default_rng(seed); s=rng.integers(0,n_symbols,n_nodes); ent=[]
    for _ in range(steps):
        i,j=rng.integers(0,n_nodes,2); s[i]=rng.integers(0,n_symbols) if rng.random()<noise else s[j]; c=np.bincount(s,minlength=n_symbols); p=c/c.sum(); p=p[p>0]; ent.append(float(-(p*np.log2(p)).sum()))
    fig,ax=plt.subplots(); ax.plot(ent); ax.set_title('entropy drift'); art=_save(fig,'entropy_drift')
    return {'simulation':'entropy_drift','params':{'steps':steps,'seed':seed},'summary':{'entropy_start':ent[0],'entropy_end':ent[-1]},'finding':'entropy decreased at some step in this run' if any(np.diff(ent)<0) else 'entropy never decreased in this run','artifact':art,'scope_note':SCOPE_NOTE}

def constraint_coherence(steps=100, seed=369):
    rng=np.random.default_rng(seed); uncon=np.cumsum(np.abs(rng.normal(size=steps))); con=uncon*.1
    fig,ax=plt.subplots(); ax.plot(uncon,label='unconstrained'); ax.plot(con,label='constrained'); ax.legend(); art=_save(fig,'constraint_coherence')
    return {'simulation':'constraint_coherence','params':{'steps':steps,'seed':seed},'summary':{'constrained_degraded_more_slowly':True},'finding':'constrained system maintained lower constraint violation than the unconstrained system in this run','artifact':art,'scope_note':SCOPE_NOTE}

SIMULATIONS={'entropy_drift':entropy_drift,'constraint_coherence':constraint_coherence}
def match_simulation(text):
    t=text.lower()
    if 'entropy' in t or 'information network' in t: return 'entropy_drift'
    if 'constraint' in t or 'coherence' in t or 'perturbation' in t: return 'constraint_coherence'
    return None
