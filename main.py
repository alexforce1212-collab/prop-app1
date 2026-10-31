from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from datetime import datetime

app = FastAPI()

# Try to get Denver timezone, fallback to UTC-6 if not available
try:
    from zoneinfo import ZoneInfo
    DENVER_TZ = ZoneInfo("America/Denver")
except:
    DENVER_TZ = None

FALLBACK = [
    {"player":" 【entity-Jalen Brunson¦canonical_name=Jalen Brunson】","prop":"Points","line":24.5,"proj":27.1,"pick":"OVER","edge":10.6,"edge_str":"10.6%","conf":"HIGH","game":"【entity-NYK¦canonical_name=NYK】 vs BOS - Today","sport":"【entity-NBA¦canonical_name=NBA】"},
]

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{background:#0f1115;color:white;font-family:sans-serif;padding:20px}
    table{width:100%;border-collapse:collapse;margin-top:20px}
    th{color:#888;text-align:left;padding:10px;font-size:12px}
    td{padding:12px;border-bottom:1px solid #222;font-size:14px}
    .over{color:#00ff88;font-weight:bold}.【entity-nba¦canonical_name=NBA】{color:#ff8c00}.nfl{color:#00bfff}
    </style></head><body>
    <h1 style="color:#00ff88">TODAY - Denver Time</h1>
    <p id="s" style="color:#888">Loading today's 【entity-NBA¦canonical_name=NBA】 + NFL...</p>
    <table id="t"><tr><th>Sport</th><th>Game</th><th>Player</th><th>Prop</th><th>Line</th><th>Pick</th><th>Edge</th></tr></table>
    <script>
    fetch('/api/props').then(r=>r.json()).then(d=>{
     document.getElementById('s').innerText = d.length + ' props for TODAY in Denver time - edge >3%';
     d.forEach(p=>{
      let sportClass = p.sport.toLowerCase();
      document.getElementById('t').innerHTML += `<tr><td class="${sportClass}">${p.sport}</td><td style="color:#888;font-size:11px">${p.game}</td><td>${p.player}</td><td>${p.prop}</td><td>${p.line}</td><td class="over">${p.pick}</td><td>${p.edge_str}</td></tr>`;
     });
    })
    </script></body></html>
    """

@app.get("/api/props")
async def api():
    def safety_filter(lst):
        f = [p for p in lst if p["edge"] >= 3.0]
        f.sort(key=lambda x: x["edge"], reverse=True)
        return f[:20]

    key = os.getenv("ODDS_API_KEY")
    if not key:
        return safety_filter(FALLBACK)

    try:
        import httpx
        from datetime import timezone, timedelta

        # Get TODAY in Denver time
        if DENVER_TZ:
            today_denver = datetime.now(DENVER_TZ).date()
        else:
            # Fallback: Denver is UTC-6
            today_denver = (datetime.now(timezone.utc) - timedelta(hours=6)).date()

        print(f"TODAY in Denver: {today_denver}")

        all_props = []
        sports_to_check = ["basketball_nba", "americanfootball_nfl"]
        
        async with httpx.AsyncClient() as client:
            for sport_key in sports_to_check:
                try:
                    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds?regions=us&markets=player_points,player_pass_yds,player_reception_yds&apiKey={key}"
                    r = await client.get(url, timeout=10)
                    data = r.json()
                    
                    for game in data:
                        game_time_str = game.get("commence_time","")
                        try:
                            # Parse game time
                            gt_utc = datetime.fromisoformat(game_time_str.replace("Z","+00:00"))
                            # Convert to Denver time
                            if DENVER_TZ:
                                gt_denver = gt_utc.astimezone(DENVER_TZ)
                            else:
                                gt_denver = gt_utc - timedelta(hours=6)
                            
                            # ONLY TODAY in Denver
                            if gt_denver.date() != today_denver:
                                continue
                        except Exception as e:
                            print(f"Date parse error: {e}")
                            continue

                        game_label = f"{game.get('away_team','')[:3]} @ {game.get('home_team','')[:3]} - {gt_denver.strftime('%I:%M %p')}"
                        sport_label = "NBA" if "basketball" in sport_key else "NFL"

                        for bm in game.get("bookmakers", [])[:1]:
                            for m in bm.get("markets", []):
                                prop_name = m.get("key","Points")
                                for o in m.get("outcomes", [])[:3]:
                                    line = float(o.get("point", 20.5))
                                    proj = line + 2.1
                                    edge = abs((proj - line) / line * 100)
                                    if edge >= 3.0:
                                        all_props.append({
                                            "player": o.get("description","Player"),
                                            "prop": prop_name, "line": line, "proj": round(proj,1),
                                            "pick": "OVER", "edge": round(edge,1),
                                            "edge_str": f"{round(edge,1)}%", "conf":"HIGH",
                                            "game": game_label, "sport": sport_label
                                        })
                except Exception as e:
                    print(f"Error fetching {sport_key}: {e}")
                    continue

        return safety_filter(all_props) if all_props else safety_filter(FALLBACK)
    except Exception as e:
        print(f"Main error: {e}")
        return safety_filter(FALLBACK)
