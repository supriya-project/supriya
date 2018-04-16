import doctest
import pathlib
import re
import types
import unittest
import uqbar.strings
from io import StringIO


class TestCase(unittest.TestCase):

    ### CLASS VARIABLES ###

    ansi_escape = re.compile(r'\x1b[^m]*m')

    ### PUBLIC METHODS ###

    def compare_captured_output(self, expected):
        actual = self.ansi_escape.sub('', self.string_io.getvalue())
        actual = uqbar.strings.normalize(actual)
        expected = uqbar.strings.normalize(expected)
        self.compare_strings(expected, actual)

    def compare_file_contents(self, path, expected_contents):
        expected_contents = uqbar.strings.normalize(expected_contents)
        with open(str(path), 'r') as file_pointer:
            actual_contents = uqbar.strings.normalize(file_pointer.read())
        self.compare_strings(expected_contents, actual_contents)

    def compare_path_contents(self, path_to_search, expected_files):
        actual_files = sorted(
            str(path.relative_to(self.test_path))
            for path in sorted(path_to_search.glob('**/*.*'))
            if '__pycache__' not in path.parts and
            path.suffix != '.pyc'
            )
        self.compare_strings(
            '\n'.join(str(_) for _ in actual_files),
            '\n'.join(str(_) for _ in expected_files),
            )

    def compare_strings(cls, expected, actual):
        actual = cls.normalize(cls.ansi_escape.sub('', actual))
        expected = cls.normalize(cls.ansi_escape.sub('', expected))
        example = types.SimpleNamespace()
        example.want = expected
        output_checker = doctest.OutputChecker()
        flags = (
            doctest.NORMALIZE_WHITESPACE |
            doctest.ELLIPSIS |
            doctest.REPORT_NDIFF
            )
        success = output_checker.check_output(expected, actual, flags)
        if not success:
            diff = output_checker.output_difference(example, actual, flags)
            raise Exception(diff)

    def get_objects_as_string(self, objects, replace_uuids=False):
        pattern = re.compile(r"\bUUID\('(.*)'\)")
        objects_string = '\n'.join(format(x) for x in objects)
        if replace_uuids:
            matches = []
            search_offset = 0
            while True:
                match = pattern.search(objects_string, search_offset)
                if not match:
                    break
                group = match.groups()[0]
                if group not in matches:
                    matches.append(group)
                search_offset = match.end()
            for i, match in enumerate(matches, 65):
                objects_string = objects_string.replace(match, chr(i))
        return objects_string

    def normalize(self, string):
        return uqbar.strings.normalize(string)

    def reset_string_io(self):
        self.string_io.close()
        self.string_io = StringIO()

    def setUp(self):
        self.string_io = StringIO()

    def tearDown(self):
        self.string_io.close()

    ### PUBLIC PROPERTIES ###

    @property
    def test_path(self):
        return pathlib.Path(__file__).parent
