import supriya
import sphinx_rtd_theme


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    # "sphinx_autodoc_typehints",
    "uqbar.sphinx.api",
    "uqbar.sphinx.book",
    "uqbar.sphinx.inheritance",
    "uqbar.sphinx.style",
]

copyright = "2014, Josiah Wolf Oberholtzer"
exclude_patterns = []
graphviz_dot_args = ["-s32"]
graphviz_output_format = "svg"
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": True,
    "navigation_depth": -1,
    "sticky_navigation": True,
    "style_external_links": True,
    "titles_only": True,
}
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
htmlhelp_basename = "Supriyadoc"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "uqbar": ("http://josiahwolfoberholtzer.com/uqbar", None),
}
master_doc = "index"
project = "Supriya"
pygments_style = "sphinx"
version = release = supriya.__version__
source_suffix = ".rst"
templates_path = ["_templates"]

uqbar_api_member_documenter_classes = [
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.SummarizingClassDocumenter",
]
uqbar_api_module_documenter_class = "uqbar.apis.SummarizingModuleDocumenter"
uqbar_api_omit_root = True
uqbar_api_root_documenter_class = "uqbar.apis.SummarizingRootDocumenter"
uqbar_api_source_paths = supriya.__path__
uqbar_api_title = "Supriya API Reference"
uqbar_book_console_setup = [
    "import supriya"
]
uqbar_book_console_teardown = [
    "for server in supriya.Server._servers:",
    "    server.quit()",
    "",
    "supriya.scsynth.kill()",
]

uqbar_book_extensions = [
    "uqbar.book.extensions.GraphExtension",
    "supriya.ext.book.RenderExtension",
]
uqbar_book_strict = False
uqbar_book_use_black = True
uqbar_book_use_cache = True
