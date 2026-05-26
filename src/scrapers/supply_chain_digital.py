from __future__ import annotations

from .generic import GenericListingScraper


class SupplyChainDigitalScraper(GenericListingScraper):
    link_selectors = (
        "article a[href]",
        ".teaser a[href]",
        ".card a[href]",
        "h2 a[href]",
        "h3 a[href]",
    )
