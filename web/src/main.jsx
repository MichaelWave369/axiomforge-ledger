import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const REPO = 'https://github.com/MichaelWave369/axiomforge-ledger';
const EXAMPLES = [
  ['Parity invariant', 'The sum of two even integers is even.', 'Mathematics', 'Formalizable theorem candidate'],
  ['Prime universal', 'All prime numbers are odd.', 'Mathematics', 'Counterexample: 2'],
  ['Mass-energy relation', 'E = m * c^2, where E is energy in joules, m is mass in kg, and c is the speed of light in m/s.', 'Physics', 'Units alone are not proof'],
  ['Force equation', 'F = m * v, where F is force in N, m is mass in kg, and v is velocity in m/s.', 'Physics', 'Potential dimensional mismatch'],
  ['Noisy network', 'In an information network with noisy copying, entropy of node states drifts upward over time as noise accumulates.', 'Systems', 'Simulation candidate'],
  ['Constraint coherence', 'Systems that maintain constraint coherence degrade more slowly than unconstrained systems under identical random perturbation.', 'Systems', 'Simulation candidate'],
  ['Universal resonance', 'Consciousness is a standing wave of universal resonance.', 'Metaphor', 'Requires an operational definition']
];
const STAGES = [
  ['01', 'Intake', 'Read the words, quantifiers, equations, and declared assumptions.'],
  ['02', 'Classification', 'Route theorem, empirical, simulation, and metaphor candidates.'],
  ['03', 'Formalization', 'Attempt structure without inventing a machine proof.'],
  ['04', 'Units', 'Check dimensional consistency when applicable.'],
  ['05', 'Counterexamples', 'Search for falsifying cases and disclose test scope.'],
  ['06', 'Simulation', 'Record model-specific findings with reproducible seeds.'],
  ['07', 'Receipt', 'Attach assumptions, outcomes, notes, UTC time, and SHA-256.']
];

