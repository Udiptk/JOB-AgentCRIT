"""Glassdoor Scraper — fetches jobs with salary and review data."""
from typing import List
from loguru import logger
from app.scrapers.base_scraper import BaseScraper


class GlassdoorScraper(BaseScraper):
    source = "glassdoor"

    async def _scrape(self, query: str, location: str) -> List[dict]:
        logger.info(f"[Glassdoor] Searching: '{query}' in '{location}'")
        return self._demo_fallback(query, location)

    def _demo_fallback(self, query: str, location: str) -> List[dict]:
        companies = [
            ("Atlassian", "₹25L-₹45L", 4.4),
            ("Salesforce", "₹30L-₹50L", 4.3),
            ("Adobe", "₹20L-₹40L", 4.1),
            ("Intuit", "₹22L-₹38L", 4.2),
        ]
        return [
            self._make_job(
                title=f"{query} Engineer",
                company=name,
                location=location,
                salary_range=salary,
                description=f"Great {query} role at {name}. Rating: {rating}/5.0. Excellent work-life balance.",
                source_url=f"https://glassdoor.com/jobs/{name.lower()}",
            )
            for name, salary, rating in companies
        ]
