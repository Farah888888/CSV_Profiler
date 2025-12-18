from __future__ import annotations

from csv import DictReader 
from pathlib import Path
import csv

def read_csv_rows(path: str | Path) -> list[dict[str, str]]: 
    path =Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    with open(path ,"r",encoding="utf-8", newline="") as f:
        reader = DictReader(f)
        rows =list(reader)

    if not rows: 
        raise ValueError("CSV has no data rows")

    return rows


