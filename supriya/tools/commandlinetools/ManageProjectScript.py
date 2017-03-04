# -*- encoding: utf-8 -*-
import os
import pathlib
import sys
import yaml
from abjad.tools import stringtools
from supriya.tools.commandlinetools.ProjectPackageScript import ProjectPackageScript


class ManageProjectScript(ProjectPackageScript):
    '''
    Manages project packages.

    ..  shell::

        spv project --help

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    alias = 'project'
    short_description = 'manage project packages'

    ### PRIVATE METHODS ###

    def _handle_new(
        self,
        title,
        composer_email=None,
        composer_github=None,
        composer_library=None,
        composer_name=None,
        composer_website=None,
        force=False,
        ):
        print('Creating project package {!r}...'.format(title))
        package_name = stringtools.to_accent_free_snake_case(title)
        outer_target_path = pathlib.Path(package_name).absolute()
        if outer_target_path.exists() and not force:
            message = '    Directory {!s} already exists.'
            message = message.format(package_name)
            print(message)
            sys.exit(1)
        inner_target_path = outer_target_path.joinpath(package_name)
        boilerplate_path = self._get_boilerplate_path()
        outer_source_path = boilerplate_path.joinpath('example_project')
        inner_source_path = outer_source_path.joinpath('example_project')
        metadata = {
            'project_package_name': package_name,
            'composer_email': composer_email,
            'composer_full_name': composer_name,
            'composer_github_username': composer_github,
            'composer_library_package_name': composer_library,
            'title': title,
            }
        for path in self._copy_tree(
            outer_source_path,
            outer_target_path,
            recurse=False,
            ):
            if path.is_file() and path.suffix == '.jinja':
                self._template_file(path, **metadata)
                path.rename(path.with_suffix(''))
        for path in self._copy_tree(
            inner_source_path,
            inner_target_path,
            recurse=True,
            ):
            if path.is_file() and path.suffix == '.jinja':
                self._template_file(path, **metadata)
                path.rename(path.with_suffix(''))
        self._setup_paths(inner_target_path)
        self._write_json(
            dict(
                composer_email=composer_email,
                composer_github=composer_github,
                composer_library=composer_library,
                composer_name=composer_name,
                composer_website=composer_website,
                title=title,
                ),
            inner_target_path.joinpath('metadata.json'),
            )
        self._make_project_settings_yaml(
            inner_target_path,
            composer_email=composer_email,
            composer_github=composer_github,
            composer_library=composer_library,
            composer_name=composer_name,
            composer_website=composer_website,
            title=title,
            )
        print('    Created {path!s}{sep}'.format(
            path=package_name,
            sep=os.path.sep))

    @classmethod
    def _make_project_settings_yaml(
        cls,
        inner_project_path,
        composer_email=None,
        composer_github=None,
        composer_library=None,
        composer_name=None,
        composer_website=None,
        title=None,
        ):
        from supriya.tools import servertools
        server_options = servertools.ServerOptions()
        server_options = server_options.as_dict()
        project_settings = dict(
            server_options=server_options,
            composer=dict(
                email=composer_email,
                github=composer_github,
                library=composer_library,
                name=composer_name,
                website=composer_website,
                ),
            title=title,
            )
        project_settings_yaml = yaml.dump(
            project_settings,
            default_flow_style=False,
            indent=4,
            )
        project_settings_path = inner_project_path.joinpath(
            'project-settings.yml',
            )
        with open(str(project_settings_path), 'w') as file_pointer:
            file_pointer.write(project_settings_yaml)

    def _process_args(self, args):
        if args.new:
            self._handle_new(
                composer_email=args.composer_email,
                composer_github=args.composer_github,
                composer_library=args.composer_library,
                composer_name=args.composer_name,
                composer_website=args.composer_website,
                force=args.force,
                title=args.new,
                )
            return
        self._setup_paths(args.project_path)
        if args.clean:
            self._handle_clean(args.project_path)

    def _setup_argument_parser(self, parser):
        action_group = parser.add_argument_group('actions')
        action_group = action_group.add_mutually_exclusive_group(required=True)
        action_group.add_argument(
            '--new', '-N',
            help='create a new project',
            metavar='TITLE',
            )
        action_group.add_argument(
            '--clean', '-C',
            action='store_true',
            help='clean out stale render artifacts',
            )
        new_group = parser.add_argument_group('--new options')
        new_group.add_argument(
            '--composer-name', '-n',
            default='A Composer',
            metavar='NAME',
            )
        new_group.add_argument(
            '--composer-email', '-e',
            default='composer@email.com',
            metavar='EMAIL',
            )
        new_group.add_argument(
            '--composer-github', '-g',
            default='composer',
            metavar='GITHUB_USERNAME',
            )
        new_group.add_argument(
            '--composer-library', '-l',
            default='library',
            metavar='LIBRARY_NAME',
            )
        new_group.add_argument(
            '--composer-website', '-w',
            default='www.composer.com',
            metavar='WEBSITE',
            )
        common_group = parser.add_argument_group('common options')
        common_group.add_argument(
            '--force', '-f',
            action='store_true',
            help='force overwriting',
            )
        common_group.add_argument(
            '--project-path', '-p',
            metavar='project',
            help='project path or package name',
            default=os.path.curdir,
            )