function preview(text) {
  const t = text.trim().toLowerCase();
  if (!t) return null;
  const metaphor = ['standing wave of','universal resonance','is like','sacred','vibration'].some(x => t.includes(x));
  const formal = ['integer','prime','even','odd','square','sum','product'].some(x => t.includes(x));
  const simulation = ['network','entropy','coherence','perturbation','noise','drift'].some(x => t.includes(x));
  const equation = /[a-z]\w*\s*=\s*[a-z0-9_]/i.test(text);
  const empirical = equation || ['energy','mass','force','velocity'].some(x => t.includes(x));
  let category = 'Unclassified', label = 'unsupported_claim', reason = 'No supported classification cue found.';
  if (metaphor) { category='Metaphor'; label='metaphor'; reason='Figurative language without a defined operational test.'; }
  else if (formal) { category='Formal'; label='theorem_candidate'; reason='Mathematical structure detected by keyword heuristic.'; }
  else if (simulation) { category='Simulation'; label='simulation_candidate'; reason='Dynamic systems language detected.'; }
  else if (empirical) { category='Empirical'; label='empirical_hypothesis'; reason='Equation or measurable quantity detected.'; }
  const assumptions = [];
  const explicit = text.match(/\b(?:assuming|given that|suppose(?: that)?)\s+([^.;]+)/i);
  if (explicit) assumptions.push(explicit[1].trim());
  if (/\b(all|every|any|always|never)\b/i.test(text)) assumptions.push('Universal quantifiers must be interpreted over an explicit domain.');
  if (equation) assumptions.push('Symbols and units must be defined before checking the equation.');
  if (!assumptions.length) assumptions.push('No assumptions supplied; literal interpretation requires review.');
  return { category, label, reason, assumptions };
}
function Status({value}) {
  const s = String(value || 'unknown');
  const bad = s === 'falsified_by_counterexample' || s === 'blocked_unit_mismatch';
  const good = s === 'proven';
  const caution = s === 'not_falsified_in_this_test';
  return <span className={'status ' + (bad?'bad':good?'good':caution?'caution':'')}>{s.replaceAll('_',' ')}</span>;
}
function App() {
  const [tab,setTab]=useState('workbench');
  const [claim,setClaim]=useState(EXAMPLES[1][1]);
  const [previewed,setPreviewed]=useState(false);
  const [receipts,setReceipts]=useState([]);
  const [filename,setFilename]=useState('');
  const [error,setError]=useState('');
  const [query,setQuery]=useState('');
  const [status,setStatus]=useState('all');
  const [selectedId,setSelectedId]=useState('');
  const info=useMemo(()=>preview(claim),[claim]);
  const statuses=useMemo(()=>[...new Set(receipts.map(r=>r.current_status||'unknown'))].sort(),[receipts]);
  const visible=useMemo(()=>receipts.filter(r=>(status==='all'||r.current_status===status)&&
    (String(r.original_claim||'').toLowerCase().includes(query.toLowerCase())||String(r.claim_id||'').toLowerCase().includes(query.toLowerCase()))),
    [receipts,status,query]);
  const selected=visible.find(r=>r.claim_id===selectedId)||visible[0];

  async function importJson(event) {
    const file=event.target.files?.[0];
    if(!file)return;
    setError('');
    try {
      if(file.size>5*1024*1024)throw new Error('Select a JSON file smaller than 5 MB.');
      const obj=JSON.parse(await file.text());
      const rows=Array.isArray(obj)?obj:obj?.receipts;
      if(!Array.isArray(rows)||!rows.every(r=>r&&typeof r==='object'&&!Array.isArray(r)&&typeof r.original_claim==='string')){
        throw new Error('Expected an array of receipts or an export object containing a receipts array.');
      }
      setReceipts(rows);setFilename(file.name);setSelectedId('');setQuery('');setStatus('all');setTab('ledger');
    }catch(e){setError(e instanceof Error?e.message:'Invalid file');}
    finally{event.target.value='';}
  }
  function openExample(text){setClaim(text);setPreviewed(false);setTab('workbench');}
  function clearImport(){setReceipts([]);setFilename('');setQuery('');setStatus('all');setSelectedId('');}

  return <div className="shell">
    <div className="topline"><span><i className="indicator"/> FIELD RESEARCH / AXIOMFORGE</span><span>PUBLIC CONSOLE · V0.1</span></div>
    <header className="hero">
      <div className="hero-copy">
        <p className="eyebrow">RECEIPT-FIRST CLAIM RESEARCH</p>
        <h1>AXIOM<span>FORGE</span><br/>LEDGER<span className="period">.</span></h1>
        <p className="lead">Ideas are welcome. Evidence gets a receipt. Every conclusion keeps its assumptions attached.</p>
      </div>
      <div className="hero-art" aria-hidden="true"><div className="rings"><div className="core">∴</div></div><small>NO PROOF WITHOUT VERIFICATION</small></div>
    </header>
    <div className="notice"><strong>STATIC RESEARCH EXPLORER</strong><span>Browser preview only. This site does not run the Python engine, database, simulations, or proof backend.</span></div>
    <nav className="nav" aria-label="Research sections">
      {[['workbench','01 / Workbench'],['ledger','02 / Receipt Ledger'],['method','03 / Method']].map(([id,name])=>
        <button key={id} onClick={()=>setTab(id)} className={tab===id?'active':''} aria-current={tab===id?'page':undefined}>{name}</button>
      )}
      <a href={REPO} target="_blank" rel="noreferrer">SOURCE ↗</a>
    </nav>
    {tab==='workbench'&&<main className="content">
      <div className="sectionline"><span>01 / CLAIM INTAKE</span><span>LOCAL HEURISTIC · NOT A TEST</span></div>
      <div className="columns">
        <section className="panel">
          <div className="panelhead"><span>CLAIM EDITOR</span><small>INPUT / 001</small></div>
          <label htmlFor="claim">State a testable claim or candidate hypothesis</label>
          <textarea id="claim" value={claim} maxLength={3000} onChange={e=>{setClaim(e.target.value);setPreviewed(false);}} placeholder="Write a claim to explore..."/>
          <div className="editorfooter"><small>{claim.length} / 3000 CHARACTERS</small><button className="primary" disabled={!claim.trim()} onClick={()=>setPreviewed(true)}>PREVIEW CLASSIFICATION ↗</button></div>
          <p className="muted">A non-authoritative, local preview. Nothing is submitted, tested, proved, saved to a ledger, or sent to a server.</p>
        </section>
        <section className="panel result">
          <div className="panelhead"><span>INSPECTION PANEL</span><small>{previewed?'PREVIEW READY':'AWAITING PREVIEW'}</small></div>
          {previewed&&info?<div>
            <div className="resulttitle"><div><small className="eyebrow">CANDIDATE ROUTE</small><h2>{info.category}</h2></div><span className="stamp">HEURISTIC ONLY</span></div>
            <div className="readout"><span>CLASSIFICATION LABEL</span><code>{info.label}</code></div>
            <p className="muted">{info.reason}</p>
            <div className="subheading">ASSUMPTION PROMPTS <span>{info.assumptions.length}</span></div>
            {info.assumptions.map((a,i)=><p className="assumption" key={i}><b>A{i+1}</b>{a}</p>)}
            <p className="warning">No counterexample search, unit check, simulation, or formal proof performed. Status: <b>NOT EVALUATED</b>.</p>
          </div>:<div className="pending"><span>⌁</span><h2>Nothing asserted yet.</h2><p>Choose an example or enter a claim, then preview its likely intake category.</p></div>}
        </section>
      </div>
      <div className="sectionline space"><span>REFERENCE CLAIMS / PROJECT EXAMPLES</span><span>07 CASES</span></div>
      <div className="examples">{EXAMPLES.map(([name,text,family,note],i)=>
        <button key={name} className="example" onClick={()=>openExample(text)}>
          <div className="examplehead"><span>{String(i+1).padStart(2,'0')} · {family.toUpperCase()}</span><span>↗</span></div>
          <h3>{name}</h3><p>{text}</p><small>{note}</small>
        </button>)}</div>
    </main>}
    {tab==='ledger'&&<main className="content">
      <div className="sectionline"><span>02 / RECEIPT LEDGER</span><span>LOCAL JSON VIEWER</span></div>
      <div className="panel importer"><div><h2>Inspect real research receipts.</h2><p>Import a JSON file from the Python backend's <code>/api/export/json</code> endpoint. Files remain in this browser and are not uploaded.</p></div><div className="importactions">
        <label className="filebutton">IMPORT JSON<input type="file" accept=".json,application/json" onChange={importJson}/></label>
        {!!receipts.length&&<button className="outline" onClick={clearImport}>CLEAR</button>}
      </div></div>
      {!!error&&<p className="error" role="alert">{error}</p>}
      <div className="stats"><div><small>RECEIPTS LOADED</small><strong>{receipts.length}</strong></div><div><small>STATUS TYPES</small><strong>{statuses.length}</strong></div><div><small>LOCAL DATA SOURCE</small><strong className="filename">{filename||'NONE'}</strong></div></div>
      {receipts.length>0?<div className="columns ledgercols">
        <section className="panel"><div className="panelhead"><span>RECORDED CLAIMS</span><small>{visible.length} MATCHES</small></div>
          <input className="field" value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search receipt or claim..." aria-label="Search receipts"/>
          <select className="field" value={status} onChange={e=>setStatus(e.target.value)} aria-label="Filter receipts by status"><option value="all">ALL STATUSES</option>{statuses.map(s=><option key={s} value={s}>{s.replaceAll('_',' ')}</option>)}</select>
          <div className="recordlist">{visible.length?visible.map((r,i)=><button className={selected===r?'record selected':'record'} key={r.claim_id||i} onClick={()=>setSelectedId(r.claim_id)}>
            <small>{r.claim_id||'UNIDENTIFIED'}</small><span>{r.original_claim}</span><Status value={r.current_status}/>
          </button>):<p className="muted">No matching records.</p>}</div>
        </section>
        <section className="panel detail"><div className="panelhead"><span>RECEIPT DETAIL</span><small>IMPORTED / UNVERIFIED</small></div>
          {selected?<><small className="eyebrow">RESEARCH CLAIM</small><h2>{selected.original_claim}</h2><Status value={selected.current_status}/>
            <div className="subheading">ASSUMPTION CHAIN</div>
            {Array.isArray(selected.assumptions)&&selected.assumptions.length?selected.assumptions.map((a,i)=><p key={i} className="assumption"><b>A{i+1}</b>{String(a)}</p>):<p className="warning">No assumption chain in imported record.</p>}
            <div className="readout"><span>CLASSIFICATION</span><code>{Array.isArray(selected.classification?.labels)?selected.classification.labels.join(', ')||'none recorded':'not supplied'}</code></div>
            <div className="readout"><span>RECORDED TIMESTAMP</span><code>{selected.timestamp||'not supplied'}</code></div>
            <div className="readout"><span>RECORDED SHA-256 (NOT VERIFIED)</span><code className="hash">{selected.receipt_sha256||'not supplied'}</code></div>
            {Array.isArray(selected.confidence_notes)&&selected.confidence_notes.length>0&&<><div className="subheading">CONFIDENCE NOTES</div>{selected.confidence_notes.map((n,i)=><p className="muted" key={i}>{String(n)}</p>)}</>}
            <p className="warning">This browser only displays the claimed hash. Use the Python receipt verification endpoint for an actual integrity check.</p>
          </>:<p className="muted">Select a receipt to inspect its assumptions.</p>}
        </section>
      </div>:<div className="empty"><span>◇</span><h3>No receipts imported.</h3><p>Example claims are not fabricated receipts. Run the backend, export real receipts, and inspect them here.</p><a href={REPO+'#run-the-python-workbench'} target="_blank" rel="noreferrer">HOW TO RUN THE BACKEND ↗</a></div>}
    </main>}
    {tab==='method'&&<main className="content">
      <div className="sectionline"><span>03 / EVIDENCE PIPELINE</span><span>GOVERNED BY DISCLOSED LIMITS</span></div>
      <section className="methodhero"><p className="eyebrow">THE DISCIPLINE CONTRACT</p><h2>Evidence before elevation.</h2><p>AxiomForge evaluates claims without confusing plausibility, a passing test, and machine-verified proof. Every conclusion must stay attached to its assumptions.</p></section>
      <div className="stages">{STAGES.map(([n,title,note])=><div className="stage" key={n}><small>{n}</small><h3>{title}</h3><p>{note}</p></div>)}</div>
      <div className="principles">
        <div><small>01 / PROOF DISCIPLINE</small><h3>Stub ≠ proof</h3><p>The included Lean adapter is a stub. It cannot establish proven status.</p></div>
        <div><small>02 / FALSIFIABILITY</small><h3>A counterexample matters</h3><p>A falsifying instance refutes a universal claim. Not finding one is not proof.</p></div>
        <div><small>03 / PROVENANCE</small><h3>Assumptions stay visible</h3><p>Evidence, notes, timestamps and hashes are attached to receipts. A hash is not a signature.</p></div>
      </div>
      <div className="methodend"><p>Explore the real source code and tests. This static site explains the workflow; it does not replace it.</p><a className="primary" href={REPO+'/tree/main/axiomforge'} target="_blank" rel="noreferrer">INSPECT PYTHON SOURCE ↗</a></div>
    </main>}
    <footer><span>AXIOMFORGE LEDGER / OPEN RESEARCH</span><div><a href={REPO} target="_blank" rel="noreferrer">GITHUB ↗</a><a href={REPO+'/blob/main/LICENSE'} target="_blank" rel="noreferrer">MIT LICENSE ↗</a></div><span>VERIFY · DOCUMENT · REVISE</span></footer>
  </div>;
}
createRoot(document.getElementById('root')).render(<App/>);
