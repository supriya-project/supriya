# -*- encoding: utf-8 -*-
import importlib
import jinja2
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import traceback
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.commandlinetools.CommandlineScript import CommandlineScript


class ProjectPackageScript(CommandlineScript):

    ### CLASS VARIABLES ###

    _name_re = re.compile('^[a-z][a-z0-9_]*$')

    _project_subdirectory_names = (
        'assets',
        'composites',
        'distribution',
        'materials',
        'renders',
        'synthdefs',
        'tools',
        )

    ### PRIVATE METHODS ###

    def _call_subprocess(self, command):
        '''Trivial wrapper for mocking purposes.'''
        return subprocess.call(command, shell=True)

    def _collect_globbable_names(self, input_names):
        validated_names = []
        for input_name in input_names:
            if not self._name_is_valid_globbable(input_name):
                print('Cannot glob {!r}'.format(input_name))
                sys.exit(1)
            validated_names.append(input_name)
        return validated_names

    def _collect_matching_paths(self, names, section):
        matching_paths = []
        section_path = self.inner_project_path.joinpath(section)
        valid_paths = self._list_subpackages(section)
        for name in names:
            if name.startswith('+'):
                name = '*{}*'.format('*'.join(name[1:]))
            for path in sorted(section_path.glob(name)):
                if path not in matching_paths and path in valid_paths:
                    matching_paths.append(path)
        return matching_paths

    def _copy_package(self, source_name, target_name, section, force=False):
        singular = section
        if singular.endswith('s'):
            singular = singular[:-1]
        print('Copying {singular} subpackage {source_name!r} to {target_name!r} ...'.format(
            singular=singular, source_name=source_name, target_name=target_name))
        source_path = self._name_to_project_subdirectory_path(
            source_name, section, self.inner_project_path)
        target_path = self._name_to_project_subdirectory_path(
            target_name, section, self.inner_project_path)
        if not source_path.exists():
            print('    Subpackage {path!s}{sep} does not exist!'.format(
                path=source_path.relative_to(self.outer_project_path),
                sep=os.path.sep))
            sys.exit(1)
        if target_path.exists():
            if force:
                print('    Overwriting {path!s}{sep} ...'.format(
                    path=target_path.relative_to(self.outer_project_path),
                    sep=os.path.sep))
                self._remove_tree(target_path)
            else:
                print('    Subpackage {path!s}{sep} exists!'.format(
                    path=target_path.relative_to(self.outer_project_path),
                    sep=os.path.sep))
                sys.exit(1)
        self._copy_tree(source_path, target_path)
        self._replace_in_files(target_path, source_name, target_name)
        print('    Copied {source_path!s}{sep} to {target_path!s}{sep}'.format(
            source_path=source_path.relative_to(self.outer_project_path),
            target_path=target_path.relative_to(self.outer_project_path),
            sep=os.path.sep))

    @classmethod
    def _copy_tree(cls, source_directory, target_directory, recurse=True):
        copied_paths = []
        source_paths = [_ for _ in source_directory.glob('*')]
        if not target_directory.exists():
            target_directory.mkdir(parents=True)
        for source_path in source_paths:
            if source_path.name == '__pycache__':
                continue
            elif source_path.suffix == '.pyc':
                continue
            source_name = source_path.relative_to(source_directory)
            target_path = target_directory.joinpath(source_name)
            if source_path.is_dir() and recurse:
                copied_paths.extend(
                    cls._copy_tree(source_path, target_path, recurse=True)
                    )
            elif source_path.is_file():
                shutil.copyfile(str(source_path), str(target_path))
            copied_paths.append(target_path)
        return copied_paths

    def _create_package_from_template(
        self,
        package_name,
        section,
        force=False,
        ):
        singular = section
        if singular.endswith('s'):
            singular = singular[:-1]
        print('Creating {singular} subpackage {package_name!r} ...'.format(
            singular=singular, package_name=package_name))
        source_name = 'example_{}'.format(singular)
        source_path = self._get_boilerplate_path().joinpath(source_name)
        if not source_path.exists():
            print('    Missing source!')
            sys.exit(1)
        target_path = self._name_to_project_subdirectory_path(
            package_name, section, self.inner_project_path)
        if target_path.exists() and not force:
            print('    Path exists: {}'.format(
                target_path.relative_to(self.inner_project_path.parent)))
            sys.exit(1)
        metadata = self._read_project_metadata_json(
            self.inner_project_path)
        metadata['project_package_name'] = self.inner_project_path.name
        metadata['package_name'] = target_path.name
        for path in self._copy_tree(source_path, target_path):
            if path.is_file() and path.suffix == '.jinja':
                self._template_file(path, **metadata)
                path.rename(path.with_suffix(''))
        print('    Created {path!s}{sep}'.format(
            path=target_path.relative_to(self.outer_project_path),
            sep=os.path.sep))

    def _edit_packages(self, names, section):
        from abjad import abjad_configuration
        globbable_names = self._collect_globbable_names(names)
        print('Edit candidates: {!r} ...'.format(
            ' '.join(globbable_names)))
        matching_paths = self._collect_matching_paths(
            globbable_names, section)
        if not matching_paths:
            print('    No matching {}.'.format(section))
            self._handle_list()
        command = [abjad_configuration.get_text_editor()]
        for path in matching_paths:
            command.append(str(path.joinpath('definition.py')))
        command = ' '.join(command)
        exit_code = self._call_subprocess(command)
        if exit_code:
            sys.exit(exit_code)

    @classmethod
    def _get_boilerplate_path(cls):
        import supriya
        return pathlib.Path(supriya.__path__[0]).joinpath('boilerplate')

    def _import_path(self, path, project_root_path, verbose=True):
        if verbose:
            print('    Importing {!s}'.format(path))
        with systemtools.TemporaryDirectoryChange(str(project_root_path)):
            try:
                importlib.invalidate_caches()
            except:
                pass
            if path in sys.modules:
                importlib.reload(sys.modules[path])
            try:
                return importlib.import_module(path)
            except ImportError:
                print(traceback.format_exc())
                raise SystemExit(1)
            except Exception:
                print(traceback.format_exc())
                raise SystemExit(1)

    def _list_subpackages(self, section, project_path=None):
        if project_path is None:
            project_path = os.curdir
            project_path = self._path_to_project_package_path(project_path)
        else:
            project_path = self._project_project_path
        section_path = project_path.joinpath(section)
        paths = [
            path for path in section_path.glob('*')
            if path.is_dir() and path.joinpath('__init__.py').exists()
            ]
        return sorted(paths)

    def _list_package_nominatives(self, section):
        pass

    @classmethod
    def _name_is_valid_globbable(cls, name):
        if '..' in name:
            return False
        elif '**' in name:
            return False
        elif '/' in name:
            return False
        return True

    def _name_to_project_subdirectory_path(self, name, section, project_path):
        project_path = self._path_to_project_package_path(project_path)
        name = stringtools.to_accent_free_snake_case(name)
        path = project_path.joinpath(section, name)
        return path

    def _path_to_packagesystem_path(self, path):
        project_package_path = self._path_to_project_package_path(path)
        relative_path = path.relative_to(project_package_path)
        parts = [project_package_path.name]
        parts.extend(relative_path.parts)
        return '.'.join(parts)

    def _path_to_project_package_path(self, path):
        if isinstance(path, str):
            # Is `path` an importable name? Use its module path.
            if self._name_re.match(path):
                try:
                    importlib.invalidate_caches()
                    module = importlib.import_module(path)
                    path = getattr(module, '__file__',  # A module.
                        getattr(module, '__path__'))  # A package.
                    if hasattr(path, '_path'):  # A local import.
                        path = path._path
                    if not isinstance(path, str):  # If it's a package...
                        path = path[0]  # Get the first path in the list.
                except:
                    print(traceback.format_exc())
            # Make sure to expand any home variables.
            path = pathlib.Path(os.path.expanduser(path))
        path = path.absolute()
        if not path.exists():
            print("Couldn locate or import project matching {!r}.".format(path))
            sys.exit(1)
        # Convert to directory.
        if path.is_file():
            path = path.parent
        # Check for parent package if not actually inside a package.
        # E.g.:
        #   - project_root
        #   - project_root/project/build/build_target
        #   - project_root/project/etc
        if not path.joinpath('__init__.py').exists():
            if path.joinpath(path.name, '__init__.py').exists():
                pass
            elif path.parent.joinpath('__init__.py').exists():
                path = path.parent
            elif path.parent.parent.joinpath('__init__.py').exists():
                path = path.parent.parent
        # Drill down as long as we're inside a Python package.
        while path.joinpath('__init__.py').exists():
            path = path.parent
        path = path.joinpath(path.name)
        # Make sure the directory even exists.
        if not path.exists():
            print('No project matching {!r} exists.'.format(path))
            sys.exit(1)
        # Check for mandatory files and subdirectories.
        necessary_paths = {}
        for name in ('__init__.py',) + self._project_subdirectory_names:
            necessary_path = path.joinpath(name)
            necessary_paths[necessary_path] = necessary_path.exists()
        if not all(necessary_paths.values()):
            print('Project directory {!s} is malformed.'.format(path))
            for necessary_path, exists in sorted(necessary_paths.items()):
                if exists:
                    continue
                print('    Missing: {!s}'.format(necessary_path))
            sys.exit(1)
        return path

    def _read_json(self, path, strict=False, verbose=True):
        if verbose:
            message = '    Reading {!s} ... '
            path_to_print = path.relative_to(self.inner_project_path.parent)
            print(message.format(path_to_print), end='')
        if not path.exists():
            if verbose:
                print('JSON does not exist.')
            if strict:
                sys.exit(1)
            return {}
        try:
            with open(str(path), 'r') as file_pointer:
                expr = json.loads(file_pointer.read())
        except:
            if verbose:
                print('JSON is corrupted.')
            if strict:
                sys.exit(1)
            return {}
        if verbose:
            print('OK!')
        return expr

    def _read_project_metadata_json(self, project_path=None, verbose=True):
        if project_path:
            project_path = self._path_to_project_package_path(project_path)
        else:
            project_path = self.inner_project_path
        metadata_path = project_path.joinpath('metadata.json')
        metadata = self._read_json(metadata_path, verbose=verbose)
        assert isinstance(metadata, dict)
        return metadata

    def _remove_tree(self, target_path):
        if target_path.is_dir():
            shutil.rmtree(str(target_path))
        elif target_path.is_file():
            target_path.unlink()

    def _remove_package(self, target_name, section):
        singular = section
        if singular.endswith('s'):
            singular = singular[:-1]
        target_path = self._name_to_project_subdirectory_path(
            target_name, section, self.inner_project_path)
        print('Deleting {singular} subpackage {package_name!r} ...'.format(
            singular=singular, package_name=target_name))
        if not target_path.exists():
            print('    Subpackage {path!s}{sep} does not exist!'.format(
                path=target_path.relative_to(self.outer_project_path),
                sep=os.path.sep))
            sys.exit(1)
        self._remove_tree(target_path)
        print('    Deleted {path!s}{sep}'.format(
            path=target_path.relative_to(self.outer_project_path),
            sep=os.path.sep))

    def _rename_package(self, source_name, target_name, section, force=False):
        singular = section
        if singular.endswith('s'):
            singular = singular[:-1]
        print('Renaming {singular} subpackage {source_name!r} to {target_name!r} ...'.format(
            singular=singular, source_name=source_name, target_name=target_name))
        source_path = self._name_to_project_subdirectory_path(
            source_name, section, self.inner_project_path)
        target_path = self._name_to_project_subdirectory_path(
            target_name, section, self.inner_project_path)
        if not source_path.exists():
            print('    Subpackage {path!s}{sep} does not exist!'.format(
                path=source_path.relative_to(self.outer_project_path),
                sep=os.path.sep))
            sys.exit(1)
        if target_path.exists():
            if force:
                print('    Overwriting {path!s}{sep} ...'.format(
                    path=target_path.relative_to(self.outer_project_path),
                    sep=os.path.sep))
                self._remove_tree(target_path)
            else:
                print('    Subpackage {path!s}{sep} exists!'.format(
                    path=target_path.relative_to(self.outer_project_path),
                    sep=os.path.sep))
                sys.exit(1)
        self._copy_tree(source_path, target_path)
        self._replace_in_files(target_path, source_name, target_name)
        self._remove_tree(source_path)
        print('    Renamed {source_path!s}{sep} to {target_path!s}{sep}'.format(
            source_path=source_path.relative_to(self.outer_project_path),
            target_path=target_path.relative_to(self.outer_project_path),
            sep=os.path.sep))

    def _replace_in_file(self, target_name, old_string, new_string):
        pass

    def _replace_in_files(self, target_directory, old_string, new_string):
        pass

    def _report_time(self, timer, prefix='Runtime'):
        message = '        {}: {} {}'
        total_time = int(timer.elapsed_time)
        identifier = stringtools.pluralize('second', total_time)
        message = message.format(prefix, total_time, identifier)
        print(message)

    def _setup_paths(self, project_path):
        project_package_path = self._path_to_project_package_path(
            project_path)
        self.inner_project_path = project_package_path
        self.outer_project_path = project_package_path.parent
        self._root_parent_path = self.outer_project_path.parent
        for name in self._project_subdirectory_names:
            path = self.inner_project_path.joinpath(name)
            setattr(self, '_{}_path'.format(name), path)

    @classmethod
    def _template_file(cls, file_path, **kwargs):
        file_path = str(file_path)
        with open(file_path, 'r') as file_pointer:
            source = file_pointer.read()
        template = jinja2.Template(source)
        result = template.render(**kwargs)
        with open(file_path, 'w') as file_pointer:
            file_pointer.write(result)

    def _write_json(self, expr, path, verbose=True):
        if verbose:
            message = '    Writing {!s}'
            path_to_print = path.relative_to(self.outer_project_path)
            print(message.format(path_to_print))
        contents = json.dumps(
            expr,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
            )
        should_write = True
        if path.exists():
            with open(str(path), 'r') as file_pointer:
                if file_pointer.read() == contents:
                    should_write = False
        if should_write:
            with open(str(path), 'w') as file_pointer:
                file_pointer.write(contents)
