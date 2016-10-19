# -*- coding: utf-8 -*-
from abjad.tools import documentationtools


class SupriyaDocumentationManager(documentationtools.DocumentationManager):
    api_directory_name = 'api'
    api_title = 'Supriya API'
    root_package_name = 'supriya'
    source_directory_path_parts = ('docs', 'source')
    tools_packages_package_path = 'supriya.tools'
