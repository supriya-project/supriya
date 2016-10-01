# -*- encoding: utf-8 -*-
import inspect
import pytest
from supriya.tools import documentationtools


pytestmark = pytest.mark.skip()


classes = documentationtools.list_all_supriya_classes()


@pytest.mark.skip()
@pytest.mark.parametrize('class_', classes)
def test_supriya___hash___01(class_):
    r'''All concrete classes with __hash__ can hash.
    '''
    if not inspect.isabstract(class_):
        if getattr(class_, '__hash__', None):
            instance = class_()
            value = hash(instance)
            assert isinstance(value, int)
