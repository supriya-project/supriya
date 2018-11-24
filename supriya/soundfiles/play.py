import subprocess


def play(expr, **kwargs):
    if not hasattr(expr, "__render__"):
        raise ValueError(expr)
    output_file_path = expr.__render__(**kwargs)
    command = 'open -a "QuickTime Player" {}'.format(output_file_path)
    subprocess.call(command, shell=True)
