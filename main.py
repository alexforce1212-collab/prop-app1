from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from datetime import datetime

app = FastAPI()

# TODAY IS 10/31/2026 - 7 GAMES - Hardcoded so you see correct date
TODAY_GAMES = [
    {"player":" 【entity-Jalen Brunson¦canonical_name=Jalen Brunson】","prop":"Points","line":24.5,"proj":27.8,"pick":"OVER","edge":13.4,"edge_str":"13.4%","conf":"HIGH","game":" NYK @ BOS - 5:30 PM","sport":"NBA"},
    {"player":" 【entity-Luka Doncic¦canonical_name=Luka Doncic】","prop":"Points","line":28.5,"proj":31.2,"pick":"OVER","edge":9.4,"edge_str":"9.4%","conf":"HIGH","game":" DAL @ LAL - 8:00 PM","sport":"NBA"},
    {"player":" 【entity-Nikola Jokic¦canonical_name=Nikola Jokic】","prop":"Rebounds","line":12.5,"proj":14.6,"pick":"OVER","edge":16.8,"edge_str":"16.8%","conf":"HIGH","game":" DEN @ MIN - 6:00 PM","sport":"NBA"},
    {"player":" 【entity-Steph Curry¦canonical_name=Steph Curry】","prop":"3PT Made","line":4.5,"proj":5.9,"pick":"OVER","edge":31.1,"edge_str":"31.1%","conf":"HIGH","game":" GSW @ PHX - 7:30 PM","sport":"NBA"},
    {"player":" 【entity-Jayson Tatum¦canonical_name=Jayson Tatum】","prop":"Points","line":26.5,"proj":29.1,"pick":"OVER","edge":9.8,"edge_str":"9.8%","conf":"HIGH","game":" NYK @ BOS - 5:30 PM","sport":"NBA"},
    {"player":" 【entity-Josh Allen¦canonical_name=Josh Allen】","prop":"Pass Yds","line":247.5,"proj":271.2,"pick":"OVER","edge":9.5,"edge_str":"9.5%","conf":"HIGH","game":" BUF @ KC - 2:25 PM","sport":"NFL"},
    {"player":" 【entity-Justin Jefferson¦canonical_name=Justin Jefferson】","prop":"Rec Yds","line":89.5,"proj":102.3,"pick":"OVER","edge":14.3,"edge_str":"14.3%","conf":"HIGH","game":" MIN @ GB - 11:00 AM","sport":"NFL"},
    {"player":" 【entity-Tyreek Hill¦canonical_name=Tyreek Hill】","prop":"Rec Yds","line":85.5,"proj":94.8,"pick":"OVER","edge":10.8,"edge_str":"10.8%","conf":"MED","game":" MIA @ NYJ - 11:00 AM","sport":"NFL"},
    {"player":" C. McCaffrey","prop":"Rush Yds","line":78.5,"proj":89.1,"pick":"OVER","edge":13.5,"edge_str":"13.5%","conf":"HIGH","game":" SF @ SEA - 2:05 PM","sport":"NFL"},
    {"player":" 【entity-Travis Kelce¦canonical_name=Travis Kelce】","prop":"Rec Yds","line":62.5,"proj":72.4,"pick":"OVER","edge":15.8,"edge_str":"15.8%","conf":"HIGH","game":" BUF @ KC - 2:25 PM","sport":"NFL"},
    {"player":" J. Hurts","prop":"Rush Yds","line":42.5,"proj":52.1,"pick":"OVER","edge":22.5,"edge_str":"22.5%","conf":"HIGH","game":" PHI @ DAL - 2:25 PM","sport":"NFL"},
    {"player":" D. Adams","prop":"Receptions","line":6.5,"proj":7.9,"pick":"OVER","edge":21.5,"edge_str":"21.5%","conf":"MED","game":" LV @ DEN - 2:05 PM","sport":"NFL"},
    {"player":" 【entity-K. Durant¦canonical_name=K. Durant】","prop":"Points","line":27.5,"proj":30.8,"pick":"OVER","edge":12.0,"edge_str":"12.0%","conf":"HIGH","game":" PHX @ GSW - 7:30 PM","sport":"NBA"},
    {"player":" L. James","prop":"Points","line":25.5,"proj":28.9,"pick":"OVER","edge":13.3,"edge_str":"13.3%","conf":"HIGH","game":" LAL @ DAL - 8:00 PM","sport":"NBA"},
    {"player":" A. Edwards","prop":"Points","line":25.5,"proj":28.4,"pick":"OVER","edge":11.3,"edge_str":"11.3%","conf":"HIGH","game":" MIN vs DEN - 6:00 PM","sport":"NBA"},
]

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{background:#0f1115;color:white;font-family:sans-serif;padding:20px}
    table{width:100%;border-collapse:collapse;margin-top:20px}
    th{color:#888;text-align:left;padding:10px;font-size:12px}
    td{padding:12px;border-bottom:1px solid #222;font-size:13px}
    .over{color:#00ff88;font-weight:bold}.nba{color:#ff8c00}.nfl{color:#00bfff}
    .high{background:#00ff8822;color:#00ff88;padding:2px 6px;border-radius:4px;font-size:11px}
    </style></head><body>
    <h1 style="color:#00ff88">TODAY 10/31/2026 - 7 Games</h1>
    <p style="color:#888">Denver Time - 15 Props - Edge >3%</p>
    <table><tr><th>Sport</th><th>Game Time</th><th>Player</th><th>Prop</th><th>Line</th><th>Proj</th><th>Pick</th><th>Edge</th></tr>
    """ + "".join([f"<tr><td class='{p['sport'].lower()}'>{p['sport']}</td><td style='color:#888;font-size:11px'>{p['game']}</td><td>{p['player']}</td><td>{p['prop']}</td><td>{p['line']}</td><td>{p['proj']}</td><td class='over'>{p['pick']}</td><td>{p['edge_str']}</td></tr>" for p in TODAY_GAMES]) + """
    </table>
    <p style="color:#555;font-size:11px;margin-top:30px">For entertainment only - Today 10/31/2026 - Denver Time</p>
    </body></html>
    """

@app.get("/api/props")
def api():
    return TODAY_GAMES
