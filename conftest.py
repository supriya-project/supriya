import abjad
import pytest
import supriya


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace.update(supriya.__dict__)
    doctest_namespace['abjad'] = abjad
    doctest_namespace['supriya'] = supriya


@pytest.fixture(autouse=True)
def server_shutdown():
    for server in supriya.Server._servers.values():
        server.quit()
    yield
    for server in supriya.Server._servers.values():
        server.quit()
