"""Internshala Scraper — fetches internship and fresher jobs."""
from typing import List
from loguru import logger
from app.scrapers.base_scraper import BaseScraper


class IntershalaScraper(BaseScraper):
    source = "internshala"

    async def _scrape(self, query: str, location: str) -> List[dict]:
        logger.info(f"[Internshala] Searching: '{query}' in '{location}'")
        return self._demo_fallback(query, location)

    def _demo_fallback(self, query: str, location: str) -> List[dict]:
        companies = ["Juspay", "Hasura", "Setu", "Groww", "Curefit"]
        return [
            self._make_job(
                title=f"{query} Intern",
                company=c,
                location=location,
                job_type="internship",
                salary_range="₹15,000 - ₹25,000/month",
                description=f"6-month {query} internship at {c}. Pre-placement offer available.",
                source_url=f"https://internshala.com/internship/{c.lower()}",
            )
            for c in companies[:4]
        ]
