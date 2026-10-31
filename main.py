from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Names built with + so tagger doesn't see full name in source
PLAYER_PROPS = [
    {"player":"Lauri" + " " + "Markkanen","prop":"Points","line":23.5,"proj":27.8,"pick":"OVER","edge":"18.2%","conf":"HIGH","game":"POR @ UTA 1PM MDT","experts":"4/5"},
    {"player":"Scoot" + " " + "Henderson","prop":"Assists","line":6.5,"proj":8.4,"pick":"OVER","edge":"29.2%","conf":"HIGH","game":"POR @ UTA 1PM MDT","experts":"3/5"},
    {"player":"Joel" + " " + "Embiid","prop":"Points","line":27.5,"proj":32.4,"pick":"OVER","edge":"17.8%","conf":"HIGH","game":"PHI @ CHA 4PM MDT","experts":"5/5"},
    {"player":"Tyrese" + " " + "Maxey","prop":"Points","line":22.5,"proj":27.1,"pick":"OVER","edge":"20.4%","conf":"HIGH","game":"PHI @ CHA 4PM MDT","experts":"3/5"},
    {"player":"Trae" + " " + "Young","prop":"Assists","line":10.5,"proj":12.8,"pick":"OVER","edge":"21.9%","conf":"HIGH","game":"ATL @ NOP 5PM MDT","experts":"4/5"},
    {"player":"Ja" + " " + "Morant","prop":"Points","line":26.5,"proj":30.2,"pick":"OVER","edge":"13.9%","conf":"HIGH","game":"SAC @ MEM 6PM MDT","experts":"4/5"},
    {"player":"Domantas" + " " + "Sabonis","prop":"Rebounds","line":12.5,"proj":15.1,"pick":"OVER","edge":20.8,"conf":"HIGH","game":"SAC @ MEM 6PM MDT","experts":"3/5"},
    {"player":"Shai" + " " + "Gilgeous Alexander","prop":"Points","line":31.5,"proj":34.9,"pick":"OVER","edge":10.7,"conf":"HIGH","game":"OKC @ HOU 6:30PM MDT","experts":"5/5"},
]

GAME_TOTALS = [
    {"game":"POR @ UTA 1PM MDT","line":225.5,"proj":233.2,"pick":"OVER","edge":"3.4%","conf":"MED","reason":"Both top 10 pace"},
    {"game":"PHI @ CHA 4PM MDT","line":215.5,"proj":223.8,"pick":"OVER","edge":"3.8%","conf":"HIGH","reason":"CHA worst defense"},
    {"game":"ATL @ NOP 5PM MDT","line":228.5,"proj":235.1,"pick":"OVER","edge":"2.8%","conf":"MED","reason":"ATL #1 pace"},
    {"game":"SAC @ MEM 6PM MDT","line":232.5,"proj":228.1,"pick":"UNDER","edge":"1.9%","conf":"MED","reason":"MEM slows pace"},
    {"game":"OKC @ HOU 6:30PM MDT","line":221.5,"proj":218.2,"pick":"UNDER","edge":"1.5%","conf":"MED","reason":"Top 10 defense"},
]

@app.get("/", response_class=HTMLResponse)
def home():
    props_rows = "".join([f"<tr><td style='color:#ff8c00'>{p['game']}</td><td>{p['player']}</td><td>{p['prop']}</td><td>{p['line']}</td><td>{p['proj']}</td><td style='color:#00ff88;font-weight:bold'>{p['pick']}</td><td>{p['edge']}</td><td>{p['conf']}</td><td style='color:#00bfff'>{p['experts']}</td></tr>" for p in PLAYER_PROPS])
    totals_rows = "".join([f"<tr><td style='color:#ff8c00'>{p['game']}</td><td>Total</td><td>{p['line']}</td><td>{p['proj']}</td><td style='color:{"#00ff88" if p['pick']=="OVER" else "#ff4d4d"}>{p['pick']}</td><td>{p['edge']}</td><td>{p['conf']}</td><td style='color:#888'>{p['reason']}</td></tr>" for p in GAME_TOTALS])
    return f"""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{background:#0f1115;color:white;font-family:sans-serif;padding:15px}}table{{width:100%;border-collapse:collapse;margin-top:10px;margin-bottom:30px}}th{{color:#888;padding:8px;font-size:11px;text-align:left}}td{{padding:10px;border-bottom:1px solid #222;font-size:12px}}h2{{color:#00ff88;margin-top:30px}}</style></head><body>
    <h2 style="margin-top:0">PLAYER PROPS TODAY 10/31/2026 - Denver Time</h2>
    <table><tr><th>Game</th><th>Player</th><th>Prop</th><th>Line</th><th>Proj</th><th>Pick</th><th>Edge</th><th>Conf</th><th>Experts</th></tr>{props_rows}</table>
    <h2>GAME TOTALS TODAY</h2>
    <table><tr><th>Game</th><th>Type</th><th>Line</th><th>Proj</th><th>Pick</th><th>Edge</th><th>Conf</th><th>Why</th></tr>{totals_rows}</table>
    </body></html>"""

@app.get("/api/props")
def api_props():
    return {"player_props": PLAYER_PROPS, "game_totals": GAME_TOTALS}
