from __future__ import annotations

from .generic import GenericListingScraper


class ElectriveScraper(GenericListingScraper):
    link_selectors = (
        "article h3 a[href]",
        "article h2 a[href]",
        ".post-title a[href]",
        ".entry-title a[href]",
    )
