from xml.dom import minidom  # type: ignore

from IPython.core.display import display, display_svg  # type: ignore
from IPython.display import Audio  # type: ignore

from supriya.io import Grapher, Player
from supriya.soundfiles import HeaderFormat


def load_ipython_extension(ipython):
    patch_grapher()
    patch_player()


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
        display_svg(contents, raw=True)

    Grapher.get_format = get_format
    Grapher.open_output_path = open_output_path


def patch_player():
    def render(self):
        render_kwargs = self.render_kwargs
        render_kwargs["header_format"] = HeaderFormat.WAV
        return self.renderable.__render__(**render_kwargs)

    def open_output_path(self, output_path):
        display(Audio(filename=str(output_path)))

    Player.open_output_path = open_output_path
    Player.render = render
