from __future__ import annotations

from .generic import GenericListingScraper


class VoltaFoundationScraper(GenericListingScraper):
    link_selectors = (
        "article a[href]",
        "[class*='news'] a[href]",
        "main a[href]",
    )
