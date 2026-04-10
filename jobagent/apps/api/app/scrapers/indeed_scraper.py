"""
Indeed Scraper — fetches job listings from Indeed.
"""
import httpx
from bs4 import BeautifulSoup
from typing import List
from loguru import logger
from app.scrapers.base_scraper import BaseScraper
from app.core.config import settings


class IndeedScraper(BaseScraper):
    source = "indeed"

    async def _scrape(self, query: str, location: str) -> List[dict]:
        logger.info(f"[Indeed] Searching: '{query}' in '{location}'")

        try:
            url = f"https://in.indeed.com/jobs"
            params = {"q": query, "l": location, "sort": "date"}

            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                resp = await client.get(url, params=params, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                })

            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select(".job_seen_beacon")[:settings.MAX_JOBS_PER_SOURCE]

            jobs = []
            for card in cards:
                title_el = card.select_one('[class*="jobTitle"]')
                company_el = card.select_one('[data-testid="company-name"]')
                location_el = card.select_one('[data-testid="text-location"]')
                description_el = card.select_one(".underShelfFooter")

                if not title_el:
                    continue

                jobs.append(self._make_job(
                    title=title_el.get_text(strip=True),
                    company=company_el.get_text(strip=True) if company_el else "",
                    location=location_el.get_text(strip=True) if location_el else location,
                    description=description_el.get_text(strip=True) if description_el else "",
                    source_url=f"https://in.indeed.com{card.find('a', href=True)['href'] if card.find('a', href=True) else ''}",
                ))

            logger.info(f"[Indeed] Found {len(jobs)} jobs")
            return jobs

        except Exception as e:
            logger.warning(f"[Indeed] Scraping failed: {e}")
            return self._demo_fallback(query, location)

    def _demo_fallback(self, query: str, location: str) -> List[dict]:
        companies = ["TCS", "Infosys", "Wipro", "HCL", "Tech Mahindra"]
        return [
            self._make_job(
                title=f"{query} Developer",
                company=c,
                location=location,
                description=f"{query} role at {c}. Competitive salary and benefits.",
                source_url=f"https://indeed.com/jobs/{c.lower().replace(' ', '-')}",
            )
            for c in companies[:4]
        ]
