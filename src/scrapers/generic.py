from __future__ import annotations

import logging
import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from ..article_parser import fetch_and_parse_article
from .base import BaseScraper


class GenericListingScraper(BaseScraper):
    """Conservative fallback scraper for simple news listing pages."""

    link_selectors = (
        ".recommend-content-right a[href]",
        ".recommend-content a[href]",
        ".news-list a[href]",
        ".newslist a[href]",
        ".list a[href]",
        ".list_news a[href]",
        ".list-con a[href]",
        ".listCon a[href]",
        ".channel-list a[href]",
        ".sub-list a[href]",
        ".main-list a[href]",
        "article a[href]",
        ".post a[href]",
        ".entry-title a[href]",
        "h1 a[href]",
        "h2 a[href]",
        "h3 a[href]",
        "ul li a[href]",
        "main a[href]",
        "a[href]",
    )

    article_url_patterns = (
        re.compile(r"/20\d{2}(?:\d{2})?/\d{1,2}/[^/]+\.html?$"),
        re.compile(r"/20\d{4}/[^/]+\.html?$"),
        re.compile(r"/\d{6}/\d+\.html?$"),
        re.compile(r"/t20\d{6}_\d+\.html?$"),
        re.compile(r"/article/\d+\.html?$"),
        re.compile(r"/news/[^/?#]+\.html?$"),
    )

    def discover_article_urls(self, limit: int) -> list[str]:
        result = self.client.get(self.source.url)
        if not result:
            return []

        soup = BeautifulSoup(result.text, "html.parser")
        source_host = urlparse(result.url).netloc
        source_page = result.url.rstrip("/")
        urls: list[str] = []
        seen = set()
        for selector in self.link_selectors:
            for link in soup.select(selector):
                href = link.get("href")
                title = link.get_text(" ", strip=True)
                if not href or href.startswith(("javascript:", "#", "mailto:")):
                    continue
                url = urljoin(result.url, href)
                parsed = urlparse(url)
                if parsed.scheme not in ("http", "https") or not self.same_site(parsed.netloc, source_host):
                    continue
                if url.rstrip("/") == source_page:
                    continue
                if not self.looks_like_article_url(parsed.path) and len(title) < 8:
                    continue
                if url not in seen:
                    seen.add(url)
                    urls.append(url)
                if len(urls) >= limit:
                    return urls
        return urls

    @staticmethod
    def same_site(candidate_host: str, source_host: str) -> bool:
        return candidate_host.lower().lstrip("www.") == source_host.lower().lstrip("www.")

    def looks_like_article_url(self, path: str) -> bool:
        return any(pattern.search(path) for pattern in self.article_url_patterns)

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
