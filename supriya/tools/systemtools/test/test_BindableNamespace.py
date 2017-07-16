from supriya.tools import systemtools
from abjad.tools.systemtools import TestCase


class TestCase(TestCase):

    def test_01(self):

        class TestClass:
            def __init__(self):
                self.value = 0

            @systemtools.Bindable(rebroadcast=True)
            def __call__(self, value):  # noqa
                self.value = value
                return value

        namespace = systemtools.BindableNamespace(foo=10, bar=20, baz=30)
        source = TestClass()
        target = TestClass()
        systemtools.Binding(source, namespace.proxies['bar'])
        systemtools.Binding(namespace.proxies['bar'], target)

        assert sorted(namespace.items()) == [('bar', 20), ('baz', 30), ('foo', 10)]
        assert namespace['bar'] == 20

        assert source(666) == 666
        assert source.value == 666
        assert namespace['bar'] == 666
        assert sorted(namespace.items()) == [('bar', 666), ('baz', 30), ('foo', 10)]
        assert target.value == 666

        assert namespace.proxies['bar'](-23)
        assert source.value == -23
        assert namespace['bar'] == -23
        assert sorted(namespace.items()) == [('bar', -23), ('baz', 30), ('foo', 10)]
        assert target.value == -23

        namespace['bar'] = 17
        assert source.value == 17
        assert namespace['bar'] == 17
        assert sorted(namespace.items()) == [('bar', 17), ('baz', 30), ('foo', 10)]
        assert target.value == 17

        assert target(2046) == 2046
        assert source.value == 2046
        assert namespace['bar'] == 2046
        assert sorted(namespace.items()) == [('bar', 2046), ('baz', 30), ('foo', 10)]
        assert target.value == 2046

    def test_02(self):
        namespace = systemtools.BindableNamespace(foo=10, bar=20, baz=30)
        with self.assertRaises(KeyError):
            namespace['quux'] = 'wux'
