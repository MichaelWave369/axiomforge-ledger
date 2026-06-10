# AxiomForge Ledger

Receipt-first math, physics, and systems-theory claim workbench.

AxiomForge converts natural-language claims into structured receipts with assumptions, classifications, formalization attempts, unit checks, counterexample sweeps, simulations, confidence notes, timestamps, and tamper-evident hashes.

## Discipline contract

- `proven` is unreachable with the bundled stub prover.
- Counterexamples downgrade claims to `falsified_by_counterexample`.
- Surviving a sweep or simulation means `not_falsified_in_this_test`, not proof.
- Unit mismatches block physics claims from being marked proven.
- Metaphors are never dressed up as math.
- Receipts require assumption chains.

## Run

```bash
pip install -r requirements.txt
python scripts/load_samples.py
uvicorn axiomforge.app:app --reload --port 8369
```

Open <http://127.0.0.1:8369>.

## Tests

```bash
python -m pytest tests -q
```

## Recovery note

This repo was initialized from the recovered AxiomForge Ledger project materials. Runtime files such as `data/ledger.db`, simulation plots, `__pycache__`, and pytest cache are intentionally excluded.
