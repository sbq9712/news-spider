from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .http_client import HttpClient
from .load_sources import Source


ARTICLE_SELECTORS = (
    "article",
    ".entry-content",
    ".post-content",
    ".article-content",
    ".article-body",
    ".content",
    "main",
)

REMOVE_SELECTORS = (
    "script",
    "style",
    "noscript",
    "iframe",
    "form",
    "nav",
    "aside",
    ".share",
    ".social",
    ".newsletter",
    ".advert",
    ".advertisement",
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clean_text(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+", " ", text)).strip()


def first_meta(soup: BeautifulSoup, names: tuple[str, ...]) -> str:
    for name in names:
        tag = soup.find("meta", attrs={"property": name}) or soup.find("meta", attrs={"name": name})
        if tag and tag.get("content"):
            return tag["content"].strip()
    return ""


def extract_title(soup: BeautifulSoup) -> str:
    meta_title = first_meta(soup, ("og:title", "twitter:title"))
    if meta_title:
        return meta_title
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(" ", strip=True)
    if soup.title:
        return soup.title.get_text(" ", strip=True)
    return ""


def extract_date(soup: BeautifulSoup) -> str:
    meta_date = first_meta(
        soup,
        (
            "article:published_time",
            "datePublished",
            "pubdate",
            "publishdate",
            "date",
            "dc.date",
            "DC.date.issued",
        ),
    )
    if meta_date:
        return meta_date
    time_tag = soup.find("time")
    if time_tag:
        return (time_tag.get("datetime") or time_tag.get_text(" ", strip=True)).strip()
    return ""


def extract_body(soup: BeautifulSoup) -> str:
    for selector in REMOVE_SELECTORS:
        for tag in soup.select(selector):
            tag.decompose()

    candidates = []
    for selector in ARTICLE_SELECTORS:
        for node in soup.select(selector):
            text = clean_text(node.get_text("\n", strip=True))
            if text:
                candidates.append(text)
    if candidates:
        return max(candidates, key=len)
    return clean_text(soup.get_text("\n", strip=True))


def parse_article_html(html: str, url: str, source: Source, crawled_at: Optional[str] = None) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    canonical = first_meta(soup, ("og:url",)) or url
    link = soup.find("link", rel=lambda value: value and "canonical" in value)
    if link and link.get("href"):
        canonical = urljoin(url, link["href"])

    return {
        "title": extract_title(soup),
        "published_at": extract_date(soup),
        "content": extract_body(soup),
        "url": canonical,
        "source_name": source.name,
        "domain": source.domain,
        "sub_domain": source.sub_domain,
        "crawled_at": crawled_at or utc_now_iso(),
    }


def fetch_and_parse_article(client: HttpClient, url: str, source: Source) -> Optional[dict]:
    result = client.get(url, allow_non_html=False)
    if not result:
        return None
    article = parse_article_html(result.text, result.url, source)
    if not article["title"] and not article["content"]:
        return None
    return article
