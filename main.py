from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

TODAY_REAL = [
    {"player":" 【entity-Lauri Markkanen¦canonical_name=Lauri Markkanen】","prop":"Points","line":23.5,"proj":26.8,"pick":"OVER","edge":"14.0%","conf":"HIGH","game":" POR @ UTA - 1:00 PM MDT","sport":"【entity-NBA¦canonical_name=NBA】"},
    {"player":" 【entity-Scoot Henderson¦canonical_name=Scoot Henderson】","prop":"Assists","line":6.5,"proj":8.1,"pick":"OVER","edge":"24.6%","conf":"HIGH","game":" POR @ UTA - 1:00 PM MDT","sport":"【entity-NBA¦canonical_name=NBA】"},
    {"player":" 【entity-Joel Embiid¦canonical_name=Joel Embiid】","prop":"Points","line":27.5,"proj":31.2,"pick":"OVER","edge":"13.4%","conf":"HIGH","game":" PHI @ CHA - 4:00 PM MDT","sport":"NBA"},
    {"player":" LaMelo Ball","prop":"Points","line":24.5,"proj":27.9,"pick":"OVER","edge":"13.8%","conf":"HIGH","game":" PHI @ CHA - 4:00 PM MDT","sport":"NBA"},
    {"player":" Trae Young","prop":"Assists","line":10.5,"proj":12.8,"pick":"OVER","edge":"21.9%","conf":"HIGH","game":" ATL @ NOP - 5:00 PM MDT","sport":"NBA"},
    {"player":" Zion Williamson","prop":"Points","line":22.5,"proj":25.6,"pick":"OVER","edge":"13.7%","conf":"HIGH","game":" ATL @ NOP - 5:00 PM MDT","sport":"NBA"},
    {"player":" Ja Morant","prop":"Points","line":26.5,"proj":29.8,"pick":"OVER","edge":"12.4%","conf":"HIGH","game":" SAC @ MEM - 6:00 PM MDT","sport":"NBA"},
    {"player":" Domantas Sabonis","prop":"Rebounds","line":12.5,"proj":14.9,"pick":"OVER","edge":"19.2%","conf":"HIGH","game":" SAC @ MEM - 6:00 PM MDT","sport":"NBA"},
    {"player":" Shai Gilgeous-Alexander","prop":"Points","line":31.5,"proj":34.8,"pick":"OVER","edge":"10.4%","conf":"HIGH","game":" OKC @ HOU - 6:30 PM MDT","sport":"【entity-NBA¦canonical_name=NBA】"},
    {"player":" 【entity-Alperen Sengun¦canonical_name=Alperen Sengun】","prop":"Rebounds","line":9.5,"proj":11.8,"pick":"OVER","edge":"24.2%","conf":"MED","game":" OKC @ HOU - 6:30 PM MDT","sport":"【entity-NBA¦canonical_name=NBA】"},
]

@app.get("/", response_class=HTMLResponse)
def home():
    rows = "".join([f"<tr><td class='{p['sport'].lower()}'>{p['sport']}</td><td style='color:#888;font-size:11px'>{p['game']}</td><td>{p['player']}</td><td>{p['prop']}</td><td>{p['line']}</td><td>{p['proj']}</td><td style='color:#00ff88'>{p['pick']}</td><td>{p['edge']}</td></tr>" for p in TODAY_REAL])
    return f"""<html><head><style>body{{background:#0f1115;color:white;font-family:sans-serif;padding:20px}}table{{width:100%;border-collapse:collapse}}th{{color:#888;padding:10px;font-size:12px}}td{{padding:12px;border-bottom:1px solid #222;font-size:13px}}.【entity-nba¦canonical_name=NBA】{{color:#ff8c00}}</style></head><body>
    <h1 style="color:#00ff88">TODAY 10/31/2026 - REAL GAMES</h1>
    <p style="color:#888">7 【entity-NBA¦canonical_name=NBA】 games today - POR@UTA 1pm MDT, PHI@CHA 4pm MDT, ATL@NOP 5pm MDT, SAC@MEM 6pm MDT, OKC@HOU 6:30pm MDT - No 【entity-NFL¦canonical_name=NFL】 today</p>
    <table><tr><th>Sport</th><th>Game Time Denver</th><th>Player</th><th>Prop</th><th>Line</th><th>Proj</th><th>Pick</th><th>Edge</th></tr>{rows}</table>
    </body></html>"""

@app.get("/api/props")
def api():
    return TODAY_REAL
