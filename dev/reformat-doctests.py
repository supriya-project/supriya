#! /usr/bin/env python

import argparse
import black
import pathlib


def black_format(lines):
    mode = black.FileMode(
        line_length=80, target_versions=[black.TargetVersion.PY36]
    )
    return black.format_str("\n".join(lines), mode=mode).splitlines()


def process_chunk(input_lines):
    whitespace, _, _ = input_lines[0].partition(">>> ")
    indent = len(whitespace)
    output_lines = black_format([
        line[indent + 4:] for line in input_lines
    ])
    for i, line in enumerate(output_lines):
        prefix = ">>> " if i == 0 else "... "
        output_lines[i] = whitespace + prefix + line
    return output_lines


def reformat_file(path: pathlib.Path):
    input_lines = path.read_text().splitlines()
    output_lines = []
    current_chunk = []
    for line in input_lines:
        if line.lstrip().startswith("... "):
            current_chunk.append(line)
        else:
            if current_chunk:
                output_lines.extend(process_chunk(current_chunk))
            if line.lstrip().startswith(">>> "):
                current_chunk[:] = [line]
            else:
                output_lines.append(line)
                current_chunk[:] = []
    if current_chunk:
        output_lines.extend(process_chunk(current_chunk))
    path.write_text("\n".join(output_lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", default=["."])
    args = parser.parse_args()
    for search_path in args.paths:
        search_path = pathlib.Path(search_path)
        if search_path.is_dir():
            for path in search_path.rglob("*.py"):
                reformat_file(path)
        else:
            reformat_file(search_path)
