from __future__ import annotations

from .base import BaseScraper
from .batteries_international import BatteriesInternationalScraper
from .batterytechonline import BatteryTechOnlineScraper
from .electrek import ElectrekScraper
from .electrive import ElectriveScraper
from .generic import GenericListingScraper
from .pv_magazine import PVMagazineScraper
from .supply_chain_digital import SupplyChainDigitalScraper
from .volta import VoltaFoundationScraper


SCRAPER_REGISTRY: dict[str, type[BaseScraper]] = {
    "electrive": ElectriveScraper,
    "batteries international": BatteriesInternationalScraper,
    "volta foundation": VoltaFoundationScraper,
    "battery tech online": BatteryTechOnlineScraper,
    "supply chain digital": SupplyChainDigitalScraper,
    "electrek": ElectrekScraper,
    "pv magazine": PVMagazineScraper,
}


def get_scraper_class(source_name: str) -> type[BaseScraper]:
    return SCRAPER_REGISTRY.get(source_name.strip().lower(), GenericListingScraper)
