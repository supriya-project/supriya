import doctest
import pathlib
import re
import types
import unittest
from io import StringIO
from supriya import utils


class TestCase(unittest.TestCase):

    ### CLASS VARIABLES ###

    ansi_escape = re.compile(r'\x1b[^m]*m')

    ### PUBLIC METHODS ###

    def compare_captured_output(self, expected):
        actual = self.ansi_escape.sub('', self.string_io.getvalue())
        actual = utils.normalize_string(actual)
        expected = utils.normalize_string(expected)
        self.compare_strings(expected, actual)

    def compare_file_contents(self, path, expected_contents):
        expected_contents = utils.normalize_string(expected_contents)
        with open(str(path), 'r') as file_pointer:
            actual_contents = utils.normalize_string(file_pointer.read())
        self.compare_strings(expected_contents, actual_contents)

    def compare_path_contents(self, path_to_search, expected_files):
        actual_files = sorted(
            str(path.relative_to(self.test_path))
            for path in path_to_search.glob('**/*.*')
            if '__pycache__' not in path.parts and
            path.suffix != '.pyc'
            )
        self.compare_strings(
            '\n'.join(str(_) for _ in actual_files),
            '\n'.join(str(_) for _ in expected_files),
            )

    def compare_strings(self, expected, actual):
        actual = self.normalize(self.ansi_escape.sub('', actual))
        expected = self.normalize(self.ansi_escape.sub('', expected))
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
