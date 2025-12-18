from src.csv_profiler.io import read_csv_rows
from src.csv_profiler.profile import basic_profile
from src.csv_profiler.render import write_json, write_markdown
from src.csv_profiler.strings import slugify
from src.csv_profiler.cli import app
def main() -> None: 
    rows = read_csv_rows("data/sample.csv")
    report = basic_profile(rows)
    write_json(report ,"outputs/report.json")
    write_markdown(report, "outputs/report.md")
    print(slugify("My Report 01"))
    print("Wrote outputs/report.json and outputs/report.md")
    #app()

if __name__ == "__main__": 
    main()