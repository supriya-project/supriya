# -*- encoding: utf-8 -*-
import inspect
import pytest
import supriya
from supriya.tools import documentationtools


classes = documentationtools.list_all_supriya_classes()

_classes_to_temporarily_skip = (
    )


@pytest.mark.skip()
@pytest.mark.parametrize('class_', classes)
def test_supriya___format___01(class_):
    r"""
    All concrete classes have a storage format.
    """
    if '_storage_format_specification' in dir(class_) and \
        not inspect.isabstract(class_):
        instance = class_()
        instance_format = format(instance, 'storage')
        assert isinstance(instance_format, str)
        assert not instance_format == ''


@pytest.mark.parametrize('class_', classes)
@pytest.mark.skip()
def test_supriya___format___02(class_):
    r"""
    All storage-formattable classes have evaluable storage format.
    """
    if '_storage_format_specification' in dir(class_) and \
        not inspect.isabstract(class_) and \
        class_ not in _classes_to_temporarily_skip:
        environment = supriya.__dict__.copy()
        environment.update(supriya.demos.__dict__)
        instance_one = class_()
        instance_one_format = format(instance_one, 'storage')
        assert isinstance(instance_one_format, str)
        assert instance_one_format != ''
        instance_two = eval(instance_one_format, environment)
        instance_two_format = format(instance_two, 'storage')
        assert instance_one_format == instance_two_format
