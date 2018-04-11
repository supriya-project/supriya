from abjad.tools import abjadbooktools


def setup(app):
    abjadbooktools.SphinxDocumentHandler.setup_sphinx_extension(app)
