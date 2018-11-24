import pytest

import supriya.system


@pytest.mark.skip
def test_01():
    class TestClass:
        def __init__(self):
            self.value = 0

        def __call__(self, value):  # noqa
            self.value = value
            return value

    parent = TestClass()
    child = TestClass()
    binding = supriya.system.Binding(parent, child)
    assert binding.source is parent.__call__
    assert binding.target is child.__call__
    assert parent.__call__ is not child.__call__
    assert parent.__call__ is not TestClass.__call__
    assert child.__call__ is not TestClass.__call__
    assert parent.value == 0
    assert child.value == 0
    parent(1)
    assert parent.value == 1
    assert child.value == 1


def test_02():
    class TestClass:
        def __init__(self):
            self.value = 0

        @supriya.system.Bindable  # noqa
        def __call__(self, value):
            self.value = value
            return value

    parent = TestClass()
    child = TestClass()
    binding = supriya.system.Binding(parent, child)
    assert binding.source is parent.__call__
    assert binding.target is child.__call__
    assert parent.__call__ is not child.__call__
    assert parent.__call__ is not TestClass.__call__
    assert child.__call__ is not TestClass.__call__
    assert parent.value == 0
    assert child.value == 0
    parent(1)
    assert parent.value == 1
    assert child.value == 1


def test_03():
    class TestClass:
        def __init__(self):
            self.value = 0

        @supriya.system.Bindable(rebroadcast=True)  # noqa
        def __call__(self, value):
            self.value = value
            return value

    parent = TestClass()
    child = TestClass()
    binding = supriya.system.Binding(parent, child)
    assert binding.source is parent.__call__
    assert binding.target is child.__call__
    assert parent.__call__ is not child.__call__
    assert parent.__call__ is not TestClass.__call__
    assert child.__call__ is not TestClass.__call__
    assert parent.value == 0
    assert child.value == 0
    parent(1)
    assert parent.value == 1
    assert child.value == 1


def test_04():
    class TestClass:
        def __init__(self):
            self.value = 0

        @supriya.system.Bindable(rebroadcast=True)  # noqa
        def __call__(self, value):
            self.value = value
            return value

    parent = TestClass()
    child = TestClass()
    supriya.system.Binding(parent, child)
    assert parent.value == 0
    assert child.value == 0
    child(1)
    assert parent.value == 1
    assert child.value == 1


def test_05():
    class TestClass:
        def __init__(self):
            self.value = 0

        @supriya.system.Bindable(rebroadcast=True)  # noqa
        def __call__(self, value):
            self.value = value
            return value

    node_a = TestClass()
    node_b = TestClass()
    node_c = TestClass()
    node_d = TestClass()
    supriya.system.Binding(node_a, node_b)
    supriya.system.Binding(node_a, node_c)
    supriya.system.Binding(node_c, node_d)
    assert node_a.value == 0
    assert node_b.value == 0
    assert node_c.value == 0
    assert node_d.value == 0
    node_b(1)
    assert node_a.value == 1
    assert node_b.value == 1
    assert node_c.value == 1
    assert node_d.value == 1


def test_06():
    class TestClass:
        def __init__(self):
            self.value = 0

        @supriya.system.Bindable(rebroadcast=True)  # noqa
        def __call__(self, value):
            self.value = value
            return value

    node_a = TestClass()
    node_b = TestClass()
    supriya.system.Binding(node_a, node_b)
    supriya.system.Binding(node_b, node_a)
    assert node_a.value == 0
    assert node_b.value == 0
    node_a(1)
    assert node_a.value == 1
    assert node_b.value == 1


@pytest.mark.skip
def test_07():
    class TestClass:
        __slots__ = ("value", "__weakref__")

        def __init__(self):  # noqa
            self.value = 0

        def __call__(self, value):  # noqa
            self.value = value
            return value

    parent = TestClass()
    child = TestClass()
    binding = supriya.system.Binding(parent, child)
    assert binding.source is parent.__call__
    assert binding.target is child.__call__
    assert parent.__call__ is not child.__call__
    assert parent.__call__ is not TestClass.__call__
    assert child.__call__ is not TestClass.__call__
    assert parent.value == 0
    assert child.value == 0
    parent(1)
    assert parent.value == 1
    assert child.value == 1


@pytest.mark.skip
def test_08():
    class TestClass(supriya.system.SupriyaObject):
        __slots__ = ("value",)

        def __init__(self):  # noqa
            self.value = 0

        def __call__(self, value):  # noqa
            self.value = value
            return value

    parent = TestClass()
    child = TestClass()
    binding = supriya.system.Binding(parent, child)
    assert binding.source is parent.__call__
    assert binding.target is child.__call__
    assert parent.__call__ is not child.__call__
    assert parent.__call__ is not TestClass.__call__
    assert child.__call__ is not TestClass.__call__
    assert parent.value == 0
    assert child.value == 0
    parent(1)
    assert parent.value == 1
    assert child.value == 1
