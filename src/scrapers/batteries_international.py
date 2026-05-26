from __future__ import annotations

from .generic import GenericListingScraper


class BatteriesInternationalScraper(GenericListingScraper):
    link_selectors = (
        "article h2 a[href]",
        ".td-module-title a[href]",
        ".entry-title a[href]",
        "h3 a[href]",
    )
