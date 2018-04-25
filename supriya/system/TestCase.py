import re
import pytest
import pathlib
import unittest


class TestCase(unittest.TestCase):

    ### PUBLIC METHODS ###

    ansi_escape = re.compile(r'\x1b[^m]*m')

    def compare_file_contents(self, path, expected_contents):
        with pathlib.Path(path).open('r') as file_pointer:
            actual_contents = file_pointer.read()
        pytest.helpers.compare_strings(expected_contents, actual_contents)

    ### PUBLIC PROPERTIES ###

    @property
    def test_path(self):
        return pathlib.Path(__file__).parent
