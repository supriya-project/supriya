#! /usr/bin/env python
import os
import supriya
from abjad.tools import documentationtools


class SupriyaAPIGenerator(documentationtools.AbjadAPIGenerator):
    r'''API generator for the supriya package.
    '''

    _api_title = 'Supriya API'

    @property
    def docs_api_index_path(self):
        return os.path.join(
            supriya.__path__[0],
            'docs',
            'source',
            'index.rst',
            )

    @property
    def path_definitions(self):
        tools_code_path = os.path.join(
            supriya.__path__[0],
            'tools',
            )
        tools_docs_path = os.path.join(
            supriya.__path__[0],
            'docs',
            'source',
            'tools',
            )
        tools_package_prefix = 'supriya.tools.'
        tools_triple = (
            tools_code_path,
            tools_docs_path,
            tools_package_prefix,
            )
        demos_code_path = os.path.join(
            supriya.__path__[0],
            'demos',
            )
        demos_docs_path = os.path.join(
            supriya.__path__[0],
            'docs',
            'source',
            'demos',
            )
        demos_package_prefix = 'supriya.demos.'
        demos_triple = (
            demos_code_path,
            demos_docs_path,
            demos_package_prefix,
            )
        all_triples = (tools_triple, demos_triple)
        return all_triples

    @property
    def root_package(self):
        return 'supriya'

    @property
    def tools_package_path_index(self):
        return 2


def _build_api():
    SupriyaAPIGenerator()()


if __name__ == '__main__':
    _build_api()
