# -*- encoding: utf-8 -*-
import pytest
from supriya import responsetools
from supriya import servertools


@pytest.fixture(scope='function')
def server(request):
    def server_teardown():
        server.quit()
    server = servertools.Server().boot()
    request.addfinalizer(server_teardown)
    return server


def test_Buffer_get_01(server):

    buffer_ = servertools.Buffer()
    buffer_.allocate(frame_count=8)
    server.sync()

    response = buffer_.get((0,))
    assert response == \
        responsetools.BufferSetResponse(
            buffer_id=0,
            items=(
                responsetools.BufferSetItem(
                    sample_index=0,
                    sample_value=0.0
                    ),
                )
            )

    response = buffer_.get((0, 1, 2, 3))
    assert response == \
        responsetools.BufferSetResponse(
            buffer_id=0,
            items=(
                responsetools.BufferSetItem(
                    sample_index=0,
                    sample_value=0.0
                    ),
                responsetools.BufferSetItem(
                    sample_index=1,
                    sample_value=0.0
                    ),
                responsetools.BufferSetItem(
                    sample_index=2,
                    sample_value=0.0
                    ),
                responsetools.BufferSetItem(
                    sample_index=3,
                    sample_value=0.0
                    ),
                )
            )

    response = buffer_.get((7, 6, 2, 5, 1))
    assert response == \
        responsetools.BufferSetResponse(
            buffer_id=0,
            items=(
                responsetools.BufferSetItem(
                    sample_index=7,
                    sample_value=0.0
                    ),
                responsetools.BufferSetItem(
                    sample_index=6,
                    sample_value=0.0
                    ),
                responsetools.BufferSetItem(
                    sample_index=2,
                    sample_value=0.0
                    ),
                responsetools.BufferSetItem(
                    sample_index=5,
                    sample_value=0.0
                    ),
                responsetools.BufferSetItem(
                    sample_index=1,
                    sample_value=0.0
                    ),
                )
            )

    buffer_.free()
