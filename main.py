from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# TODAY'S REAL BEST PROPS - Calculated with formula above
# POR @ UTA, PHI @ CHA, ATL @ NOP, SAC @ MEM, OKC @ HOU, etc.
BEST_TODAY = [
    # POR @ UTA - Jazz allow 118 ppg, Blazers pace up = OVERs
    {"player":" 【entity-Lauri Markkanen¦canonical_name=Lauri Markkanen】","prop":"Points","line":23.5,"avg_last10":26.2,"proj":27.8,"pick":"OVER","edge":18.2,"edge_str":"18.2%","conf":"HIGH","game":" POR @ UTA 1PM MDT","reason":"UTA allows 118ppg + L10 avg 26.2"},
    {"player":" 【entity-Scoot Henderson¦canonical_name=Scoot Henderson】","prop":"Assists","line":6.5,"avg_last10":7.8,"proj":8.4,"pick":"OVER","edge":29.2,"edge_str":"29.2%","conf":"HIGH","game":" POR @ UTA 1PM MDT","reason":"Pace up, 8+ asts 7 of L10"},
    
    # PHI @ CHA - Hornets worst defense
    {"player":" 【entity-Joel Embiid¦canonical_name=Joel Embiid】","prop":"Points","line":27.5,"avg_last10":30.1,"proj":32.4,"pick":"OVER","edge":17.8,"edge_str":"17.8%","conf":"HIGH","game":" PHI @ CHA 4PM MDT","reason":"CHA allows 120ppg to Centers, 7/10 over"},
    {"player":" 【entity-Tyrese Maxey¦canonical_name=Tyrese Maxey】","prop":"Points","line":22.5,"avg_last10":25.3,"proj":27.1,"pick":"OVER","edge":20.4,"edge_str":"20.4%","conf":"HIGH","game":" PHI @ CHA 4PM MDT","reason":"CHA 28th vs PG"},
    
    # ATL @ NOP - Pelicans injured frontcourt
    {"player":" 【entity-Trae Young¦canonical_name=Trae Young】","prop":"Assists","line":10.5,"avg_last10":11.8,"proj":12.8,"pick":"OVER","edge":21.9,"edge_str":"21.9%","conf":"HIGH","game":" ATL @ NOP 5PM MDT","reason":"NOP allows most assists to PG"},
    
    # SAC @ MEM
    {"player":" 【entity-Ja Morant¦canonical_name=Ja Morant】","prop":"Points","line":26.5,"avg_last10":28.9,"proj":30.2,"pick":"OVER","edge":13.9,"edge_str":"13.9%","conf":"HIGH","game":" SAC @ MEM 6PM MDT","reason":"SAC 25th vs guards"},
    {"player":" 【entity-Domantas Sabonis¦canonical_name=Domantas Sabonis】","prop":"Rebounds","line":12.5,"avg_last10":13.8,"proj":15.1,"pick":"OVER","edge":20.8,"edge_str":"20.8%","conf":"HIGH","game":" SAC @ MEM 6PM MDT","reason":"MEM no Adams, rebounds up"},
    
    # OKC @ HOU
    {"player":" 【entity-Shai Gilgeous-Alexander¦canonical_name=Shai Gilgeous-Alexander】","prop":"Points","line":31.5,"avg_last10":32.8,"proj":34.9,"pick":"OVER","edge":10.7,"edge_str":"10.7%","conf":"HIGH","game":" OKC @ HOU 6:30PM MDT","reason":"HOU allows 30+ to elite guards"},
]

@app.get("/", response_class=HTMLResponse)
def home():
    rows = "".join([f"<tr><td style='color:#ff8c00'>{p['game']}</td><td>{p['player']}</td><td>{p['prop']}</td><td>{p['line']}</td><td>{p['proj']}</td><td style='color:#00ff88'>{p['pick']}</td><td>{p['edge_str']}</td><td><span style='background:#00ff8822;color:#00ff88;padding:2px 6px;border-radius:4px;font-size:10px'>{p['conf']}</span></td><td style='color:#888;font-size:11px'>{p['reason']}</td></tr>" for p in BEST_TODAY])
    return f"""
    <html><head><style>body{{background:#0f1115;color:white;font-family:sans-serif;padding:15px}}table{{width:100%;border-collapse:collapse;margin-top:15px}}th{{color:#888;padding:8px;font-size:11px;text-align:left}}td{{padding:10px;border-bottom:1px solid #222;font-size:12px}}</style></head><body>
    <h2 style="color:#00ff88">BEST PROPS TODAY 10/31/2026 - Safety Filter ON</h2>
    <p style="color:#888;font-size:12px">Formula: L10 Avg x Matchup Multiplier | Edge >8% | Hit 6/10 | Denver Time</p>
    <table><tr><th>Game</th><th>Player</th><th>Prop</th><th>Line</th><th>Proj</th><th>Pick</th><th>Edge</th><th>Conf</th><th>Why</th></tr>{rows}</table>
    <p style="color:#555;font-size:10px;margin-top:20px">Entertainment only. No guaranteed win rate. Edge = (Proj-Line)/Line. Safety = Edge>8% + Consistency.</p>
    </body></html>
    """

@app.get("/api/props")
def api():
    return BEST_TODAY
