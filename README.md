# AxiomForge Ledger

Receipt-first math, physics, and systems-theory claim workbench.

AxiomForge converts natural-language claims into structured receipts with assumptions, classifications, formalization attempts, unit checks, counterexample sweeps, simulations, confidence notes, timestamps, and tamper-evident hashes.

**React GitHub Pages:** https://michaelwave369.github.io/axiomforge-ledger/ (available after enabling Pages via Actions and merging the frontend PR).

## Discipline contract

- Machine proof is unreachable with the bundled stub prover.
- Counterexamples downgrade claims to falsified_by_counterexample.
- Surviving a sweep/simulation means not_falsified_in_this_test, not proof.
- Unit mismatches block physics claims from being marked proven.
- Metaphors are never dressed up as math.
- Receipts require assumption chains.

## Run the Python workbench

    pip install -r requirements.txt
    python scripts/load_samples.py
    uvicorn axiomforge.app:app --reload --port 8369

Open http://127.0.0.1:8369.

## Run the React site

    cd web
    npm install
    npm run dev

The public site is a static, browser-only companion, not the FastAPI runtime. Visitors can view example claims, preview a non-authoritative heuristic classification, read the methodology, and inspect locally imported receipts. The site cannot run the Python proof attempts, simulations, counterexample searches, unit checks or create verified receipts.

To inspect real receipts, start the Python backend and save the response from GET http://127.0.0.1:8369/api/export/json as a JSON file, then import it on the public site's Ledger panel. Files stay in the browser, and the website does not verify SHA-256 hashes. For verification, use the backend's /api/claims/{claim_id}/verify endpoint.

### Publish using GitHub Actions

1. Merge the website PR into main.
2. Select Settings → Pages → Build and deployment → Source: GitHub Actions.
3. The pages.yml workflow will build and deploy the Vite site on pushes affecting web/.
4. Open https://michaelwave369.github.io/axiomforge-ledger/ after the deployment completes.

The Vite base path is /axiomforge-ledger/ to support project GitHub Pages.

## Tests

    python -m pytest tests -q
    cd web
    npm install
    npm run build

## Recovery note

This repo was initialized from the recovered AxiomForge Ledger project materials. Runtime files such as data/ledger.db, simulation plots, __pycache__, and pytest cache are intentionally excluded.

## License

MIT, see [LICENSE](LICENSE).
