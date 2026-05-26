from __future__ import annotations

from abc import ABC, abstractmethod

from ..http_client import HttpClient
from ..load_sources import Source


class BaseScraper(ABC):
    def __init__(self, client: HttpClient, source: Source) -> None:
        self.client = client
        self.source = source

    @abstractmethod
    def scrape(self, limit: int = 20) -> list[dict]:
        """Return normalized article dictionaries."""
