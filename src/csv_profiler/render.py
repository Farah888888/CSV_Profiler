from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime 


def write_json(report:dict, path: str | Path) ->None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True) 
    path.write_text(json.dumps(report,indent=2, ensure_ascii=False) + "\n")
    

def write_markdown(report, path):
    path = Path(path)
    path.parent.mkdir(parents= True , exist_ok= True)

    rows = report["summary"]["rows"]
    ncols = report["summary"]["columns"]
    columns = report.get("columns", [])
    missing = report.get("missing", {})
    missing_pct = ((missing/rows)*100) if rows else 0.0

    md = md_header(report)
    lines:list[str] = []
    lines.append(md)
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- Rows: **{report.get('rows', 0)}**")

    lines.append("| name | type | missing | missing_pct | unique |")
    lines.append("|---|---:|---:|---:|---:|")
    lines.extend([
        f"| {c['name']} | {c['type']} | {c['missing']} | {c['missing_pct']:.1f}% | {c['unique']} |"
        for c in report["columns"]
    ])
    
    for col in columns:
        name = col["name"]
        ctype = col["type"]
        missing_count = col.get("missing", 0)
        unique = col.get("unique", 0)
        missing_pct = (missing_count / rows * 100) if rows else 0.0

        lines.append(f"| {name} | {ctype} | {missing_pct:.1f}% | {unique} |")

    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")