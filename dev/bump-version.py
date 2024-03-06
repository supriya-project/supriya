import argparse
import datetime
import re
from pathlib import Path


def calculate_new_version_info(old_version_name: str) -> tuple[int, int, int]:
    old_year, old_month, old_beta = [
        int(x) for x in re.match(r"v?(\d+).(\d+)b(\d+)", old_version_name).groups()
    ]
    now = datetime.datetime.now(datetime.UTC)
    new_year, new_month, new_beta = int(str(now.year)[2:]), now.month, 0
    if (old_year, old_month) == (new_year, new_month):
        new_beta = old_beta + 1
    return new_year, new_month, new_beta


def rewrite_version_file(year: int, month: int, beta: int) -> None:
    path = Path(__file__).parent.parent / "supriya" / "_version.py"
    text = path.read_text()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("__version_info__ ="):
            lines[i] = f'__version_info__ = ({year}, "{month}b{beta}")'
    path.write_text("\n".join(lines))


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("release")
    return parser


def run():
    parser = build_parser()
    parsed_args = parser.parse_args()
    year, month, beta = calculate_new_version_info(parsed_args.release)
    rewrite_version_file(year, month, beta)
    print(f"{year}.{month}b{beta}", end="")


if __name__ == "__main__":
    run()
