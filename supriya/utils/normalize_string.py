import textwrap


def normalize_string(string):
    string = string.replace('\t', '    ')
    lines = string.split('\n')
    while lines and (not lines[0] or lines[0].isspace()):
        lines.pop(0)
    while lines and (not lines[-1] or lines[-1].isspace()):
        lines.pop()
    for i, line in enumerate(lines):
        lines[i] = line.rstrip()
    string = '\n'.join(lines)
    string = textwrap.dedent(string)
    return string
