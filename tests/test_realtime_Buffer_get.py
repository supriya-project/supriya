import collections
import supriya.realtime
import supriya.system


class Test(supriya.system.TestCase):

    def setUp(self):
        super(supriya.system.TestCase, self).setUp()
        self.server = supriya.realtime.Server().boot()

    def tearDown(self):
        self.server.quit()
        super(supriya.system.TestCase, self).tearDown()

    def test_01(self):
        buffer_ = supriya.realtime.Buffer()
        buffer_.allocate(frame_count=8, sync=True)
        response = buffer_.get((0,))
        result = response.as_dict()
        assert result == collections.OrderedDict([
            (0, 0),
            ])
        response = buffer_.get((0, 1, 2, 3))
        result = response.as_dict()
        assert result == collections.OrderedDict([
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            ])
        response = buffer_.get((7, 6, 2, 5, 1))
        result = response.as_dict()
        assert result == collections.OrderedDict([
            (7, 0),
            (6, 0),
            (2, 0),
            (5, 0),
            (1, 0),
            ])
        buffer_.free()

    def test_02(self):
        buffer_ = supriya.realtime.Buffer()
        buffer_.allocate(frame_count=8, sync=True)
        buffer_.set_contiguous(
            index_values_pairs=(
                (0, (1, 2, 3, 4, 5, 6, 7, 8)),
                ),
            )
        response = buffer_.get((0, 1, 2, 3, 4, 5, 6, 7))
        result = response.as_dict()
        assert result == collections.OrderedDict([
            (0, 1.0),
            (1, 2.0),
            (2, 3.0),
            (3, 4.0),
            (4, 5.0),
            (5, 6.0),
            (6, 7.0),
            (7, 8.0),
            ])
        buffer_.set(
            index_value_pairs=(
                (2, -1.5),
                (4, -2.125),
                ),
            )
        response = buffer_.get((7, 6, 5, 4, 3, 2, 1, 0))
        result = response.as_dict()
        assert result == collections.OrderedDict([
            (7, 8.0),
            (6, 7.0),
            (5, 6.0),
            (4, -2.125),
            (3, 4.0),
            (2, -1.5),
            (1, 2.0),
            (0, 1.0),
            ])
        buffer_.free()
