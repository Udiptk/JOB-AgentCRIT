"""
LinkedIn Scraper — fetches job listings from LinkedIn Jobs.
Uses httpx + BeautifulSoup for demo. Upgrade to Playwright for full automation.
"""
import httpx
from bs4 import BeautifulSoup
from typing import List
from loguru import logger
from app.scrapers.base_scraper import BaseScraper
from app.core.config import settings


class LinkedInScraper(BaseScraper):
    source = "linkedin"

    async def _scrape(self, query: str, location: str) -> List[dict]:
        logger.info(f"[LinkedIn] Searching: '{query}' in '{location}'")

        url = "https://www.linkedin.com/jobs/search/"
        params = {
            "keywords": query,
            "location": location,
            "f_TPR": "r86400",  # Last 24 hours
            "count": settings.MAX_JOBS_PER_SOURCE,
        }

        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                resp = await client.get(url, params=params, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                })

            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select(".jobs-search__results-list li")[:settings.MAX_JOBS_PER_SOURCE]

            jobs = []
            for card in cards:
                title_el = card.select_one(".base-search-card__title")
                company_el = card.select_one(".base-search-card__subtitle")
                location_el = card.select_one(".job-search-card__location")
                link_el = card.select_one("a.base-card__full-link")

                if not title_el:
                    continue

                jobs.append(self._make_job(
                    title=title_el.get_text(strip=True),
                    company=company_el.get_text(strip=True) if company_el else "",
                    location=location_el.get_text(strip=True) if location_el else location,
                    source_url=link_el["href"] if link_el else "",
                    description="",
                ))

            logger.info(f"[LinkedIn] Found {len(jobs)} jobs")
            return jobs

        except Exception as e:
            logger.warning(f"[LinkedIn] Scraping failed: {e}")
            return self._demo_fallback(query, location)

    def _demo_fallback(self, query: str, location: str) -> List[dict]:
        """Return realistic demo data when scraping fails."""
        base_companies = ["Google", "Microsoft", "Amazon", "Flipkart", "Razorpay", "CRED", "Zepto"]
        return [
            self._make_job(
                title=f"{query} Engineer",
                company=company,
                location=location,
                description=f"Join {company} as a {query} Engineer. Work on cutting-edge systems.",
                source_url=f"https://linkedin.com/jobs/{company.lower()}",
            )
            for company in base_companies[:5]
        ]
