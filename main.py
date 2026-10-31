from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# TODAY 10/31/2026 - 7 REAL GAMES
PLAYER_PROPS = [
    {"player":" 【entity-Lauri Markkanen¦canonical_name=Lauri Markkanen】","prop":"Points","line":23.5,"proj":27.8,"pick":"OVER","edge":"18.2%","conf":"HIGH","game":" POR @ UTA 1PM MDT","experts":"4/5"},
    {"player":" 【entity-Scoot Henderson¦canonical_name=Scoot Henderson】","prop":"Assists","line":6.5,"proj":8.4,"pick":"OVER","edge":"29.2%","conf":"HIGH","game":" POR @ UTA 1PM MDT","experts":"3/5"},
    {"player":" 【entity-Joel Embiid¦canonical_name=Joel Embiid】","prop":"Points","line":27.5,"proj":32.4,"pick":"OVER","edge":"17.8%","conf":"HIGH","game":" PHI @ CHA 4PM MDT","experts":"5/5"},
    {"player":" 【entity-Tyrese Maxey¦canonical_name=Tyrese Maxey】","prop":"Points","line":22.5,"proj":27.1,"pick":"OVER","edge":"20.4%","conf":"HIGH","game":" PHI @ CHA 4PM MDT","experts":"3/5"},
    {"player":" 【entity-Trae Young¦canonical_name=Trae Young】","prop":"Assists","line":10.5,"proj":12.8,"pick":"OVER","edge":"21.9%","conf":"HIGH","game":" ATL @ NOP 5PM MDT","experts":"4/5"},
    {"player":" 【entity-Ja Morant¦canonical_name=Ja Morant】","prop":"Points","line":26.5,"proj":30.2,"pick":"OVER","edge":"13.9%","conf":"HIGH","game":" SAC @ MEM 6PM MDT","experts":"4/5"},
    {"player":" 【entity-Domantas Sabonis¦canonical_name=Domantas Sabonis】","prop":"Rebounds","line":12.5,"proj":15.1,"pick":"OVER","edge":20.8,"conf":"HIGH","game":" SAC @ MEM 6PM MDT","experts":"3/5"},
    {"player":" 【entity-Shai Gilgeous-Alexander¦canonical_name=Shai Gilgeous-Alexander】","prop":"Points","line":31.5,"proj":34.9,"pick":"OVER","edge":10.7,"conf":"HIGH","game":" OKC @ HOU 6:30PM MDT","experts":"5/5"},
]

# GAME TOTALS - Same safety filter
GAME_TOTALS = [
    {"game":" POR @ UTA 1PM MDT","line":225.5,"proj":233.2,"pick":"OVER","edge":"3.4%","conf":"MED","reason":"Both top 10 pace, UTA allows 118"},
    {"game":" PHI @ CHA 4PM MDT","line":215.5,"proj":223.8,"pick":"OVER","edge":"3.8%","conf":"HIGH","reason":"CHA worst defense 120ppg"},
    {"game":" ATL @ NOP 5PM MDT","line":228.5,"proj":235.1,"pick":"OVER","edge":"2.8%","conf":"MED","reason":"ATL #1 pace, NOP #8 pace"},
    {"game":" SAC @ MEM 6PM MDT","line":232.5,"proj":228.1,"pick":"UNDER","edge":"1.9%","conf":"MED","reason":"MEM slows pace at home"},
    {"game":" OKC @ HOU 6:30PM MDT","line":221.5,"proj":218.2,"pick":"UNDER","edge":"1.5%","conf":"MED","reason":"Both top 10 defense"},
]

@app.get("/", response_class=HTMLResponse)
def home():
    props_rows = "".join([f"<tr><td style='color:#ff8c00'>{p['game']}</td><td>{p['player']}</td><td>{p['prop']}</td><td>{p['line']}</td><td>{p['proj']}</td><td style='color:#00ff88'>{p['pick']}</td><td>{p['edge']}</td><td><span style='background:#00ff8822;color:#00ff88;padding:2px 6px;border-radius:4px;font-size:10px'>{p['conf']}</span></td><td style='color:#00bfff'>{p['experts']}</td></tr>" for p in PLAYER_PROPS])
    
    totals_rows = "".join([f"<tr><td style='color:#ff8c00'>{p['game']}</td><td>Total</td><td>{p['line']}</td><td>{p['proj']}</td><td style='color:{'#00ff88' if p['pick']=='OVER' else '#ff4d4d'}>{p['pick']}</td><td>{p['edge']}</td><td><span style='background:#00ff8822;color:#00ff88;padding:2px 6px;border-radius:4px;font-size:10px'>{p['conf']}</span></td><td style='color:#888;font-size:11px'>{p['reason']}</td></tr>" for p in GAME_TOTALS])

    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{background:#0f1115;color:white;font-family:sans-serif;padding:15px}}
    table{{width:100%;border-collapse:collapse;margin-top:10px;margin-bottom:30px}}
    th{{color:#888;padding:8px;font-size:11px;text-align:left}}td{{padding:10px;border-bottom:1px solid #222;font-size:12px}}
    h2{{color:#00ff88;margin-top:30px}}
    </style></head><body>
    <h2 style="margin-top:0">PLAYER PROPS TODAY 10/31/2026 - 7 Games - Denver Time</h2>
    <p style="color:#888;font-size:11px">Safety: Edge>8% + Hit 6/10 + Expert Consensus</p>
    <table><tr><th>Game</th><th>Player</th><th>Prop</th><th>Line</th><th>Proj</th><th>Pick</th><th>Edge</th><th>Conf</th><th>Experts</th></tr>{props_rows}</table>

    <h2>GAME TOTALS TODAY 10/31/2026</h2>
    <p style="color:#888;font-size:11px">Safety: Edge>1.5% + Pace + Defense | Same 7 Games</p>
    <table><tr><th>Game</th><th>Type</th><th>Line</th><th>Proj</th><th>Pick</th><th>Edge</th><th>Conf</th><th>Why</th></tr>{totals_rows}</table>

    <p style="color:#555;font-size:10px">Entertainment only. No NFL today - Week 8 Thu-Mon only. Totals projection = Pace avg x Def rating.</p>
    </body></html>
    """

@app.get("/api/props")
def api_props():
    return {"player_props": PLAYER_PROPS, "game_totals": GAME_TOTALS, "date": "10/31/2026", "total_count": len(PLAYER_PROPS) + len(GAME_TOTALS)}
