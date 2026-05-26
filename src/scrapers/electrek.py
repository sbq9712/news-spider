from __future__ import annotations

from .generic import GenericListingScraper


class ElectrekScraper(GenericListingScraper):
    link_selectors = (
        "article h1 a[href]",
        "article h2 a[href]",
        ".post-title a[href]",
        ".entry-title a[href]",
    )
