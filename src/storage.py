from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable


FIELDNAMES = (
    "title",
    "published_at",
    "content",
    "url",
    "source_name",
    "domain",
    "sub_domain",
    "crawled_at",
)


def load_existing_urls(jsonl_path: Path) -> set[str]:
    urls: set[str] = set()
    if not jsonl_path.exists():
        return urls
    with jsonl_path.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if item.get("url"):
                urls.add(item["url"])
    return urls


def append_jsonl(jsonl_path: Path, articles: Iterable[dict]) -> int:
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with jsonl_path.open("a", encoding="utf-8") as file:
        for article in articles:
            normalized = {key: article.get(key, "") for key in FIELDNAMES}
            file.write(json.dumps(normalized, ensure_ascii=False) + "\n")
            count += 1
    return count


def export_csv(jsonl_path: Path, csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        if not jsonl_path.exists():
            return
        with jsonl_path.open("r", encoding="utf-8") as jsonl_file:
            for line in jsonl_file:
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                writer.writerow({key: item.get(key, "") for key in FIELDNAMES})
