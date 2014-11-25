# -*- encoding: utf-8 -*-
from __future__ import print_function
import enum
import inspect
import importlib
import os
import re
import shutil
import types


class SupriyaDocumentationManager(object):

    @staticmethod
    def build_attribute_section(
        cls,
        attrs,
        directive,
        title,
        ):
        from abjad.tools import documentationtools
        result = []
        if attrs:
            result.append(documentationtools.ReSTHeading(
                level=3,
                text=title,
                ))
            for attr in attrs:
                options = {
                    'noindex': True,
                    }
                autodoc = documentationtools.ReSTAutodocDirective(
                    argument='{}.{}'.format(cls.__name__, attr.name),
                    directive=directive,
                    options=options,
                    )
                if cls is attr.defining_class:
                    result.append(autodoc)
                else:
                    container = documentationtools.ReSTDirective(
                        argument='inherited',
                        directive='container',
                        )
                    container.append(autodoc)
                    html_only = documentationtools.ReSTDirective(
                        argument='html',
                        directive='only',
                        )
                    html_only.append(container)
                    result.append(html_only)
        return result

    @staticmethod
    def build_attributes_autosummary(
        cls,
        class_methods,
        data,
        inherited_attributes,
        methods,
        readonly_properties,
        readwrite_properties,
        special_methods,
        static_methods,
        ):
        from abjad.tools import documentationtools
        result = []
        attributes = []
        attributes.extend(readonly_properties)
        attributes.extend(readwrite_properties)
        attributes.extend(methods)
        attributes.extend(class_methods)
        attributes.extend(static_methods)
        attributes.sort(key=lambda x: x.name)
        attributes.extend(special_methods)
        if attributes:
            autosummary = documentationtools.ReSTAutosummaryDirective()
            for attribute in attributes:
                autosummary.append('~{}.{}.{}'.format(
                    cls.__module__,
                    cls.__name__,
                    attribute.name,
                    ))
            html_only = documentationtools.ReSTOnlyDirective(argument='html')
            html_only.append(documentationtools.ReSTHeading(
                level=3,
                text='Attribute summary',
                ))
            html_only.append(autosummary)
            result.append(html_only)
        return result

    @staticmethod
    def build_bases_section(cls):
        from abjad.tools import documentationtools
        result = []
        result.append(documentationtools.ReSTHeading(
            level=3,
            text='Bases',
            ))
        mro = inspect.getmro(cls)[1:]
        for cls in mro:
            parts = cls.__module__.split('.') + [cls.__name__]
            while 1 < len(parts) and parts[-1] == parts[-2]:
                parts.pop()
            packagesystem_path = '.'.join(parts)
            text = '- :py:class:`{}`'.format(packagesystem_path)
            paragraph = documentationtools.ReSTParagraph(
                text=text,
                wrap=False,
                )
            result.append(paragraph)
        return result

    @staticmethod
    def build_enumeration_section(cls):
        from abjad.tools import documentationtools
        result = []
        if not issubclass(cls, enum.Enum):
            return result
        items = sorted(cls, key=lambda x: x.name)
        if items:
            result.append(documentationtools.ReSTHeading(
                level=3,
                text='Enumeration Items',
                ))
            for item in items:
                name = item.name
                value = item.value
                line = '- `{}`: {}'.format(name, value)
                paragraph = documentationtools.ReSTParagraph(
                    text=line,
                    wrap=False,
                    )
                result.append(paragraph)
        return result

    @staticmethod
    def collect_class_attributes(cls):
        ignored_special_methods = (
            '__getattribute__',
            '__getnewargs__',
            '__getstate__',
            '__init__',
            '__reduce__',
            '__reduce_ex__',
            '__setstate__',
            '__sizeof__',
            '__subclasshook__',
            'fromkeys',
            'pipe_cloexec',
            )
        class_methods = []
        data = []
        inherited_attributes = []
        methods = []
        readonly_properties = []
        readwrite_properties = []
        special_methods = []
        static_methods = []
        attrs = inspect.classify_class_attrs(cls)
        for attr in attrs:
            if attr.defining_class is object:
                continue
            if attr.defining_class is not cls:
                inherited_attributes.append(attr)
            if attr.kind == 'method':
                if attr.name not in ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        methods.append(attr)
            elif attr.kind == 'class method':
                if attr.name not in ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        class_methods.append(attr)
            elif attr.kind == 'static method':
                if attr.name not in ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        static_methods.append(attr)
            elif attr.kind == 'property' and not attr.name.startswith('_'):
                if attr.object.fset is None:
                    readonly_properties.append(attr)
                else:
                    readwrite_properties.append(attr)
            elif attr.kind == 'data' and not attr.name.startswith('_') \
                and attr.name not in getattr(cls, '__slots__', ()):
                data.append(attr)
        class_methods = tuple(sorted(class_methods))
        data = tuple(sorted(data))
        inherited_attributes = tuple(sorted(inherited_attributes))
        methods = tuple(sorted(methods))
        readonly_properties = tuple(sorted(readonly_properties))
        readwrite_properties = tuple(sorted(readwrite_properties))
        special_methods = tuple(sorted(special_methods))
        static_methods = tuple(sorted(static_methods))
        result = (
            class_methods,
            data,
            inherited_attributes,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
            )
        return result

    @staticmethod
    def ensure_directory(path):
        path = os.path.dirname(path)
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def execute(source_directory):
        print('Rebuilding Supriya documentation source.')
        source_directory = os.path.abspath(source_directory)
        manager = SupriyaDocumentationManager
        rewritten_files = set()
        tools_packages = manager.get_tools_packages()
        api_index_rst = manager.get_api_index_rst(tools_packages)
        api_index_file_path = manager.get_api_index_file_path(source_directory)
        manager.ensure_directory(api_index_file_path)
        manager.write(
            api_index_file_path,
            api_index_rst.rest_format,
            rewritten_files,
            )
        for package in tools_packages:
            tools_package_rst = manager.get_tools_package_rst(package)
            tools_package_file_path = manager.package_path_to_file_path(
                package.__package__,
                source_directory,
                )
            manager.ensure_directory(tools_package_file_path)
            manager.write(
                tools_package_file_path,
                tools_package_rst.rest_format,
                rewritten_files,
                )
            classes, functions = \
                manager.get_tools_package_contents(package)
            for cls in classes:
                file_path = manager.module_path_to_file_path(
                    cls.__module__,
                    source_directory,
                    )
                rst = manager.get_class_rst(cls)
                manager.write(file_path, rst.rest_format, rewritten_files)
            for function in functions:
                file_path = manager.module_path_to_file_path(
                    function.__module__,
                    source_directory,
                    )
                rst = manager.get_function_rst(function)
                manager.write(file_path, rst.rest_format, rewritten_files)
        for root, directory_names, file_names in os.walk(
            manager.get_api_directory_path(source_directory),
            topdown=False,
            ):
            for file_name in file_names[:]:
                file_path = os.path.join(root, file_name)
                if file_path not in rewritten_files:
                    file_names.remove(file_name)
                    os.remove(file_path)
                    print('PRUNED: {}'.format(file_path))
            if not file_names and not directory_names:
                shutil.rmtree(root)
                print('PRUNED: {}'.format(root))

    @staticmethod
    def get_api_directory_path(source_directory):
        path = os.path.join(
            source_directory,
            'tools',
            )
        return path

    @staticmethod
    def get_api_index_file_path(source_directory):
        manager = SupriyaDocumentationManager
        path = os.path.join(
            manager.get_api_directory_path(source_directory),
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
        toc = documentationtools.ReSTTOCDirective(
            options={
                'maxdepth': 2,
                },
            )
        for tools_package in tools_packages:
            tools_package_name = tools_package.__package__.split('.')[-1]
            toc_item = documentationtools.ReSTTOCItem(
                text='{}/index'.format(tools_package_name),
                )
            toc.append(toc_item)
        document.append(toc)
        return document

    @staticmethod
    def get_class_rst(cls):
        import abjad
        manager = SupriyaDocumentationManager
        module_name, _, class_name = cls.__module__.rpartition('.')
        tools_package_python_path = '.'.join(cls.__module__.split('.')[:-1])

        (
            class_methods,
            data,
            inherited_attributes,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
            ) = manager.collect_class_attributes(cls)

        document = abjad.documentationtools.ReSTDocument()

        module_directive = abjad.documentationtools.ReSTDirective(
            directive='currentmodule',
            argument=tools_package_python_path,
            )
        document.append(module_directive)

        heading = abjad.documentationtools.ReSTHeading(
            level=2,
            text=class_name,
            )
        document.append(heading)

        autoclass_directive = abjad.documentationtools.ReSTAutodocDirective(
            argument=cls.__name__,
            directive='autoclass',
            )
        document.append(autoclass_directive)

        lineage_heading = abjad.documentationtools.ReSTHeading(
            level=3,
            text='Lineage',
            )
        document.append(lineage_heading)
        lineage_graph = SupriyaDocumentationManager.get_lineage_graph(cls)
        lineage_graph.attributes['background'] = 'transparent'
        lineage_graph.attributes['rankdir'] = 'LR'
        graphviz_directive = abjad.documentationtools.GraphvizDirective(
            graph=lineage_graph,
            )
        graphviz_container = abjad.documentationtools.ReSTDirective(
            directive='container',
            argument='graphviz',
            )
        graphviz_container.append(graphviz_directive)
        document.append(graphviz_container)

        document.extend(manager.build_bases_section(cls))

        document.extend(manager.build_enumeration_section(cls))
        document.extend(manager.build_attributes_autosummary(
            cls,
            class_methods,
            data,
            inherited_attributes,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
            ))

        document.extend(manager.build_attribute_section(
            cls,
            readonly_properties,
            'autoattribute',
            'Read-only properties',
            ))

        document.extend(manager.build_attribute_section(
            cls,
            readwrite_properties,
            'autoattribute',
            'Read/write properties',
            ))

        document.extend(manager.build_attribute_section(
            cls,
            methods,
            'automethod',
            'Methods',
            ))

        document.extend(manager.build_attribute_section(
            cls,
            class_methods,
            'automethod',
            'Class methods',
            ))

        document.extend(manager.build_attribute_section(
            cls,
            static_methods,
            'automethod',
            'Static methods',
            ))

        document.extend(manager.build_attribute_section(
            cls,
            special_methods,
            'automethod',
            'Special methods',
            ))

        return document

    @staticmethod
    def get_class_summary(cls):
        doc = cls.__doc__
        if doc is None:
            doc = ''
        doc = doc.splitlines()
        m = re.search(r"^([A-Z].*?\.)(?:\s|$)", " ".join(doc).strip())
        if m:
            summary = m.group(1).strip()
        elif doc:
            summary = doc[0].strip()
        else:
            summary = ''
        return summary

    @staticmethod
    def get_function_rst(function):
        import abjad
        document = abjad.documentationtools.ReSTDocument()
        tools_package_python_path = '.'.join(function.__module__.split('.')[:-1])
        module_directive = abjad.documentationtools.ReSTDirective(
            directive='currentmodule',
            argument=tools_package_python_path,
            )
        document.append(module_directive)
        tools_package_qualified_name = '.'.join(
            function.__module__.split('.')[-2:],
            )
        heading = abjad.documentationtools.ReSTHeading(
            level=2,
            text=tools_package_qualified_name,
            )
        document.append(heading)
        autodoc_directive = abjad.documentationtools.ReSTAutodocDirective(
            argument=function.__name__,
            directive='autofunction',
            )
        document.append(autodoc_directive)
        return document

    @staticmethod
    def get_lineage_graph(cls):
        def get_node_name(original_name):
            parts = original_name.split('.')
            name = [parts[0]]
            for part in parts[1:]:
                if part != name[-1]:
                    name.append(part)
            if name[0] in ('abjad', 'experimental', 'supriya'):
                return str('.'.join(name[2:]))
            return str('.'.join(name))
        from abjad.tools import documentationtools
        addresses = ('abjad', 'supriya')
        module_name, _, class_name = cls.__module__.rpartition('.')
        importlib.import_module(module_name)
        lineage = documentationtools.InheritanceGraph(
            addresses=addresses,
            lineage_addresses=((module_name, class_name),)
            )
        graph = lineage.__graph__()
        maximum_node_count = 30
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=addresses,
                lineage_addresses=((module_name, class_name),),
                lineage_prune_distance=2,
                )
            graph = lineage.__graph__()
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=addresses,
                lineage_addresses=((module_name, class_name),),
                lineage_prune_distance=1,
                )
            graph = lineage.__graph__()
        node_name = get_node_name(module_name + '.' + class_name)
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=((module_name, class_name),),
                )
            graph = lineage.__graph__()
            graph_node = graph[node_name]
            graph_node.attributes['color'] = 'black'
            graph_node.attributes['fontcolor'] = 'white'
            graph_node.attributes['style'] = ('filled', 'rounded')
        graph_node = graph[node_name]
        graph_node.attributes['label'] = \
            '<<B>{}</B>>'.format(graph_node.attributes['label'])
        return graph

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
        functions = []
        for name in dir(tools_package):
            if name.startswith('_'):
                continue
            obj = getattr(tools_package, name)
            if not hasattr(obj, '__module__'):
                print('Warning: no nominative object in {}'.format(obj))
                continue
            if not obj.__module__.startswith(tools_package.__package__):
                continue
            if isinstance(obj, type):
                classes.append(obj)
            elif isinstance(obj, types.FunctionType):
                functions.append(obj)
        classes.sort(key=lambda x: x.__name__)
        classes = tuple(classes)
        functions.sort(key=lambda x: x.__name__)
        functions = tuple(functions)
        return classes, functions

    @staticmethod
    def get_tools_package_rst(tools_package):
        from abjad.tools import documentationtools
        manager = SupriyaDocumentationManager
        classes, functions = manager.get_tools_package_contents(
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
            sections = {}
            for cls in classes:
                documentation_section = getattr(
                    cls,
                    '__documentation_section__',
                    None,
                    )
                if documentation_section is None:
                    if issubclass(cls, enum.Enum):
                        documentation_section = 'Enumerations'
                    elif issubclass(cls, Exception):
                        documentation_section = 'Errors'
                    else:
                        documentation_section = 'Classes'
                    if inspect.isabstract(cls):
                        documentation_section = 'Abstract Classes'
                if documentation_section not in sections:
                    sections[documentation_section] = []
                sections[documentation_section].append(cls)
            section_names = sorted(sections)
            if 'Main Classes' in sections:
                section_names.remove('Main Classes')
                section_names.insert(0, 'Main Classes')
            if 'Errors' in sections:
                section_names.remove('Errors')
                section_names.append('Errors')
            for section_name in section_names:
                rule = documentationtools.ReSTHorizontalRule()
                document.append(rule)
                heading = documentationtools.ReSTHeading(
                    level=3,
                    text=section_name,
                    )
                document.append(heading)
                toc = documentationtools.ReSTTOCDirective(
                    options={
                        'hidden': True,
                        },
                    )
                for cls in sections[section_name]:
                    class_name = cls.__name__
                    if class_name == 'Index':
                        class_name = '_Index'
                    toc_item = documentationtools.ReSTTOCItem(
                        text=class_name,
                        )
                    toc.append(toc_item)
                document.append(toc)
                autosummary = documentationtools.ReSTAutosummaryDirective(
                    options={
                        'nosignatures': True,
                        },
                    )
                for cls in sections[section_name]:
                    item = documentationtools.ReSTAutosummaryItem(
                        text=cls.__name__,
                        )
                    autosummary.append(item)
                document.append(autosummary)
        if functions:
            heading = documentationtools.ReSTHeading(
                level=3,
                text='Functions',
                )
            document.append(heading)
            toc = documentationtools.ReSTTOCDirective(
                options={
                    'hidden': True,
                    },
                )
            for function in functions:
                toc_item = documentationtools.ReSTTOCItem(
                    text=function.__name__,
                    )
                toc.append(toc_item)
            document.append(toc)
            autosummary = documentationtools.ReSTAutosummaryDirective(
                options={
                    'nosignatures': True,
                    },
                )
            for function in functions:
                item = documentationtools.ReSTAutosummaryItem(
                    text=function.__name__,
                    )
                autosummary.append(item)
            document.append(autosummary)
        return document

    @staticmethod
    def module_path_to_file_path(module_path, source_directory):
        manager = SupriyaDocumentationManager
        parts = module_path.split('.')
        parts = parts[2:]
        if parts[-1] == 'Index':
            parts[-1] = '_' + parts[-1] + '.rst'
        else:
            parts[-1] = parts[-1] + '.rst'
        parts.insert(0, manager.get_api_directory_path(source_directory))
        path = os.path.join(*parts)
        return path

    @staticmethod
    def package_path_to_file_path(package_path, source_directory):
        manager = SupriyaDocumentationManager
        parts = package_path.split('.')
        parts = parts[2:]
        parts.append('index.rst')
        parts.insert(0, manager.get_api_directory_path(source_directory))
        path = os.path.join(*parts)
        return path

    @staticmethod
    def remove_api_directory():
        manager = SupriyaDocumentationManager
        path = manager.get_api_directory_path()
        if os.path.exists(path):
            shutil.rmtree(path)

    @staticmethod
    def write(file_path, string, rewritten_files):
        should_write = True
        if os.path.exists(file_path):
            with open(file_path, 'r') as file_pointer:
                old_string = file_pointer.read()
            if old_string == string:
                should_write = False
        if should_write:
            if os.path.exists(file_path):
                print('REWROTE: {}'.format(file_path))
            else:
                print('WROTE: {}'.format(file_path))
            with open(file_path, 'w') as file_pointer:
                file_pointer.write(string)
        else:
            print('PRESERVED: {}'.format(file_path))
        rewritten_files.add(file_path)