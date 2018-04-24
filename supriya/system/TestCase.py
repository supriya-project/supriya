import re
import pytest
import pathlib
import unittest
from io import StringIO


class TestCase(unittest.TestCase):

    ### PUBLIC METHODS ###

    ansi_escape = re.compile(r'\x1b[^m]*m')

    def compare_file_contents(self, path, expected_contents):
        with pathlib.Path(path).open('r') as file_pointer:
            actual_contents = file_pointer.read()
        pytest.helpers.compare_strings(expected_contents, actual_contents)

    def compare_path_contents(self, path_to_search, expected_files):
        actual_files = sorted(
            str(path.relative_to(self.test_path))
            for path in sorted(path_to_search.glob('**/*.*'))
            if '__pycache__' not in path.parts and
            path.suffix != '.pyc'
            )
        pytest.helpers.compare_strings(
            '\n'.join(str(_) for _ in actual_files),
            '\n'.join(str(_) for _ in expected_files),
            )

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
