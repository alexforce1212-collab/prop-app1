import httpx
from bs4 import BeautifulSoup
import asyncio
from datetime import datetime

WEIGHTS = {"pickswise": 1.5, "action": 2.0, "covers": 1.0, "my_model": 2.0}

async def scrape_pickswise():
    picks = []
    try:
        async with httpx.AsyncClient() as client:
            # 【entity-NBA¦canonical_name=NBA】 props page - inspect this page for real selectors
            url = "https://www.pickswise.com/nba/picks/"
            r = await client.get(url, headers={"User-Agent": "Mozilla/5.0 Chrome/120"}, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            # REAL SELECTOR - you will need to inspect pickswise HTML
            # Example: each pick is in div.pick-card
            for card in soup.select("div.pick-card")[:15]:
                try:
                    player = card.get_text()[:50]  # Parse real player name
                    picks.append(player)
                except:
                    continue
    except Exception as e:
        print(f"Pickswise error: {e}")
    return picks

async def scrape_action_network():
    picks = []
    try:
        async with httpx.AsyncClient() as client:
            url = "https://www.actionnetwork.com/nba/expert-picks"
            r = await client.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            # REAL SELECTOR for 【entity-Action Network¦canonical_name=Action Network】
            for row in soup.select("div.expert-pick-row")[:15]:
                picks.append(row.get_text()[:50])
    except Exception as e:
        print(f"Action error: {e}")
    return picks

async def scrape_covers():
    picks = []
    try:
        async with httpx.AsyncClient() as client:
            url = "https://www.covers.com/nba/picks"
            r = await client.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            for row in soup.select("div.covers-pick")[:15]:
                picks.append(row.get_text()[:50])
    except Exception as e:
        print(f"Covers error: {e}")
    return picks

async def get_all_consensus():
    # Run all 3 scrapers in parallel
    results = await asyncio.gather(
        scrape_pickswise(),
        scrape_action_network(),
        scrape_covers(),
        return_exceptions=True
    )
    
    pickswise_picks, action_picks, covers_picks = results
    
    # Count consensus - how many sources agree on same player prop
    consensus = {}
    
    # For today 10/31/2026 - 7 real games, we build consensus map
    # In production, you parse player + line from each source
    
    # MOCK that shows structure - replace with real parsing
    # Example real data after parsing:
    all_data = {
        "【entity-Lauri Markkanen¦canonical_name=Lauri Markkanen】 Over 23.5": {"pickswise": 4, "action": 3, "covers": 68},
        "【entity-Joel Embiid¦canonical_name=Joel Embiid】 Over 27.5": {"pickswise": 5, "action": 5, "covers": 78},
    }
    
    final = []
    for prop, scores in all_data.items():
        # Weighted consensus calculation
        weighted_score = (
            scores.get("pickswise",0) * WEIGHTS["pickswise"] +
            scores.get("action",0) * WEIGHTS["action"] +
            (scores.get("covers",0)/20) * WEIGHTS["covers"]
        ) / sum(WEIGHTS.values()) * 20
        
        if weighted_score >= 75:  # Only keep 75%+ consensus
            final.append({
                "prop": prop,
                "consensus_score": f"{round(weighted_score)}% ({len([k for k,v in scores.items() if v>0])} sources)",
                "breakdown": f"Pickswise {scores.get('pickswise',0)}/5 + Action {scores.get('action',0)}/5 + Covers {scores.get('covers',0)}% + Edge",
                "sources": scores
            })
    
    return final

if __name__ == "__main__":
    # Test run
    result = asyncio.run(get_all_consensus())
    print(f"Found {len(result)} consensus picks for {datetime.now().strftime('%m/%d/%Y')}")
    for r in result:
        print(r)
