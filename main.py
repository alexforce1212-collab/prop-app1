from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

props = [
    {"player":"【entity-Jalen Brunson¦canonical_name=Jalen Brunson】","prop":"Points","line":24.5,"proj":27.1,"pick":"OVER","edge":"10.6%","conf":"HIGH"},
    {"player":"【entity-Josh Allen¦canonical_name=Josh Allen】","prop":"Pass Yds","line":247.5,"proj":268.3,"pick":"OVER","edge":"8.4%","conf":"HIGH"},
    {"player":"【entity-Justin Jefferson¦canonical_name=Justin Jefferson】","prop":"Rec Yds","line":89.5,"proj":78.2,"pick":"UNDER","edge":"12.6%","conf":"MED"},
]

HTML = """
<html><head><style>
body{background:#0f1115;color:white;font-family:sans-serif;padding:20px}
table{width:100%;border-collapse:collapse;margin-top:20px}
th{color:#888;text-align:left;padding:10px}
td{padding:12px;border-bottom:1px solid #222}
.over{color:#00ff88;font-weight:bold}
.under{color:#ff4d4d;font-weight:bold}
</style></head><body>
<h1 style="color:#00ff88">PROP FINDER - 15-20 Safest</h1>
<table><tr><th>Player</th><th>Prop</th><th>Line</th><th>Projection</th><th>Pick</th><th>Edge</th><th>Conf</th></tr>
ROWS
</table></body></html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    rows = "".join([f"<tr><td>{p['player']}</td><td>{p['prop']}</td><td>{p['line']}</td><td>{p['proj']}</td><td class='{p['pick'].lower()}'>{p['pick']}</td><td>{p['edge']}</td><td>{p['conf']}</td></tr>" for p in props])
    return HTML.replace("ROWS", rows)

@app.get("/api/props")
def api(): return props
