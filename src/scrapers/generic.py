from __future__ import annotations

import logging
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from ..article_parser import fetch_and_parse_article
from .base import BaseScraper


class GenericListingScraper(BaseScraper):
    """Conservative fallback scraper for simple news listing pages."""

    link_selectors = (
        "article a[href]",
        ".post a[href]",
        ".entry-title a[href]",
        "h1 a[href]",
        "h2 a[href]",
        "h3 a[href]",
        "main a[href]",
    )

    def discover_article_urls(self, limit: int) -> list[str]:
        result = self.client.get(self.source.url)
        if not result:
            return []

        soup = BeautifulSoup(result.text, "html.parser")
        source_host = urlparse(result.url).netloc
        urls: list[str] = []
        seen = set()
        for selector in self.link_selectors:
            for link in soup.select(selector):
                href = link.get("href")
                title = link.get_text(" ", strip=True)
                if not href or len(title) < 8:
                    continue
                url = urljoin(result.url, href)
                parsed = urlparse(url)
                if parsed.scheme not in ("http", "https") or parsed.netloc != source_host:
                    continue
                if url not in seen:
                    seen.add(url)
                    urls.append(url)
                if len(urls) >= limit:
                    return urls
        return urls

    def scrape(self, limit: int = 20) -> list[dict]:
        articles: list[dict] = []
        urls = self.discover_article_urls(limit)
        if not urls:
            logging.warning(
                "TODO scraper needed for %s: unable to identify article links from listing page. "
                "Please provide article-list CSS selectors or API details.",
                self.source.name,
            )
            return articles

        for url in urls:
            article = fetch_and_parse_article(self.client, url, self.source)
            if article:
                articles.append(article)
        return articles
