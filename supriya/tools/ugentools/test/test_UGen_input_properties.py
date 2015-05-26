# -*- encoding: utf-8 -*-
import inspect
import pytest
from supriya.tools import documentationtools
from supriya.tools import synthdeftools


classes = documentationtools.list_all_supriya_classes(
    bases=ugentools.UGen,
    )

classes = [_ for _ in classes if '.ugentools.' in _.__module__]

pairs = []
for cls in classes:
    if inspect.isabstract(cls):
        continue
    attrs = inspect.classify_class_attrs(cls)
    ordered_input_names_attr = None
    for attr in attrs:
        if attr.name == '_ordered_input_names':
            ordered_input_names_attr = attr
            break
    if ordered_input_names_attr is None:
        continue
    ordered_input_names = ordered_input_names_attr.object
    for input_name in ordered_input_names:
        pairs.append((cls, input_name))
pairs.sort(key=lambda x: (x[0].__name__, x[1]))


@pytest.mark.parametrize('pair', pairs)
def test_UGen_input_properties_01(pair):
    r'''All classes have a docstring.
    '''
    cls, input_name = pair
    if not hasattr(cls, input_name):
        message = '{} has no input property for: {}'.format(
            cls.__name__,
            input_name,
            )
        raise Exception(message)