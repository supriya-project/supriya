import datetime
import os

import supriya

### SPHINX ###

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    # "sphinx.ext.viewcode",
    "sphinxext.opengraph",
    "uqbar.sphinx.api",
    "uqbar.sphinx.book",
    "uqbar.sphinx.inheritance",
    "sphinx_immaterial",
]

add_module_names = False
copyright = f"2014-{datetime.date.today().year}, Josiah Wolf Oberholtzer"
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
    "uqbar": ("http://josiahwolfoberholtzer.com/uqbar", None),
}

### OPENGRAPH ###

ogp_site_url = "https://josiahwolfoberholtzer.com/supriya/"

### TODO ###

todo_include_todos = True

### UQBAR API ###

uqbar_api_member_documenter_classes = [
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.ImmaterialClassDocumenter",
]
uqbar_api_module_documenter_class = "uqbar.apis.ImmaterialModuleDocumenter"
uqbar_api_omit_root = True
uqbar_api_root_documenter_class = "uqbar.apis.SummarizingRootDocumenter"
uqbar_api_source_paths = supriya.__path__
uqbar_api_title = "Supriya API Reference"

### UQBAR BOOK ###

uqbar_book_console_setup = [
    "import supriya"
]
uqbar_book_console_teardown = [
    "for server in tuple(supriya.Server._servers):",
    "    server._shutdown()",
    "",
    "supriya.scsynth.kill()",
]
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
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
]
html_domain_indices = True
html_favicon = "favicon.ico"
html_js_files = []
html_logo = "icon.svg"
html_static_path = ["_static"]
html_theme = "sphinx_immaterial"
html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
    },
    "site_url": "https://josiahwolfoberholtzer.com/supriya/",
    "repo_url": "https://github.com/josiah-wolf-oberholtzer/supriya/",
    "repo_name": "supriya",
    "repo_type": "github",
    "edit_uri": "blob/main/docs",
    "globaltoc_collapse": True,
    "features": [
        # "header.autohide",
        "navigation.expand",
        # "navigation.instant",
        # "navigation.sections",
        "navigation.tabs",
        "navigation.top",
        # "search.highlight",
        # "search.share",
        # "toc.integrate",
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
