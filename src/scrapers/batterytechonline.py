from __future__ import annotations

import re
from urllib.parse import urlparse

from .generic import GenericListingScraper


class BatteryTechOnlineScraper(GenericListingScraper):
    link_selectors = (
        "article a[href]",
        ".card a[href]",
        ".views-row a[href]",
        "h2 a[href]",
        "h3 a[href]",
    )

    article_path_re = re.compile(
        r"^/(?:battery-news|ev-batteries|stationary-batteries|battery-applications|"
        r"lithium-ion-batteries|design-manufacturing|automotive-mobility|"
        r"batteries-energy-storage)/[^/?#]+/?$"
    )
    listing_paths = {
        "/battery-news/battery-breaking-news-headlines",
    }

    def discover_article_urls(self, limit: int) -> list[str]:
        urls = super().discover_article_urls(limit * 4)
        filtered: list[str] = []
        seen = set()
        for url in urls:
            parsed = urlparse(url)
            if parsed.netloc.lower().lstrip("www.") != "batterytechonline.com":
                continue
            path = parsed.path.rstrip("/")
            if path in self.listing_paths:
                continue
            if not self.article_path_re.match(path):
                continue
            if url not in seen:
                seen.add(url)
                filtered.append(url)
            if len(filtered) >= limit:
                break
        return filtered
