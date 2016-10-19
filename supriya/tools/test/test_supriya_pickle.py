# -*- encoding: utf-8 -*-
import inspect
import pickle
import pytest
from supriya.tools import documentationtools


_classes_to_fix = (
    )

classes = documentationtools.list_all_supriya_classes()


@pytest.mark.skip()
@pytest.mark.parametrize('class_', classes)
def test_supriya_pickle_01(class_):
    r"""
    All storage-formattable classes are pickable.
    """
    if '_storage_format_specification' in dir(class_):
        if not inspect.isabstract(class_):
            if class_ not in _classes_to_fix:
                instance_one = class_()
                pickle_string = pickle.dumps(instance_one)
                instance_two = pickle.loads(pickle_string)
                instance_one_format = format(instance_one, 'storage')
                instance_two_format = format(instance_two, 'storage')
                assert instance_one_format == instance_two_format
