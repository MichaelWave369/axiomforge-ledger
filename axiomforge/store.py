import json, os, sqlite3
DEFAULT_DB=os.environ.get('AXIOMFORGE_DB', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'ledger.db'))
_SCHEMA='''CREATE TABLE IF NOT EXISTS receipts(claim_id TEXT PRIMARY KEY, created_at TEXT, status TEXT, body TEXT);CREATE TABLE IF NOT EXISTS assumptions(assumption_id TEXT PRIMARY KEY, claim_id TEXT, text TEXT, downstream_status TEXT);'''
class Store:
    def __init__(self,path=DEFAULT_DB):
        os.makedirs(os.path.dirname(path), exist_ok=True); self.path=path
        with self._conn() as c: c.executescript(_SCHEMA)
    def _conn(self):
        c=sqlite3.connect(self.path); c.row_factory=sqlite3.Row; return c
    def save_receipt(self,r,assumption_rows):
        with self._conn() as c:
            c.execute('INSERT OR REPLACE INTO receipts VALUES (?,?,?,?)',(r['claim_id'],r['timestamp'],r['current_status'],json.dumps(r)))
            c.execute('DELETE FROM assumptions WHERE claim_id=?',(r['claim_id'],))
            c.executemany('INSERT INTO assumptions VALUES (?,?,?,?)',[(a['assumption_id'],a['claim_id'],a['text'],a['downstream_status']) for a in assumption_rows])
    def get_receipt(self,claim_id):
        with self._conn() as c: row=c.execute('SELECT body FROM receipts WHERE claim_id=?',(claim_id,)).fetchone()
        return json.loads(row['body']) if row else None
    def list_receipts(self):
        with self._conn() as c: rows=c.execute('SELECT body FROM receipts ORDER BY created_at').fetchall()
        return [json.loads(r['body']) for r in rows]
    def list_assumptions(self):
        with self._conn() as c: rows=c.execute('SELECT * FROM assumptions ORDER BY claim_id').fetchall()
        return [dict(r) for r in rows]
