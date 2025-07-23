import datetime
import os
import subprocess

import supriya

### GIT INFO

git_branch = (
    subprocess.run(
        "git rev-parse --abbrev-ref HEAD".split(),
        capture_output=True,
        check=True,
        text=True,
    )
).stdout.strip()

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
]

add_module_names = False
copyright = f"2014-{datetime.date.today().year}, Joséphine Wolf Oberholtzer"
exclude_patterns = []
extlinks = {
    "github-tree": (
        f"https://github.com/supriya-project/supriya/tree/{git_branch}/%s",
        "%s",
    )
}
htmlhelp_basename = "Supriyadoc"
language = "en"
master_doc = "index"
project = "Supriya"
pygments_style = "sphinx"
rst_epilog = """
.. _Chocolatey: https://docs.chocolatey.org/
.. _Cython: https://cython.org/
.. _FFmpeg: https://ffmpeg.org/
.. _GitHub: https://github.com/supriya-project/supriya
.. _Graphviz: http://graphviz.org/
.. _Homebrew: http://brew.sh/
.. _IPython: https://ipython.org/
.. _LAME: https://lame.sourceforge.io/
.. _PyPI: https://pypi.python.org/pypi
.. _Python: https://www.python.org/
.. _Sphinx: https://www.sphinx-doc.org/
.. _SuperCollider: http://supercollider.github.io/
.. _Supriya: https://github.com/supriya-project/supriya
.. _aiohttp: https://docs.aiohttp.org/
.. _libsndfile: http://www.mega-nerd.com/libsndfile/
.. _mypy: https://mypy-lang.org/
.. _pip: https://pip.pypa.io/en/stable/
.. _pymonome: https://github.com/artfwo/pymonome
.. _pytest: https://docs.pytest.org/en/stable/
.. _python-prompt-toolkit: https://python-prompt-toolkit.readthedocs.io/
.. _python-rtmidi: https://github.com/SpotlightKid/python-rtmidi
.. _ruff: https://docs.astral.sh/ruff/
.. _virtualenv: https://readthedocs.org/projects/virtualenv/
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
.. _wavefile: https://pypi.python.org/pypi/wavefile/
"""
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
        "content.action.view",
        "content.tabs.link",
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
    "version_dropdown": False,
}
html_title = "Supriya"
html_use_index = True
object_description_options = [
    ("py:.*", dict(include_fields_in_toc=False)),  # Hide "Parameters" in TOC
    ("py:parameter", dict(include_in_toc=False)),  # Hide "p" parameter entries in TOC
    ("py:exception", {"toc_icon_class": "data", "toc_icon_text": "X"}),
]
sphinx_immaterial_custom_admonitions = [
    {
        "name": "editorial",
        "color": (236, 64, 11),
        "icon": "fontawesome/solid/face-tired",
    },
]
