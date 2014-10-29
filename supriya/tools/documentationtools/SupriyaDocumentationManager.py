# -*- encoding: utf-8 -*-
from __future__ import print_function
import enum
import os
import shutil
import types


class SupriyaDocumentationManager(object):

    @staticmethod
    def get_tools_packages():
        import supriya.tools
        tools_packages = []
        for name in dir(supriya.tools):
            if name.startswith('_'):
                continue
            module = getattr(supriya.tools, name)
            if not isinstance(module, types.ModuleType):
                continue
            if not module.__package__.startswith(supriya.__package__):
                continue
            tools_packages.append(module)
        tools_packages.sort(key=lambda x: x.__name__)
        tools_packages = tuple(tools_packages)
        return tools_packages

    @staticmethod
    def get_tools_package_contents(tools_package):
        classes = []
        enumerations = []
        functions = []
        for name in dir(tools_package):
            if name.startswith('_'):
                continue
            object_ = getattr(tools_package, name)
            if not hasattr(object_, '__module__'):
                print('Warning: no nominative object in {}'.format(object_))
                continue
            if not object_.__module__.startswith(tools_package.__package__):
                continue
            if isinstance(object_, type):
                if issubclass(object_, enum.Enum):
                    enumerations.append(object_)
                else:
                    classes.append(object_)
            elif isinstance(object_, types.FunctionType):
                functions.append(object_)
        classes.sort(key=lambda x: x.__name__)
        classes = tuple(classes)
        functions.sort(key=lambda x: x.__name__)
        functions = tuple(functions)
        return classes, enumerations, functions

    @staticmethod
    def get_class_rst(object_):
        import abjad
        import supriya
        document = abjad.documentationtools.ReSTDocument()
        tools_package_python_path = '.'.join(object_.__module__.split('.')[:-1])
        module_directive = supriya.documentationtools.ConcreteReSTDirective(
            directive='currentmodule',
            argument=tools_package_python_path,
            )
        document.append(module_directive)
        tools_package_qualified_name = '.'.join(
            object_.__module__.split('.')[-2:],
            )
        heading = abjad.documentationtools.ReSTHeading(
            level=2,
            text=tools_package_qualified_name,
            )
        document.append(heading)
        autodoc_directive = abjad.documentationtools.ReSTAutodocDirective(
            argument=object_.__module__,
            directive='autoclass',
            )
        document.append(autodoc_directive)
        return document

    @staticmethod
    def get_function_rst(object_):
        import abjad
        import supriya
        document = abjad.documentationtools.ReSTDocument()
        tools_package_python_path = '.'.join(object_.__module__.split('.')[:-1])
        module_directive = supriya.documentationtools.ConcreteReSTDirective(
            directive='currentmodule',
            argument=tools_package_python_path,
            )
        document.append(module_directive)
        tools_package_qualified_name = '.'.join(
            object_.__module__.split('.')[-2:],
            )
        heading = abjad.documentationtools.ReSTHeading(
            level=2,
            text=tools_package_qualified_name,
            )
        document.append(heading)
        autodoc_directive = abjad.documentationtools.ReSTAutodocDirective(
            argument=object_.__module__,
            directive='autofunction',
            )
        document.append(autodoc_directive)
        return document

    @staticmethod
    def get_tools_package_rst(tools_package):
        from abjad.tools import documentationtools
        manager = SupriyaDocumentationManager
        classes, enumerations, functions = manager.get_tools_package_contents(
            tools_package,
            )
        document = documentationtools.ReSTDocument()
        heading = documentationtools.ReSTHeading(
            level=2,
            text=tools_package.__name__.split('.')[-1],
            )
        document.append(heading)
        automodule_directive = documentationtools.ReSTAutodocDirective(
            argument=tools_package.__name__,
            directive='automodule',
            )
        document.append(automodule_directive)
        if classes:
            heading = documentationtools.ReSTHeading(
                level=3,
                text='Classes',
                )
            document.append(heading)
            toc = documentationtools.ReSTTOCDirective()
            for class_ in classes:
                toc_item = documentationtools.ReSTTOCItem(
                    text=class_.__name__,
                    )
                toc.append(toc_item)
            document.append(toc)
        if functions:
            heading = documentationtools.ReSTHeading(
                level=3,
                text='Functions',
                )
            document.append(heading)
            toc = documentationtools.ReSTTOCDirective()
            for function in functions:
                toc_item = documentationtools.ReSTTOCItem(
                    text=function.__name__,
                    )
                toc.append(toc_item)
            document.append(toc)
        if enumerations:
            heading = documentationtools.ReSTHeading(
                level=3,
                text='Enumerations',
                )
            document.append(heading)
            toc = documentationtools.ReSTTOCDirective()
            for enumeration in enumerations:
                toc_item = documentationtools.ReSTTOCItem(
                    text=enumeration.__name__,
                    )
                toc.append(toc_item)
            document.append(toc)
        return document

    @staticmethod
    def get_api_directory_path():
        import supriya
        path = supriya.__path__[0]
        path = os.path.join(
            path,
            'docs',
            'source',
            'tools',
            )
        return path

    @staticmethod
    def get_api_index_file_path():
        manager = SupriyaDocumentationManager
        path = os.path.join(
            manager.get_api_directory_path(),
            'index.rst',
            )
        return path

    @staticmethod
    def get_api_index_rst(tools_packages):
        from abjad.tools import documentationtools
        document = documentationtools.ReSTDocument()
        heading = documentationtools.ReSTHeading(
            level=2,
            text='Supriya API',
            )
        document.append(heading)
        toc = documentationtools.ReSTTOCDirective()
        for tools_package in tools_packages:
            tools_package_name = tools_package.__package__.split('.')[-1]
            toc_item = documentationtools.ReSTTOCItem(
                text='{}/index'.format(tools_package_name),
                )
            toc.append(toc_item)
        document.append(toc)
        return document

    @staticmethod
    def module_path_to_file_path(module_path):
        manager = SupriyaDocumentationManager
        parts = module_path.split('.')
        parts = parts[2:]
        parts[-1] = parts[-1] + '.rst'
        parts.insert(0, manager.get_api_directory_path())
        path = os.path.join(*parts)
        return path

    @staticmethod
    def package_path_to_file_path(package_path):
        manager = SupriyaDocumentationManager
        parts = package_path.split('.')
        parts = parts[2:]
        parts.append('index.rst')
        parts.insert(0, manager.get_api_directory_path())
        path = os.path.join(*parts)
        return path

    @staticmethod
    def remove_api_directory():
        manager = SupriyaDocumentationManager
        path = manager.get_api_directory_path()
        if os.path.exists(path):
            shutil.rmtree(path)

    @staticmethod
    def ensure_directory(path):
        path = os.path.dirname(path)
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def write(file_path, string):
        should_write = True
        if os.path.exists(file_path):
            with open(file_path, 'r') as file_pointer:
                old_string = file_pointer.read()
            if old_string == string:
                should_write = False
        if should_write:
            with open(file_path, 'w') as file_pointer:
                file_pointer.write(string)

    @staticmethod
    def execute():
        print('Rebuilding Supriya documentation source.')
        manager = SupriyaDocumentationManager
        manager.remove_api_directory()
        tools_packages = manager.get_tools_packages()
        api_index_rst = manager.get_api_index_rst(tools_packages)
        api_index_file_path = manager.get_api_index_file_path()
        manager.ensure_directory(api_index_file_path)
        manager.write(
            api_index_file_path,
            api_index_rst.rest_format,
            )
        for package in tools_packages:
            tools_package_rst = manager.get_tools_package_rst(package)
            tools_package_file_path = manager.package_path_to_file_path(
                package.__package__)
            manager.ensure_directory(tools_package_file_path)
            manager.write(
                tools_package_file_path,
                tools_package_rst.rest_format,
                )
            classes, enumerations, functions = \
                manager.get_tools_package_contents(package)
            for class_ in classes:
                file_path = manager.module_path_to_file_path(
                    class_.__module__,
                    )
                rst = manager.get_class_rst(class_)
                manager.write(file_path, rst.rest_format)
            for enumeration in enumerations:
                file_path = manager.module_path_to_file_path(
                    enumeration.__module__,
                    )
                rst = manager.get_class_rst(enumeration)
                manager.write(file_path, rst.rest_format)
            for function in functions:
                file_path = manager.module_path_to_file_path(
                    function.__module__,
                    )
                rst = manager.get_function_rst(function)
                manager.write(file_path, rst.rest_format)