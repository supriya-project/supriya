master_doc = "index"

extensions = ["sphinx.ext.autodoc", "uqbar.sphinx.book"]

html_static_path = ["_static"]

uqbar_book_console_setup = ["import supriya"]
uqbar_book_extensions = [
    "uqbar.book.extensions.GraphExtension",
    "supriya.ext.book.PlayExtension",
]
uqbar_book_strict = True
uqbar_book_use_black = True
