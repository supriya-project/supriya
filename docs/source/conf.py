import datetime
import os

import supriya

### SPHINX ###

extensions = [
    "sphinx_toolbox.more_autodoc.typevars",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinx_immaterial",
    "sphinxext.opengraph",
    "uqbar.sphinx.api",
    "uqbar.sphinx.book",
    "uqbar.sphinx.inheritance",
]

add_module_names = False
copyright = f"2014-{datetime.date.today().year}, Joséphine Wolf Oberholtzer"
exclude_patterns = []
htmlhelp_basename = "Supriyadoc"
language = "en"
master_doc = "index"
project = "Supriya"
pygments_style = "sphinx"
source_suffix = ".rst"
templates_path = ["_templates"]
version = release = supriya.__version__

### GRAPHVIZ ###

graphviz_dot_args = ["-s32"]
graphviz_output_format = "svg"

### INTERSPHINX ###

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "uqbar": ("http://supriya-project.github.io/uqbar", None),
}

### OPENGRAPH ###

ogp_site_url = "https://supriya-project.github.io/supriya/"

### TODO ###

todo_include_todos = True

### UQBAR API ###

uqbar_api_member_documenter_classes = [
    "supriya.ext.book.TypeVarDocumenter",
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.ImmaterialClassDocumenter",
]
uqbar_api_module_documenter_class = "uqbar.apis.ImmaterialModuleDocumenter"
uqbar_api_omit_root = True
uqbar_api_root_documenter_class = "uqbar.apis.SummarizingRootDocumenter"
uqbar_api_source_paths = supriya.__path__
uqbar_api_title = "Supriya API Reference"

### UQBAR BOOK ###

uqbar_book_console_setup = ["import supriya"]
uqbar_book_console_teardown = """\
import asyncio

for server in tuple(supriya.Server._contexts):
    if asyncio.iscoroutine(result := server._shutdown()):
        await result

""".splitlines()
uqbar_book_extensions = [
    "uqbar.book.extensions.GraphExtension",
    "supriya.ext.book.PlayExtension",
    "supriya.ext.book.PlotExtension",
]
uqbar_book_strict = os.environ.get("CI") == "true"
uqbar_book_use_black = True
uqbar_book_use_cache = False

### THEME ###

html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
]
html_domain_indices = True
html_favicon = "favicon.ico"
html_js_files = []
html_logo = "icon.svg"
html_static_path = ["_static"]
html_theme = "sphinx_immaterial"
html_theme_options = {
    "icon": {"repo": "fontawesome/brands/github"},
    "site_url": "https://supriya-project.github.io/supriya/",
    "repo_url": "https://github.com/supriya-project/supriya/",
    "repo_name": "supriya",
    "edit_uri": "blob/main/docs",
    "globaltoc_collapse": False,
    "features": [
        "navigation.tabs",
        "navigation.top",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "blue-grey",
            "accent": "lime",
            "toggle": {
                "icon": "material/toggle-switch",
                "name": "Switch to light mode",
            },
        },
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "indigo",
            "accent": "teal",
            "toggle": {
                "icon": "material/toggle-switch-off-outline",
                "name": "Switch to dark mode",
            },
        },
    ],
    "version_dropdown": False,
}
html_title = "Supriya"
html_use_index = True
object_description_options = [
    ("py:.*", dict(include_fields_in_toc=False)),  # Hide "Parameters" in TOC
    ("py:parameter", dict(include_in_toc=False)),  # Hide "p" parameter entries in TOC
    ("py:exception", {"toc_icon_class": "data", "toc_icon_text": "X"}),
]
