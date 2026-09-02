import datetime
import os
import subprocess
import sys
from pathlib import Path

import supriya

repo_root = Path(__file__).parent / ".." / ".."
sys.path.append(str(repo_root))

import examples

### GIT INFO

git_branch = (
    subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        check=True,
        text=True,
    )
).stdout.strip()

if os.environ.get("CI"):
    git_branch = os.environ.get("GITHUB_HEAD_REF") or os.environ.get("GITHUB_REF_NAME")

### SPHINX ###

extensions = [
    # "sphinx_toolbox.more_autodoc.typevars",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinxext.opengraph",
    "uqbar.sphinx.api",
    "uqbar.sphinx.book",
    "uqbar.sphinx.inheritance",
    "sphinx_immaterial",
    "sphinx_immaterial.theme_result",
]

add_module_names = False
copyright = f"2014-{datetime.datetime.now(tz=datetime.timezone.utc).date().year}, Joséphine Wolf Oberholtzer"
exclude_patterns = []
extlinks = {
    "github-blob": (
        f"https://github.com/supriya-project/supriya/blob/{git_branch}/%s",
        "%s",
    ),
    "github-tree": (
        f"https://github.com/supriya-project/supriya/tree/{git_branch}/%s",
        "%s",
    ),
}
htmlhelp_basename = "Supriyadoc"
language = "en"
master_doc = "index"
project = "Supriya"
pygments_style = "sphinx"
rst_epilog = """
.. _Chocolatey: https://docs.chocolatey.org/
.. _Cython: https://cython.org/
.. _Homebrew: https://brew.sh/
.. _Jupyter: https://jupyter.org/
.. _Python: https://www.python.org/
.. _aiohttp: https://docs.aiohttp.org/en/stable/
.. _joséphine: https://josephine-wolf-oberholtzer.com/
.. _libsndfile: https://www.mega-nerd.com/libsndfile/
.. _my: https://josephine-wolf-oberholtzer.com/
.. _mypy: https://mypy-lang.org/
.. _pymonome: https://github.com/artfwo/pymonome
.. _pynput: https://github.com/moses-palmer/pynput
.. _python-prompt-toolkit: https://python-prompt-toolkit.readthedocs.io/en/master/
.. _python-rtmidi: https://spotlightkid.github.io/python-rtmidi/
.. _ruff: https://docs.astral.sh/ruff/
.. _sphinx-immaterial: https://sphinx-immaterial.readthedocs.io/en/latest/
.. _uqbar.sphinx.api: https://supriya-project.github.io/uqbar/api/uqbar/sphinx/api.html#module-uqbar.sphinx.api
.. _uqbar.sphinx.book: https://supriya-project.github.io/uqbar/api/uqbar/sphinx/book.html#module-uqbar.sphinx.book
.. _uqbar: https://supriya-project.github.io/uqbar/index.html
"""
source_suffix = ".rst"
suppress_warnings = ["ref.param"]
templates_path = ["_templates"]
version = release = supriya.__version__

### GRAPHVIZ ###

graphviz_dot_args = ["-s32"]
graphviz_output_format = "svg"

### INTERSPHINX ###

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "pynput": ("https://pynput.readthedocs.io/en/latest/", None),
    "rtmidi": ("https://spotlightkid.github.io/python-rtmidi/", None),
    "uqbar": ("https://supriya-project.github.io/uqbar/", None),
}

## LINKCHECK ###

linkcheck_ignore = [
    # she always 403s but we love her anyways
    "https://lame.sourceforge.io/",
    "https://www.trevorbaca.com/",
]

### OPENGRAPH ###

ogp_site_url = "https://supriya-project.github.io/supriya/"
ogp_image = "icon-black.png"

### TODO ###

todo_include_todos = True

### UQBAR API ###

uqbar_api_member_documenter_classes = [
    # "supriya.ext.book.TypeVarDocumenter",
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.ImmaterialClassDocumenter",
]
uqbar_api_module_documenter_class = "uqbar.apis.ImmaterialModuleDocumenter"
uqbar_api_omit_root = True
uqbar_api_root_documenter_class = "uqbar.apis.SummarizingRootDocumenter"
uqbar_api_source_paths = [*supriya.__path__, *examples.__path__]
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
    "analytics": {
        "provider": "google",
        "property": "G-6LPCB5FX1J",
    },
    "icon": {"repo": "fontawesome/brands/github"},
    "site_url": "https://supriya-project.github.io/supriya/",
    "repo_url": "https://github.com/supriya-project/supriya/",
    "repo_name": "supriya",
    "edit_uri": "blob/main/docs",
    "globaltoc_collapse": False,
    "features": [
        "content.action.view",
        "content.tabs.link",
        "content.tooltips",
        "navigation.footer",
        "navigation.tabs",
        "navigation.top",
        "toc.follow",
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
    "status": {
        "provisional": {
            "icon": "octicons/beaker-16",
            "title": "Provisional labs feature",
        },
        "under-construction": {
            "icon": "material/alert",
            "title": "Under construction",
        },
    },
    "version_dropdown": False,
}
html_title = "Supriya"
html_use_index = True
object_description_options = [
    ("py:.*", {"include_fields_in_toc": False}),  # Hide "Parameters" in TOC
    ("py:parameter", {"include_in_toc": False}),  # Hide "p" parameter entries in TOC
    ("py:exception", {"toc_icon_class": "data", "toc_icon_text": "X"}),
]
sphinx_immaterial_custom_admonitions = [
    {
        "name": "editorial",
        "color": (236, 64, 11),
        "icon": "fontawesome/solid/face-tired",
    },
    {
        "name": "self-criticism",
        "color": (236, 64, 11),
        "icon": "fontawesome/regular/face-grin-beam-sweat",
    },
]
