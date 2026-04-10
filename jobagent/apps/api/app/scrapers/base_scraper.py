"""
Base Scraper — abstract base class all platform scrapers inherit from.
"""
from abc import ABC, abstractmethod
from typing import List
import asyncio
from app.core.config import settings


class BaseScraper(ABC):
    source: str = "unknown"

    async def search(self, query: str, location: str = "") -> List[dict]:
        """Scrape jobs and return a list of raw job dicts."""
        await asyncio.sleep(settings.SCRAPER_DELAY_SECONDS)
        return await self._scrape(query, location)

    @abstractmethod
    async def _scrape(self, query: str, location: str) -> List[dict]:
        pass

    def _make_job(self, **kwargs) -> dict:
        return {
            "source": self.source,
            "match_score": None,
            "match_reasons": [],
            "missing_skills": [],
            **kwargs,
        }
