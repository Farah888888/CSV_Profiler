import typer
from pathlib import Path
app = typer.Typer()
from src.csv_profiler.profile import basic_profile
from src.csv_profiler.io import read_csv_rows

@app.command(help="Profile a file and generates an output")
def profile(
    input_path: str,
    out_dir: str = "outputs",
    report_name: str = "my-report",
):
    rows = read_csv_rows(input_path)
    report = basic_profile(rows)

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    base = slugify(report_name)
    write_json(report, str(out_path / f"{base}.json"))
    write_markdown(report, str(out_path / f"{base}.md"))

    typer.echo(f"Wrote {out_path / f'{base}.json'} and {out_path / f'{base}.md'}")
