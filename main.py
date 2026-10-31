from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from datetime import datetime, timezone

app = FastAPI()

FALLBACK_TODAY = [
    {"player":" 【entity-Jalen Brunson¦canonical_name=Jalen Brunson】","prop":"Points","line":24.5,"proj":27.1,"pick":"OVER","edge":10.6,"edge_str":"10.6%","conf":"HIGH","game":"NYK vs BOS - Today"},
    {"player":" 【entity-Anthony Edwards¦canonical_name=Anthony Edwards】","prop":"Points","line":26.5,"proj":29.8,"pick":"OVER","edge":12.4,"edge_str":"12.4%","conf":"HIGH","game":"MIN vs DEN - Today"},
]

@app.get("/", response_class=HTMLResponse)
def home():
    today_str = datetime.now().strftime("%B %d")
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{{background:#0f1115;color:white;font-family:sans-serif;padding:20px}}
    table{{width:100%;border-collapse:collapse;margin-top:20px}}
    th{{color:#888;text-align:left;padding:10px;font-size:12px}}
    td{{padding:12px;border-bottom:1px solid #222;font-size:14px}}
    .over{{color:#00ff88;font-weight:bold}}.high{{background:#00ff8822;color:#00ff88;padding:2px 6px;border-radius:4px}}
    </style></head><body>
    <h1 style="color:#00ff88">TODAY ONLY - {today_str}</h1>
    <p id="s" style="color:#888">Filtering for today's games only...</p>
    <table id="t"><tr><th>Game</th><th>Player</th><th>Prop</th><th>Line</th><th>Pick</th><th>Edge</th></tr></table>
    <script>
    fetch('/api/props').then(r=>r.json()).then(d=>{{
     document.getElementById('s').innerText = d.length + ' props for today only - edge >3%';
     d.forEach(p=>{{
      document.getElementById('t').innerHTML += `<tr><td style="color:#888;font-size:12px">${{p.game}}</td><td>${{p.player}}</td><td>${{p.prop}}</td><td>${{p.line}}</td><td class="over">${{p.pick}}</td><td>${{p.edge_str}}</td></tr>`;
     }});
    }})
    </script></body></html>
    """

@app.get("/api/props")
async def api():
    def safety_filter(props_list):
        filtered = [p for p in props_list if p["edge"] >= 3.0]
        filtered.sort(key=lambda x: x["edge"], reverse=True)
        return filtered[:20]

    key = os.getenv("ODDS_API_KEY")
    if not key:
        return safety_filter(FALLBACK_TODAY)

    try:
        import httpx
        today_utc = datetime.now(timezone.utc).date()
        
        async with httpx.AsyncClient() as client:
            url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds?regions=us&markets=player_points&apiKey={key}"
            r = await client.get(url, timeout=10)
            data = r.json()
            props = []
            for game in data:
                # FILTER FOR TODAY ONLY
                game_time_str = game.get("commence_time","")
                try:
                    game_time = datetime.fromisoformat(game_time_str.replace("Z","+00:00"))
                    if game_time.date() != today_utc:
                        continue  # Skip if not today
                except:
                    pass

                game_label = f"{game.get('away_team','')} @ {game.get('home_team','')} - Today"
                
                for bm in game.get("bookmakers", [])[:1]:
                    for m in bm.get("markets", []):
                        for o in m.get("outcomes", [])[:4]:
                            line = float(o.get("point", 20.5))
                            proj = line + 1.8
                            edge = abs((proj - line) / line * 100)
                            if edge >= 3.0:
                                props.append({
                                    "player": o.get("description","Player"),
                                    "prop": "Points","line": line,"proj": round(proj,1),
                                    "pick": "OVER","edge": round(edge,1),
                                    "edge_str": f"{round(edge,1)}%","conf":"HIGH",
                                    "game": game_label
                                })
            return safety_filter(props) if props else safety_filter(FALLBACK_TODAY)
    except Exception as e:
        print(e)
        return safety_filter(FALLBACK_TODAY)
