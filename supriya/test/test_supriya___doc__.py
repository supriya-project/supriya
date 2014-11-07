# -*- encoding: utf-8 -*-
import inspect
import pytest
from supriya.tools import documentationtools
from supriya.tools import synthdeftools


ignored_names = (
    '__dict__',
    '__init__',
    '__new__',
    '__weakref__',
    )

ignored_classes = (
    )

classes = documentationtools.list_all_supriya_classes(
    bases=synthdeftools.UGen,
    )

classes = [_ for _ in classes if '.ugentools.' in _.__module__]

class_attr_pairs = []
for cls in classes:
    if cls.__name__ in ignored_classes:
        continue
    attrs = inspect.classify_class_attrs(cls)
    for attr in attrs:
        if attr.name in ignored_names:
            continue
        elif attr.defining_class is not cls:
            continue
        elif attr.kind == 'data':
            continue
        class_attr_pairs.append((cls, attr))

functions = documentationtools.list_all_supriya_functions()


@pytest.mark.parametrize('obj', classes)
def test_supriya___doc___01(obj):
    r'''All classes have a docstring.
    '''
    if obj.__doc__ is None:
        message = 'No documentation for: {}'.format(obj.__name__)
        raise Exception(message)


@pytest.mark.parametrize('pair', class_attr_pairs)
def test_supriya___doc___02(pair):
    r'''All methods and properties have a docstring.
    '''
    cls, attr = pair
    if attr.name[0].isalpha() or attr.name.startswith('__'):
        if getattr(cls, attr.name).__doc__ is None:
            message = 'No documentation for: {}.{}'
            message = message.format(cls.__name__, attr.name)
            raise Exception(message)


@pytest.mark.parametrize('obj', functions)
def test_supriya___doc___03(obj):
    r'''All functions have a docstring.
    '''
    if obj.__doc__ is None:
        message = 'No documentation for: {}'.format(obj.__name__)
        raise Exception(message)