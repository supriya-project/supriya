# -*- encoding: utf-8 -*-
from __future__ import print_function
import enum
import inspect
import importlib
import os
import shutil
import types


class SupriyaDocumentationManager(object):

    @staticmethod
    def build_attribute_section(
        class_,
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
                autodoc = documentationtools.ReSTAutodocDirective(
                    argument='{}.{}'.format(
                        class_.__module__,
                        attr.name,
                        ),
                    directive=directive,
                    options={
                        'noindex': True,
                        },
                    )
                result.append(autodoc)
        return result

    @staticmethod
    def build_enumeration_section(class_):
        from abjad.tools import documentationtools
        result = []
        if not issubclass(class_, enum.Enum):
            return result
        result.append(documentationtools.ReSTHeading(
            level=3,
            text='Enumeration Items',
            ))
        return result

    @staticmethod
    def collect_class_attributes(class_):
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
        attrs = inspect.classify_class_attrs(class_)
        for attr in attrs:
            if attr.defining_class is object:
                continue
            if attr.defining_class is not class_:
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
                and attr.name not in getattr(class_, '__slots__', ()):
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
    def get_lineage_graph(class_):
        def get_node_name(original_name):
            parts = original_name.split('.')
            name = [parts[0]]
            for part in parts[1:]:
                if part != name[-1]:
                    name.append(part)
            if name[0] in ('abjad', 'experimental'):
                return str('.'.join(name[2:]))
            return str('.'.join(name))
        from abjad.tools import documentationtools
        addresses = ('abjad', 'supriya')
        module_name, _, class_name = class_.__module__.rpartition('.')
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
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=((module_name, class_name),),
                )
            node_name = get_node_name(module_name + '.' + class_name)
            graph = lineage.__graph__()
            graph_node = graph[node_name]
            graph_node.attributes['color'] = 'black'
            graph_node.attributes['fontcolor'] = 'white'
            graph_node.attributes['style'] = ('filled', 'rounded')
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
    def get_class_rst(class_):
        import abjad
        import supriya
        manager = SupriyaDocumentationManager
        module_name, _, class_name = class_.__module__.rpartition('.')
        tools_package_python_path = '.'.join(class_.__module__.split('.')[:-1])
        document = abjad.documentationtools.ReSTDocument()
        module_directive = supriya.documentationtools.ConcreteReSTDirective(
            directive='currentmodule',
            argument=tools_package_python_path,
            )
        document.append(module_directive)
        heading = abjad.documentationtools.ReSTHeading(
            level=2,
            text=class_name,
            )
        document.append(heading)
        # lineage_graph = manager.get_lineage_graph(class_)
        # graphviz_directive = supriya.documentationtools.GraphvizDirective(
        #     graph=lineage_graph,
        #     )
        # document.append(graphviz_directive)
        autoclass_directive = abjad.documentationtools.ReSTAutodocDirective(
            argument=class_.__module__,
            directive='autoclass',
            )
        document.append(autoclass_directive)
        (
            class_methods,
            data,
            inherited_attributes,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
            ) = manager.collect_class_attributes(class_)
        document.extend(manager.build_attribute_section(
            class_,
            readonly_properties,
            'autoattribute',
            'Read-only properties',
            ))
        document.extend(manager.build_attribute_section(
            class_,
            readwrite_properties,
            'autoattribute',
            'Read/write properties',
            ))
        document.extend(manager.build_attribute_section(
            class_,
            methods,
            'automethod',
            'Methods',
            ))
        document.extend(manager.build_attribute_section(
            class_,
            class_methods,
            'automethod',
            'Class methods',
            ))
        document.extend(manager.build_attribute_section(
            class_,
            static_methods,
            'automethod',
            'Static methods',
            ))
        document.extend(manager.build_attribute_section(
            class_,
            special_methods,
            'automethod',
            'Special methods',
            ))
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
            toc = documentationtools.ReSTTOCDirective(
                options={
                    'maxdepth': 1,
                    },
                )
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
            toc = documentationtools.ReSTTOCDirective(
                options={
                    'maxdepth': 1,
                    },
                )
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
            toc = documentationtools.ReSTTOCDirective(
                options={
                    'maxdepth': 1,
                    },
                )
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
        toc = documentationtools.ReSTTOCDirective(
            options={
                'maxdepth': 1,
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