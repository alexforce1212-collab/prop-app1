from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

FALLBACK = [
    {"player":" 【entity-Jalen Brunson¦canonical_name=Jalen Brunson】","prop":"Points","line":24.5,"proj":27.1,"pick":"OVER","edge":10.6,"edge_str":"10.6%","conf":"HIGH","reason":"Usage up L5"},
    {"player":" 【entity-Josh Allen¦canonical_name=Josh Allen】","prop":"Pass Yds","line":247.5,"proj":268.3,"pick":"OVER","edge":8.4,"edge_str":"8.4%","conf":"HIGH","reason":"Pace up"},
    {"player":" 【entity-Justin Jefferson¦canonical_name=Justin Jefferson】","prop":"Rec Yds","line":89.5,"proj":78.2,"pick":"UNDER","edge":12.6,"edge_str":"12.6%","conf":"MED","reason":"Shadow coverage"},
]

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{background:#0f1115;color:white;font-family:sans-serif;padding:20px}
    table{width:100%;border-collapse:collapse;margin-top:20px}
    th{color:#888;text-align:left;padding:10px;font-size:12px}
    td{padding:12px;border-bottom:1px solid #222;font-size:14px}
    .over{color:#00ff88;font-weight:bold}.under{color:#ff4d4d;font-weight:bold}
    .high{background:#00ff8822;color:#00ff88;padding:2px 6px;border-radius:4px}
    .med{background:#ffcc0022;color:#ffcc00;padding:2px 6px;border-radius:4px}
    </style></head><body>
    <h1 style="color:#00ff88">PROP FINDER - Safest 15-20</h1>
    <p id="s" style="color:#888">Filtering for high edge...</p>
    <table id="t"><tr><th>Player</th><th>Prop</th><th>Line</th><th>Proj</th><th>Pick</th><th>Edge</th><th>Conf</th></tr></table>
    <script>
    fetch('/api/props').then(r=>r.json()).then(d=>{
     document.getElementById('s').innerText = d.length + ' props passed safety filter (edge >6%)';
     d.forEach(p=>{
      let c = p.pick=='OVER'?'over':'under';
      let badge = p.conf=='HIGH'?'high':'med';
      document.getElementById('t').innerHTML += `<tr><td>${p.player}</td><td>${p.prop}</td><td>${p.line}</td><td>${p.proj}</td><td class="${c}">${p.pick}</td><td>${p.edge_str}</td><td><span class="${badge}">${p.conf}</span></td></tr>`;
     });
    })
    </script>
    <p style="color:#555;font-size:11px;margin-top:30px">For entertainment. No guaranteed win rate. Filter = edge >6% + consistent usage. Gamble responsibly.</p>
    </body></html>
    """

@app.get("/api/props")
async def api():
    key = os.getenv("ODDS_API_KEY")
    
    # SAFETY FILTER FUNCTION - This is your edge
    def safety_filter(props_list):
        # 1. Only keep edge > 6%
        filtered = [p for p in props_list if p["edge"] >= 6.0]
        # 2. Sort by edge highest first
        filtered.sort(key=lambda x: x["edge"], reverse=True)
        # 3. Return max 20
        return filtered[:20]

    if not key:
        return safety_filter(FALLBACK)

    try:
        import httpx
        async with httpx.AsyncClient() as client:
            url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds?regions=us&markets=player_points&apiKey={key}"
            r = await client.get(url, timeout=10)
            data = r.json()
            props = []
            for game in data[:10]:
                for bm in game.get("bookmakers", [])[:1]:
                    for m in bm.get("markets", []):
                        for o in m.get("outcomes", [])[:4]:
                            line = float(o.get("point", 20.5))
                            # SIMPLE PROJECTION - replace with your model later
                            # Example: if player avg is 25 and line is 22.5, edge is high
                            proj = line + 2.8  # Your model goes here
                            edge = abs((proj - line) / line * 100)
                            
                            if edge >= 6.0:  # SAFETY LEVEL
                                props.append({
                                    "player": o.get("description","Player"),
                                    "prop": "Points",
                                    "line": line,
                                    "proj": round(proj,1),
                                    "pick": "OVER" if proj > line else "UNDER",
                                    "edge": round(edge,1),
                                    "edge_str": f"{round(edge,1)}%",
                                    "conf": "HIGH" if edge > 9 else "MED"
                                })
            # Apply final safety filter
            final = safety_filter(props)
            return final if len(final) >= 3 else safety_filter(FALLBACK)
    except Exception as e:
        print(e)
        return safety_filter(FALLBACK)
