from __future__ import annotations

from .generic import GenericListingScraper


class BatteryTechOnlineScraper(GenericListingScraper):
    link_selectors = (
        "article a[href]",
        ".card a[href]",
        ".views-row a[href]",
        "h2 a[href]",
        "h3 a[href]",
    )
