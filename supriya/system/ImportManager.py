# -*- encoding: utf-8 -*-
import os
import types


class ImportManager(object):
    r'''Imports structured packages.
    '''

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_public_function_names_in_module(module_file):
        r'''Collects and returns all public functions defined in
        module_file.
        '''
        result = []
        module_file = module_file.replace(os.sep, '.')
        mod = __import__(module_file, fromlist=['*'])
        for key, value in list(vars(mod).items()):
            if not key.startswith('_'):
                # handle public function decorated with @require
                if getattr(value, 'func_closure', None):
                    module_name = getattr(value.func_closure[1].cell_contents,
                        '__module__', None)
                # handle plain old function
                else:
                    module_name = getattr(value, '__module__', None)
                if module_name == module_file:
                    result.append(value)
        return result

    @staticmethod
    def _import_contents_of_public_packages_in_path_into_namespace(
        path,
        namespace,
        ):
        r'''Inspects the top level of path.

        Finds public class packages and imports class package
        contents into namespace.

        Does not inspect lower levels of path.
        '''
        package_path = ImportManager._split_package_path(path)
        for name in os.listdir(path):
            fullname = os.path.join(path, name)
            if os.path.isdir(fullname):
                if name[0].isupper() and \
                    os.path.exists(os.path.join(fullname, '__init__.py')) and \
                    os.path.exists(os.path.join(fullname, '%s.py' % name)):
                    class_package = '.'.join([package_path, name])
                    class_module = '.'.join([class_package, name])
                    public_names = \
                        ImportManager._get_public_function_names_in_module(
                            class_module)
                    for public_name in public_names:
                        namespace[public_name.__name__] = public_name

    @staticmethod
    def _split_package_path(path):
        outer, inner = path, None
        while os.path.exists(os.path.join(outer, '__init__.py')):
            outer, inner = os.path.split(outer)
        package_path = os.path.relpath(path, outer)
        package_path = package_path.replace(os.sep, '.')
        return package_path

    ### PUBLIC METHODS ###

    @staticmethod
    def import_public_names_from_path_into_namespace(
        path,
        namespace,
        delete_systemtools=True,
        **kwargs
        ):
        r'''Inspects the top level of `path`.

        Finds .py modules in path and imports public functions from
        .py modules into namespace.

        Finds packages in path and imports package names into namespace.

        Does not import package content into namespace.

        Does not inspect lower levels of path.
        '''
        package_path = ImportManager._split_package_path(path)
        for element in os.listdir(path):
            if os.path.isfile(os.path.join(path, element)):
                if not element.startswith('_') and element.endswith('.py'):
                    # import function inside module
                    name = os.path.splitext(element)[0]
                    submod = os.path.join(package_path, name)
                    functions = \
                        ImportManager._get_public_function_names_in_module(
                            submod)
                    for f in functions:
                        # handle public function decorated with @require
                        if f.__name__ == 'wrapper':
                            name = f.func_closure[1].cell_contents.__name__
                        else:
                            name = f.__name__
                        namespace[name] = f
            elif os.path.isdir(os.path.join(path, element)):
                if not element in ('.svn', '.git', 'test', '__pycache__'):
                    initializer_file_path = os.path.join(
                        path,
                        element,
                        '__init__.py',
                        )
                    if os.path.exists(initializer_file_path):
                        submod = '.'.join((package_path, element))
                        namespace[element] = __import__(submod, fromlist=['*'])
            else:
                message = 'neither a directory or file: {!r}'
                message = message.format(element)
                raise ImportError(message)
        ImportManager._import_contents_of_public_packages_in_path_into_namespace(
            path, namespace)
        if delete_systemtools:
            if 'systemtools' in namespace:
                del(namespace['systemtools'])
        if ImportManager.__name__ in namespace:
            del(namespace[ImportManager.__name__])

    @staticmethod
    def import_structured_package(
        path,
        namespace,
        delete_systemtools=True,
        **kwargs
        ):
        r'''Imports public names from `path` into `namespace`.

        This is the custom function that all Abjad packages use to import
        public classes and functions on startup.

        The function will work for any package laid out like Abjad packages.
        '''
        ImportManager.import_public_names_from_path_into_namespace(
            path,
            namespace,
            delete_systemtools=delete_systemtools,
            )
        if delete_systemtools:
            if 'systemtools' in namespace:
                del(namespace['systemtools'])
        if ImportManager.__name__ in namespace:
            del(namespace[ImportManager.__name__])