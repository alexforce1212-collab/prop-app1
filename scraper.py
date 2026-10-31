import httpx
from bs4 import BeautifulSoup
from datetime import datetime

# This runs every morning at 10am Denver time via Railway cron
async def scrape_expert_picks():
    expert_picks = []
    
    # Example: Scrape 【entity-Pickswise¦canonical_name=Pickswise】 (free, no login)
    try:
        async with httpx.AsyncClient() as client:
            # NBA player props page
            url = "https://www.pickswise.com/nba/picks/"
            r = await client.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Find all prop picks - this is simplified, you inspect their HTML
            for card in soup.select(".pick-card")[:20]:
                player = card.select_one(".player-name")
                prop = card.select_one(".prop-line")
                if player and prop:
                    expert_picks.append({
                        "player": player.text.strip(),
                        "prop": prop.text.strip(),
                        "source": "Pickswise",
                        "date": datetime.now().strftime("%m/%d/%Y")
                    })
    except Exception as e:
        print(f"Scrape error: {e}")

    # Count consensus
    consensus = {}
    for pick in expert_picks:
        key = f"{pick['player']} {pick['prop']}"
        consensus[key] = consensus.get(key, 0) + 1

    # Only keep props with 3+ experts agreeing
    best = [k for k,v in consensus.items() if v >= 3]
    return best

# To run it: python scraper.py
if __name__ == "__main__":
    import asyncio
    print(asyncio.run(scrape_expert_picks()))
