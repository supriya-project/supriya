import abjad
import supriya
import os
import sphinx_rtd_theme
from docutils import nodes


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    #'abjad.docs.ext.abjadbook',
    'uqbar.sphinx.api',
    'uqbar.sphinx.inheritance',
    'uqbar.sphinx.style',
    ]

uqbar_api_title = 'Supriya API'
uqbar_api_source_paths = ['supriya']
uqbar_api_root_documenter_class = 'uqbar.apis.SummarizingRootDocumenter'
uqbar_api_module_documenter_class = 'uqbar.apis.SummarizingModuleDocumenter'
uqbar_api_member_documenter_classes = [
    'uqbar.apis.FunctionDocumenter',
    'uqbar.apis.SummarizingClassDocumenter',
    ]

doctest_path = [
    os.path.abspath(abjad.__path__[0]),
    os.path.abspath(supriya.__path__[0]),
    ]

abjadbook_global_setup = r'''
from abjad import *
from supriya import *
'''

abjadbook_global_cleanup = r'''
for server in servertools.Server._servers.values():
    server.quit()

'''

doctest_global_setup = r'''
from abjad import *
from supriya import *
'''

doctest_global_cleanup = r'''
for server in servertools.Server._servers.values():
    server.quit()
'''

doctest_test_doctest_blocks = True

abjadbook_console_module_names = ('supriya',)

nodes.doctest_block = nodes.literal_block

intersphinx_mapping = {
    'abjad': ('http://abjad.mbrsi.org', None),
    'python': ('http://docs.python.org/3.6', None),
    }

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'Supriya'
copyright = u'2014, Josiah Wolf Oberholtzer'

version = '0.1'

release = '0.1'

exclude_patterns = []

pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {
    'collapse_navigation': True,
    'navigation_depth': -1,
    'sticky_navigation': True,
    'style_external_links': True,
    'titles_only': True,
}

html_static_path = ['_static']

htmlhelp_basename = 'Supriyadoc'

latex_elements = {
    'inputenc': r'\usepackage[utf8x]{inputenc}',
    'utf8extra': '',

    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': r'''
\usepackage{upquote}
\pdfminorversion=5
\setcounter{tocdepth}{2}
\definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
\definecolor{VerbatimBorderColor}{rgb}{1.0,1.0,1.0}
\hypersetup{unicode=true}
    ''',
    }

latex_documents = [
    (
        'index',
        'Supriya.tex',
        u'Supriya Documentation',
        u'Josiah Wolf Oberholtzer',
        'manual',
        ),
    ]

latex_use_parts = True

latex_domain_indices = False

man_pages = [
    (
        'index',
        'supriya',
        u'Supriya Documentation',
        [u'Josiah Wolf Oberholtzer'],
        1,
        )
    ]

texinfo_documents = [
    (
        'index',
        'Supriya',
        u'Supriya Documentation',
        u'Josiah Wolf Oberholtzer',
        'Supriya',
        'One line description of project.',
        'Miscellaneous',
        ),
    ]

graphviz_dot_args = ['-s32']
graphviz_output_format = 'svg'
