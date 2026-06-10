#!/usr/bin/env python3
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from axiomforge.pipeline import process_claim
from axiomforge.store import Store

def main():
    path=os.path.join(os.path.dirname(__file__),'..','samples','claims.json')
    samples=json.load(open(path, encoding='utf-8'))['claims']; store=Store()
    for s in samples:
        r=process_claim(s['text'], store=store, run_simulations=True)
        print(f"{r['claim_id']} [{r['current_status']}] {s['text'][:70]}")
    print(f"\n{len(samples)} sample claims loaded into {store.path}")
if __name__=='__main__': main()
