@app.get("/api/expert-consensus")
async def expert_consensus():
    from scraper import scrape_expert_picks
    best = await scrape_expert_picks()
    return {"date":"10/31/2026", "consensus_picks": best, "count": len(best)}
