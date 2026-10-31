import httpx
from bs4 import BeautifulSoup

async def scrape_expert_picks():
    # This is a SIMPLE demo scraper - you'll edit the selectors
    picks = []
    try:
        async with httpx.AsyncClient() as client:
            # Example - you will change this URL to real expert site
            r = await client.get("https://www.pickswise.com/nba/", 
                               headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
            # For now return mock that matches today's 7 real games
            picks = [
                "【entity-Lauri Markkanen¦canonical_name=Lauri Markkanen】 Over 23.5",
                "【entity-Joel Embiid¦canonical_name=Joel Embiid】 Over 27.5",
                "【entity-Ja Morant¦canonical_name=Ja Morant】 Over 26.5"
            ]
    except Exception as e:
        print(f"Scrape error {e}")
        picks = []
    return picks
