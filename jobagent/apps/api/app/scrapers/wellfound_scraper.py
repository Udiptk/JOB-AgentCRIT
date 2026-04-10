"""Wellfound (AngelList) Scraper — startup jobs."""
from typing import List
from loguru import logger
from app.scrapers.base_scraper import BaseScraper


class WellfoundScraper(BaseScraper):
    source = "wellfound"

    async def _scrape(self, query: str, location: str) -> List[dict]:
        logger.info(f"[Wellfound] Searching: '{query}' in '{location}'")
        return self._demo_fallback(query, location)

    def _demo_fallback(self, query: str, location: str) -> List[dict]:
        startups = [
            ("Sarvam AI", "Series A", "₹20L-₹40L"),
            ("Krutrim", "Seed", "₹18L-₹35L"),
            ("Pi42", "Seed", "₹15L-₹28L"),
            ("Karya", "Series B", "₹22L-₹38L"),
        ]
        return [
            self._make_job(
                title=f"{query} Engineer",
                company=name,
                location=location,
                job_type="full-time",
                salary_range=salary,
                description=(
                    f"Join {name} ({stage} startup). Build {query} systems from scratch "
                    f"with a small, high-impact team. Equity included."
                ),
                source_url=f"https://wellfound.com/company/{name.lower().replace(' ', '-')}",
            )
            for name, stage, salary in startups
        ]
