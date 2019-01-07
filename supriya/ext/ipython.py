from xml.dom import minidom  # type: ignore

import IPython.core.display  # type: ignore

from supriya.graphing import Grapher


def load_ipython_extension(ipython):
    patch_grapher()


def patch_grapher():
    def get_format(self):
        return "svg"

    def open_output_path(self, output_path):
        with output_path.open() as file_pointer:
            contents = file_pointer.read()
        delete_attributes = True
        document = minidom.parseString(contents)
        svg_element = document.getElementsByTagName("svg")[0]
        view_box = svg_element.getAttribute("viewBox")
        view_box = [float(_) for _ in view_box.split()]
        if delete_attributes:
            if svg_element.attributes.get("height", None):
                del (svg_element.attributes["height"])
            if svg_element.attributes.get("width", None):
                del (svg_element.attributes["width"])
        else:
            height = "{}pt".format(int(view_box[-1] * 0.6))
            width = "{}pt".format(int(view_box[-2] * 0.6))
            svg_element.setAttribute("height", height)
            svg_element.setAttribute("width", width)
        svg_element.setAttribute("preserveAspectRatio", "xMinYMin")
        contents = document.toprettyxml()
        IPython.core.display.display_svg(contents, raw=True)

    Grapher.get_format = get_format
    Grapher.open_output_path = open_output_path
