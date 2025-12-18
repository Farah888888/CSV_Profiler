import typer
from pathlib import Path
import json
import time

from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_markdown

app = typer.Typer()


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



@app.command(help="Profile a file and generates an output")
def profile(
    input_path: str,
    out_dir: str = "outputs",
    report_name: str = "my-report",
    preview: bool = False
):
    try: 
        t0 = time.perf_counter_ns()
        rows = read_csv_rows(input_path)
        report = basic_profile(rows)
        t1 = time.perf_counter_ns()
        report["timing_ms"] = (t1-10) / 1_000_000

        out_dir.mkdir(parents = True, exist_ok = True)

        json_path = out_dir/ f"{report_name}.json"
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding ="utf-8"),
        typer.secho(f"Wrote {json_path}", fg=typer.colors.BRIGHT_BLUE)

        if preview:
            typer.echo(f"Rows: {report['n_rows']} | Cols: '{report['n_cols']} | {report['timing_ms']:.2f}ms)")
    except Exception as e:
        typer.secho(f"ERROR: {e}", fg = typer.colors.RED) 
        raise typer.Exit(code=1)
        

if __name__ == "__main__": 
    app()


