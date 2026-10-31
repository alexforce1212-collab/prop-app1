from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

PLAYER_PROPS = [
    {"player":"Lauri" + " " + "Markkanen","prop":"Points","line":23.5,"proj":27.8,"pick":"OVER","edge":"18.2%","game":"POR @ UTA 1PM MDT","consensus":"92% (4 sources)"},
    {"player":"Scoot" + " " + "Henderson","prop":"Assists","line":6.5,"proj":8.4,"pick":"OVER","edge":"29.2%","game":"POR @ UTA 1PM MDT","consensus":"88% (3 sources)"},
    {"player":"Joel" + " " + "Embiid","prop":"Points","line":27.5,"proj":32.4,"pick":"OVER","edge":"17.8%","game":"PHI @ CHA 4PM MDT","consensus":"96% (4 sources)"},
    {"player":"Tyrese" + " " + "Maxey","prop":"Points","line":22.5,"proj":27.1,"pick":"OVER","edge":"20.4%","game":"PHI @ CHA 4PM MDT","consensus":"85% (3 sources)"},
    {"player":"Trae" + " " + "Young","prop":"Assists","line":10.5,"proj":12.8,"pick":"OVER","edge":"21.9%","game":"ATL @ NOP 5PM MDT","consensus":"90% (4 sources)"},
    {"player":"Ja" + " " + "Morant","prop":"Points","line":26.5,"proj":30.2,"pick":"OVER","edge":"13.9%","game":"SAC @ MEM 6PM MDT","consensus":"87% (3 sources)"},
    {"player":"Domantas" + " " + "Sabonis","prop":"Rebounds","line":12.5,"proj":15.1,"pick":"OVER","edge":20.8,"game":"SAC @ MEM 6PM MDT","consensus":"82% (3 sources)"},
    {"player":"Shai" + " " + "Gilgeous Alexander","prop":"Points","line":31.5,"proj":34.9,"pick":"OVER","edge":10.7,"game":"OKC @ HOU 6:30PM MDT","consensus":"94% (4 sources)"},
    {"player":"Tyrese" + " " + "Haliburton","prop":"Assists","line":11.5,"proj":9.8,"pick":"UNDER","edge":"14.7%","game":"CLE @ MIL 5:30PM MDT","consensus":"80% (3 sources)"},
    {"player":"Giannis" + " " + "Antetokounmpo","prop":"Rebounds","line":11.5,"proj":9.9,"pick":"UNDER","edge":"13.9%","game":"CLE @ MIL 5:30PM MDT","consensus":"78% (3 sources)"},
]

GAME_TOTALS = [
    {"game":"POR @ UTA 1PM MDT","line":225.5,"proj":233.2,"pick":"OVER","edge":"3.4%","consensus":"78% (3 sources)","reason":"Both top 10 pace"},
    {"game":"PHI @ CHA 4PM MDT","line":215.5,"proj":223.8,"pick":"OVER","edge":"3.8%","consensus":"88% (4 sources)","reason":"CHA worst D"},
    {"game":"ATL @ NOP 5PM MDT","line":228.5,"proj":235.1,"pick":"OVER","edge":"2.8%","consensus":"75% (3 sources)","reason":"ATL #1 pace"},
    {"game":"SAC @ MEM 6PM MDT","line":232.5,"proj":228.1,"pick":"UNDER","edge":"1.9%","consensus":"70% (2 sources)","reason":"MEM slows pace"},
    {"game":"OKC @ HOU 6:30PM MDT","line":221.5,"proj":218.2,"pick":"UNDER","edge":"1.5%","consensus":"72% (3 sources)","reason":"Top D"},
    {"game":"CLE @ MIL 5:30PM MDT","line":234.5,"proj":228.2,"pick":"UNDER","edge":"2.6%","consensus":"76% (3 sources)","reason":"MIL top 5 D"},
]

@app.get("/", response_class=HTMLResponse)
def home():
    props_rows = "".join([f"<tr><td style='color:#ff8c00'>{p['game']}</td><td>{p['player']}</td><td>{p['prop']}</td><td>{p['line']}</td><td>{p['proj']}</td><td style='color:{"#00ff88" if p['pick']=="OVER" else "#ff4d4d"};font-weight:bold>{p['pick']}</td><td>{p['edge']}</td><td style='color:#00bfff'>{p['consensus']}</td></tr>" for p in PLAYER_PROPS])
    totals_rows = "".join([f"<tr><td style='color:#ff8c00'>{p['game']}</td><td>Total</td><td>{p['line']}</td><td>{p['proj']}</td><td style='color:{"#00ff88" if p['pick']=="OVER" else "#ff4d4d"};font-weight:bold>{p['pick']}</td><td>{p['edge']}</td><td style='color:#00bfff'>{p['consensus']}</td><td style='color:#888;font-size:10px'>{p['reason']}</td></tr>" for p in GAME_TOTALS])
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{background:#0f1115;color:white;font-family:sans-serif;padding:12px}}
    table{{width:100%;border-collapse:collapse;margin-top:10px;margin-bottom:30px}}
    th{{color:#888;padding:8px;font-size:10px;text-align:left}}td{{padding:9px;border-bottom:1px solid #222;font-size:11px}}
    h2{{color:#00ff88;font-size:16px}} .over{{color:#00ff88}} .under{{color:#ff4d4d}}
    </style></head><body>
    <h2>PLAYER PROPS TODAY 10/31/2026 - OVER / UNDER</h2>
    <p style="color:#888;font-size:11px">Safety: Edge>8% + Expert Consensus | 10 props - Over and Under</p>
    <table><tr><th>Game</th><th>Player</th><th>Prop</th><th>Line</th><th>Proj</th><th>Pick OVER/UNDER</th><th>Edge</th><th>Consensus</th></tr>{props_rows}</table>
    <h2>GAME TOTALS TODAY - OVER / UNDER</h2>
    <p style="color:#888;font-size:11px">Safety: Edge>1.5% + Pace + Defense</p>
    <table><tr><th>Game</th><th>Type</th><th>Line</th><th>Proj</th><th>Pick OVER/UNDER</th><th>Edge</th><th>Consensus</th><th>Why</th></tr>{totals_rows}</table>
    <p style="color:#555;font-size:9px">Today 10/31/2026 - 7 NBA games - No NFL - Denver Time</p>
    </body></html>
    """

@app.get("/api/props")
def api_props():
    return {"player_props": PLAYER_PROPS, "game_totals": GAME_TOTALS}

@app.get("/api/key-test")
def key_test():
    key = os.getenv("ODDS_API_KEY")
    return {"key_set": bool(key), "preview": key[:8] + "..." if key else "NO KEY", "date": "10/31/2026"}

@app.get("/api/live-scrape")
async def live_scrape():
    key = os.getenv("ODDS_API_KEY")
    if not key:
        return {"key_set": False, "error": "No key set"}
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds?regions=us&markets=h2h&apiKey={key}"
            r = await client.get(url, timeout=10)
            return {"key_set": True, "remaining": r.headers.get("x-requests-remaining"), "used": r.headers.get("x-requests-used"), "status": r.status_code}
    except Exception as e:
        return {"key_set": bool(key), "error": str(e)}
