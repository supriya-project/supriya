import datetime
import hashlib
import subprocess
import sys

import supriya


def graph(graphable, format_="pdf", layout="dot", verbose=False):
    return Grapher(graphable, format_=format_, layout=layout, verbose=verbose)()


class Grapher:

    ### CLASS VARIABLES ###

    _valid_layouts = ("circo", "dot", "fdp", "neato", "osage", "sfdp", "twopi")

    ### INITIALIZER ###

    def __init__(self, graphable, format_="pdf", layout="dot", verbose=False):
        self.graphable = graphable
        self.format_ = format_
        self.layout = layout
        self.verbose = verbose

    ### SPECIAL METHODS ###

    def __call__(self):
        graphviz_string = self.get_graphviz_string()
        layout = self.get_layout()
        format_ = self.get_format()
        render_prefix = self.get_render_prefix(graphviz_string)
        input_path = render_prefix.with_suffix(".dot")
        self.persist_graphviz_string(graphviz_string, input_path)
        output_path = render_prefix.with_suffix(f".{format_}")
        render_command = self.get_render_command(
            format_, input_path, layout, output_path
        )
        self.run_command(render_command, verbose=self.verbose)
        self.open_output_path(output_path)
        return output_path

    ### PUBLIC METHODS ###

    def get_format(self):
        return self.format_

    def get_graphviz_string(self):
        graphviz_graph = self.graphable.__graph__()
        return format(graphviz_graph, "graphviz")

    def get_layout(self):
        return self.layout

    def get_render_command(self, format_, input_path, layout, output_path):
        return f"{layout} -v -T {format_} -o {output_path} {input_path}"

    def get_render_prefix(self, graphviz_string):
        sha1 = hashlib.sha1()
        sha1.update(graphviz_string.encode())
        hexdigest = sha1.hexdigest()
        timestamp = (
            datetime.datetime.now()
            .isoformat()
            .split(".")[0]
            .replace(":", "")
            .replace("-", "")
        )
        file_prefix = f"{timestamp}-{hexdigest[:7]}"
        return supriya.output_path / file_prefix

    def open_output_path(self, output_path):
        viewer = "open"
        if sys.platform.lower().startswith("linux"):
            viewer = "xdg-open"
        subprocess.run(f"{viewer} {output_path}", shell=True, check=True)

    def persist_graphviz_string(self, graphviz_string, input_path):
        with input_path.open("w") as file_pointer:
            file_pointer.write(graphviz_string)

    def run_command(self, command, verbose=False):
        kwargs = dict(shell=True, check=True)
        if not verbose:
            kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        subprocess.run(command, **kwargs)
