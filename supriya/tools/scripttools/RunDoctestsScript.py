# -*- encoding: utf-8 -*-
from __future__ import print_function
import doctest
import importlib
import os
import sys
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.commandlinetools.DirectoryScript import DirectoryScript
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class RunDoctestsScript(DirectoryScript):
    r'''Runs doctests on all Python files in current directory recursively.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Alias of script.

        Returns ``'doctest'``.
        '''
        return 'doctest'

    @property
    def long_description(self):
        r'''Long description of  script.

        Returns string or none.
        '''
        return None

    @property
    def scripting_group(self):
        r'''Scripting group of script.

        Returns none.
        '''
        return None

    @property
    def short_description(self):
        r'''Short description of script.

        Returns string.
        '''
        return 'Run doctests on all modules in current path.'

    @property
    def version(self):
        r'''Version of script.

        Returns float.
        '''
        return 1.0

    ### PRIVATE METHODS ###

    def _get_file_paths(self, args):
        file_paths = []
        if os.path.isdir(args.path):
            for dir_path, dir_names, file_names in os.walk(args.path):
                if not os.path.exists(os.path.join(dir_path, '__init__.py')):
                    continue
                dir_names[:] = [_ for _ in dir_names if not _.startswith('.')]
                for file_name in sorted(file_names):
                    if (file_name.endswith('.py') and
                        not file_name.startswith('test_') and
                        not file_name == '__init__.py'):
                        file_path = os.path.abspath(
                            os.path.join(dir_path, file_name))
                        file_paths.append(file_path)
        elif os.path.isfile(args.path):
            file_paths.append(args.path)
        return file_paths

    def _get_globs(self):
        globs = importlib.import_module('supriya').__dict__.copy()
        globs['print_function'] = print_function
        return globs

    def _get_option_flags(self, args):
        option_flags = (
            doctest.NORMALIZE_WHITESPACE |
            doctest.ELLIPSIS
            )
        if args and args.diff:
            option_flags = option_flags | doctest.REPORT_NDIFF
        if args and args.x:
            option_flags = option_flags | doctest.REPORT_ONLY_FIRST_FAILURE
        return option_flags

    def _report_summary(
        self,
        error_messages,
        failed_file_paths,
        total_modules,
        total_successes,
        total_tests,
        ):
        if failed_file_paths:
            print()
            for error_message in error_messages:
                print(error_message)
        for file_path in failed_file_paths:
            string = 'FAILED: {}'.format(file_path)
            print(string)
        print()
        test_identifier = stringtools.pluralize('test', total_tests)
        module_identifier = stringtools.pluralize('module', total_modules)
        string = '{} of {} {} passed in {} {}.'
        string = string.format(
            total_successes,
            total_tests,
            test_identifier,
            total_modules,
            module_identifier,
            )
        print(string)
        if total_successes == total_tests:
            sys.exit(0)
        else:
            sys.exit(1)

    def _test_file_paths(
        self,
        args,
        file_paths,
        globs,
        option_flags,
        ):
        from supriya.tools import servertools
        globs = globs.copy()
        total_failures = 0
        total_modules = 0
        total_tests = 0
        failed_file_paths = []
        error_messages = []
        for file_path in file_paths:
            total_modules += 1
            relative_path = os.path.relpath(file_path)
            string_buffer = StringIO()
            with systemtools.RedirectedStreams(stdout=string_buffer):
                failure_count, test_count = doctest.testfile(
                    file_path,
                    module_relative=False,
                    globs=globs,
                    optionflags=option_flags,
                    )
            if failure_count:
                failed_file_paths.append(os.path.relpath(file_path))
                error_messages.append(string_buffer.getvalue())
                string_buffer.close()
                result_code = ''.join((
                    self.colors['RED'],
                    'FAILED',
                    self.colors['END'],
                    ))
                print(relative_path, result_code)
                if args and args.x:
                    break
            else:
                result_code = ''.join((
                    self.colors['BLUE'],
                    'OK',
                    self.colors['END'],
                    ))
                print(relative_path, result_code)
            total_failures += failure_count
            total_tests += test_count
            servertools.Server().quit()
            for server in servertools.Server._servers.values():
                server.quit()
        results = (
            error_messages,
            failed_file_paths,
            total_failures,
            total_modules,
            total_tests,
            )
        return results

    ### PUBLIC PROPERTIES ###

    def process_args(
        self,
        args=None,
        ):
        r'''Processes `args`.

        Returns none.
        '''
        globs = self._get_globs()
        option_flags = self._get_option_flags(args)
        file_paths = self._get_file_paths(args)
        results = self._test_file_paths(
            args,
            file_paths,
            globs,
            option_flags,
            )
        error_messages = results[0]
        failed_file_paths = results[1]
        total_failures = results[2]
        total_modules = results[3]
        total_tests = results[4]
        total_successes = total_tests - total_failures
        self._report_summary(
            error_messages,
            failed_file_paths,
            total_modules,
            total_successes,
            total_tests,
            )

    def setup_argument_parser(self, parser):
        r'''Sets up argument `parser`.

        Returns none.
        '''
        parser.add_argument(
            'path',
            default=os.getcwd(),
            help='directory tree to be recursed over',
            nargs='?',
            )
        parser.add_argument(
            '--diff',
            action='store_true',
            help='print diff-like output on failed tests.',
            )
        parser.add_argument(
            '-x',
            action='store_true',
            help='stop after first failure.',
            )