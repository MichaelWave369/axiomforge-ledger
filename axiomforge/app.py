import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .pipeline import process_claim
from .store import Store
from .receipts import verify_receipt, receipt_to_markdown
from .simulate import ARTIFACT_DIR

app=FastAPI(title='AxiomForge Ledger', version='0.1.0'); store=Store(); STATIC=os.path.join(os.path.dirname(__file__),'static')
class ClaimIn(BaseModel):
    text: str; run_simulations: bool=True; seed: int=369
@app.post('/api/claims')
def create_claim(body: ClaimIn):
    if not body.text.strip(): raise HTTPException(400,'claim text is empty')
    return process_claim(body.text, store=store, run_simulations=body.run_simulations, seed=body.seed)
@app.get('/api/claims')
def list_claims(): return store.list_receipts()
@app.get('/api/claims/{claim_id}')
def get_claim(claim_id):
    r=store.get_receipt(claim_id)
    if not r: raise HTTPException(404,'no such claim')
    return r
@app.get('/api/claims/{claim_id}/verify')
def verify(claim_id):
    r=store.get_receipt(claim_id)
    if not r: raise HTTPException(404,'no such claim')
    return {'claim_id':claim_id,'hash_valid':verify_receipt(r)}
@app.get('/api/assumptions')
def assumptions(): return store.list_assumptions()
@app.get('/api/graph')
def graph():
    nodes=[]; edges=[]
    for r in store.list_receipts():
        nodes.append({'id':r['claim_id'],'type':'claim','label':r['original_claim'][:60],'status':r['current_status']})
        for i,a in enumerate(r['assumptions']):
            aid=f"{r['claim_id']}-A{i+1}"; nodes.append({'id':aid,'type':'assumption','label':a[:60]}); edges.append({'from':r['claim_id'],'to':aid,'kind':'rests_on'})
    return {'nodes':nodes,'edges':edges}
@app.get('/api/export/json')
def export_json(): return {'receipts':store.list_receipts(),'assumptions':store.list_assumptions()}
@app.get('/api/export/markdown', response_class=PlainTextResponse)
def export_markdown(): return '\n'.join(['# AxiomForge Ledger — export','']+[receipt_to_markdown(r) for r in store.list_receipts()])
@app.get('/artifacts/{name}')
def artifact(name):
    path=os.path.join(ARTIFACT_DIR, os.path.basename(name))
    if not os.path.isfile(path): raise HTTPException(404,'no such artifact')
    return FileResponse(path)
@app.get('/', response_class=HTMLResponse)
def index():
    return open(os.path.join(STATIC,'index.html'), encoding='utf-8').read()
app.mount('/static', StaticFiles(directory=STATIC), name='static')
