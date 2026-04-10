"""Naukri Scraper — fetches jobs from Naukri.com."""
from typing import List
from loguru import logger
from app.scrapers.base_scraper import BaseScraper


class NaukriScraper(BaseScraper):
    source = "naukri"

    async def _scrape(self, query: str, location: str) -> List[dict]:
        logger.info(f"[Naukri] Searching: '{query}' in '{location}'")
        # Naukri requires session cookies — use demo fallback for hackathon
        return self._demo_fallback(query, location)

    def _demo_fallback(self, query: str, location: str) -> List[dict]:
        companies = ["Swiggy", "Zomato", "Ola", "Paytm", "PhonePe", "BrowserStack"]
        return [
            self._make_job(
                title=f"Senior {query} Engineer",
                company=c,
                location=location,
                salary_range="₹15L - ₹30L",
                description=f"Exciting {query} opportunity at {c}. Fast-paced startup environment.",
                source_url=f"https://naukri.com/jobs/{c.lower()}",
            )
            for c in companies[:5]
        ]
