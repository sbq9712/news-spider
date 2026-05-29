from __future__ import annotations

import re
from urllib.parse import urlparse

from .generic import GenericListingScraper


class VoltaFoundationScraper(GenericListingScraper):
    link_selectors = (
        "article a[href]",
        "[class*='news'] a[href]",
        "main a[href]",
    )

    article_path_re = re.compile(r"^/[^/?#]+/?$")
    listing_paths = {
        "/battery-news",
    }

    def discover_article_urls(self, limit: int) -> list[str]:
        urls = super().discover_article_urls(limit * 4)
        filtered: list[str] = []
        seen = set()
        for url in urls:
            parsed = urlparse(url)
            if parsed.netloc.lower().lstrip("www.") != "volta.foundation":
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
