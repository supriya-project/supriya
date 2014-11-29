# -*- encoding: utf-8 -*-
import copy
import inspect
import pytest
from supriya.tools import documentationtools


pytest.skip()


_classes_to_fix = (
    )

classes = documentationtools.list_all_supriya_classes()


@pytest.mark.parametrize('class_', classes)
def test_supriya___deepcopy___01(class_):
    r'''All concrete classes with a storage format can copy.
    '''
    if '_storage_format_specification' not in dir(class_):
        return
    if inspect.isabstract(class_):
        return
    if class_ in _classes_to_fix:
        return
    instance_one = class_()
    instance_two = copy.deepcopy(instance_one)
    instance_one_format = format(instance_one, 'storage')
    instance_two_format = format(instance_two, 'storage')
    assert instance_one_format == instance_two_format
    # TODO: eventually this second asset should also pass
    #assert instance_one == instance_two