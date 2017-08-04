import abjad
import pytest


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace['abjad'] = abjad
    doctest_namespace['supriya'] = supriya
