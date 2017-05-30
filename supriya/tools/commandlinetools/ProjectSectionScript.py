# -*- encoding: utf-8 -*-
import abc
import collections
import os
import inspect
import sys
import traceback
from abjad.tools import systemtools
from supriya.tools.commandlinetools.ProjectPackageScript import (
    ProjectPackageScript
)
from supriya.tools.nonrealtimetools import (
    NonrealtimeRenderError,
    NonrealtimeOutputMissing,
)


class ProjectSectionScript(ProjectPackageScript):

    ### PRIVATE METHODS ###

    def _build_nrt_server_options(self, session):
        from supriya.tools import commandlinetools
        project_settings = commandlinetools.ProjectSettings(
            yaml_path=self.inner_project_path.joinpath(
                'project-settings.yml'),
            )
        server_options = project_settings.get('server_options', {})
        server_options.update(
            input_bus_channel_count=session.input_bus_channel_count,
            output_bus_channel_count=session.output_bus_channel_count,
            )
        for key, value in tuple(server_options.items()):
            if value is None:
                server_options.pop(key)
        return server_options

    def _handle_copy(
        self,
        source_name,
        target_name,
        force=False,
        ):
        self._copy_package(
            source_name,
            target_name,
            self._section_plural,
            force=force,
            )

    def _handle_delete(self, name):
        self._remove_package(name, self._section_plural)

    def _handle_edit(self, names):
        self._edit_packages(names, self._section_plural)

    def _handle_list(self):
        from abjad.tools.abctools import (
            AbjadObject, AbjadValueObject,
        )
        from supriya.tools.systemtools import (
            SupriyaObject, SupriyaValueObject,
        )
        basic_bases = (
            AbjadObject,
            AbjadValueObject,
            SupriyaObject,
            SupriyaValueObject,
            object,
            )
        print('Available {}:'.format(self._section_plural))
        all_objects = self._import_objects(
            self._section_plural,
            verbose=False,
            )
        if not all_objects:
            print('    No {} available.'.format(self._section_plural))
            sys.exit(1)
        categorized_objects = {}
        for name, object_ in all_objects.items():
            class_ = type(object_)
            base = class_.__bases__[0]
            attrs = {attr.name: attr for attr in
                inspect.classify_class_attrs(class_)}
            if any(_ in class_.__bases__ for _ in basic_bases):
                base = class_
            elif getattr(class_, '__is_terminal_ajv_list_item__', False) and \
                attrs['__is_terminal_ajv_list_item__'].defining_class is class_:
                base = class_
            categorized_objects.setdefault(base, []).append((name, class_))
        categorized_objects = sorted(
            categorized_objects.items(),
            key=lambda pair: pair[0].__name__,
            )
        for base, names in categorized_objects:
            print('    {}:'.format(base.__name__))
            for name, class_ in names:
                print('        {} [{}]'.format(name, class_.__name__))
        sys.exit(1)

    def _handle_new(self, name, force=False):
        self._create_package_from_template(
            package_name=name,
            section=self._section_plural,
            force=force,
            )

    def _handle_rename(
        self,
        source_name,
        target_name,
        force=False,
        ):
        self._rename_package(
            source_name,
            target_name,
            self._section_plural,
            force=force,
            )

    def _handle_render(self, names, force=False):
        globbable_names = self._collect_globbable_names(names)
        print('Render candidates: {!r} ...'.format(
            ' '.join(globbable_names)))
        matching_paths = self._collect_matching_paths(
            globbable_names, self._section_plural)
        if not matching_paths:
            print('    No matching {}.'.format(self._section_plural))
            self._handle_list()
            sys.exit(1)
        for path in matching_paths:
            self._render_object(path, self._section_singular)
            print('    Rendered {path!s}{sep}'.format(
                path=path.relative_to(self.inner_project_path.parent),
                sep=os.path.sep))

    def _import_object(self, directory_path, section_singular, verbose=True):
        import_path = self._path_to_packagesystem_path(directory_path)
        definition_import_path = import_path + '.definition'
        try:
            module = self._import_path(
                definition_import_path,
                self.outer_project_path,
                verbose=verbose,
                )
            object_ = getattr(module, section_singular)
        except (ImportError, AttributeError):
            print(traceback.format_exc())
            sys.exit(1)
        return object_

    def _import_objects(self, section_plural, verbose=True):
        objects = collections.OrderedDict()
        for path in self._list_subpackages(section_plural):
            name = path.name
            object_ = self._import_object(
                path,
                self._section_singular,
                verbose=verbose,
                )
            objects[name] = object_
        return objects

    def _process_args_inner(self, args):
        if args.new is not None:
            self._handle_new(
                force=args.force,
                name=args.new,
                )
        if args.edit is not None:
            self._handle_edit(
                names=args.edit,
                )
        if args.list_:
            self._handle_list()
        if args.copy is not None:
            self._handle_copy(
                source_name=args.copy[0],
                target_name=args.copy[1],
                force=args.force,
                )
        if args.rename is not None:
            self._handle_rename(
                source_name=args.rename[0],
                target_name=args.rename[1],
                force=args.force,
                )
        if args.delete is not None:
            self._handle_delete(
                name=args.delete,
                )
        if args.render is not None:
            self._handle_render(
                force=args.force,
                names=args.render,
                )

    def _render_object(self, directory_path, section_singular):
        from supriya import render
        from supriya.tools import nonrealtimetools
        print('Rendering {path!s}{sep}'.format(
            path=directory_path.relative_to(self.inner_project_path.parent),
            sep=os.path.sep,
            ))
        output_file_path = directory_path / 'render.aiff'
        with systemtools.Timer() as timer:
            object_ = self._import_object(directory_path, section_singular)
            if hasattr(object_, '__session__'):
                object_ = object_.__session__()
            if not hasattr(object_, '__render__'):
                template = '    Cannot render {} of type {}.'
                message = template.format(
                    section_singular,
                    type(object_).__name__,
                    )
                print(message)
                sys.exit(1)
            kwargs = {}
            if isinstance(object_, nonrealtimetools.Session):
                kwargs.update(self._build_nrt_server_options(object_))
                kwargs.update({
                    'print_transcript': True,
                    'transcript_prefix': '    ',
                    'build_render_yml': True,
                    })
            try:
                render(
                    object_,
                    output_file_path=output_file_path,
                    render_directory_path=self._renders_path,
                    **kwargs
                    )
            except (NonrealtimeRenderError, NonrealtimeOutputMissing):
                self._report_time(timer, prefix='Python/SC runtime')
                print('    Render failed. Exiting.')
                sys.exit(1)
            except:
                print(traceback.format_exc())
                sys.exit(1)
            self._report_time(timer, prefix='Python/SC runtime')
        return output_file_path

    def _setup_argument_parser(self, parser):
        action_group = parser.add_argument_group('actions')
        action_group = action_group.add_mutually_exclusive_group(
            required=True)
        action_group.add_argument(
            '--new', '-N',
            help='create a new {}'.format(self._section_singular),
            metavar='NAME',
            )
        action_group.add_argument(
            '--edit', '-E',
            help='edit {}s'.format(self._section_singular),
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--render', '-R',
            help='render {}s'.format(self._section_singular),
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--list', '-L',
            dest='list_',
            help='list {}s'.format(self._section_singular),
            action='store_true',
            )
        action_group.add_argument(
            '--copy', '-Y',
            help='copy {}'.format(self._section_singular),
            metavar=('SOURCE', 'TARGET'),
            nargs=2,
            )
        action_group.add_argument(
            '--rename', '-M',
            help='rename {}'.format(self._section_singular),
            metavar=('SOURCE', 'TARGET'),
            nargs=2,
            )
        action_group.add_argument(
            '--delete', '-D',
            help='delete {}'.format(self._section_singular),
            metavar='NAME',
            )
        common_group = parser.add_argument_group('common options')
        common_group.add_argument(
            '--force', '-f',
            action='store_true',
            help='force overwriting',
            )
        common_group.add_argument(
            '--project-path',
            metavar='project',
            help='project path or package name',
            default=os.path.curdir,
            )
        common_group.add_argument(
            '--profile',
            action='store_true',
            help='display profiler info',
            )

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _section_plural(self):
        NotImplementedError

    @abc.abstractproperty
    def _section_singular(self):
        NotImplementedError
