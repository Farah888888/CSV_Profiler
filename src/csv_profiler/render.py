from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime 


def write_json(report:dict, path: str | Path) ->None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True) 
    path.write_text(json.dumps(report,indent=2, ensure_ascii=False) + "\n")
    

def write_markdown(report: dict) -> str:
    #rows = report["summary"]["rows"]
    #ncols = report["summary"]["columns"]
    #columns = report.get("columns", [])
    #missing = report.get("missing", {})
    #missing_pct = ((missing/rows)*100) if rows else 0.0

    lines:list[str] = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")

    lines.append("##Summary\n")
    lines.append(f"- Rows: **{report['n_rows']}**")
    lines.append(f"- Columns: **{report['n_cols']}**\n")

    lines.append("## Columns\n")
    lines.append("| name | type | missing | missing_pct | unique |")
    lines.append("|---|---:|---:|---:|---:|")
    lines.extend([
        f"| {c['name']} | {c['type']} | {c['missing']} | {c['missing_pct']:.1f}% | {c['unique']} |"
        for c in report["columns"]
    ])

    lines.append("\n## Notes\n")
    lines.append("- Missing values are: `''`, `n/a`, `null`, `none`, `nan` (case-insensitive)")

    return "\n".join(lines)