# -*- encoding: utf-8 -*-
import functools
import inspect
import pytest
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from supriya.tools import documentationtools


pytest.skip()


classes = documentationtools.list_all_supriya_classes()

valid_types = (
    bool,
    float,
    int,
    str,
    tuple,
    type(None),
    datastructuretools.OrdinalConstant,
    durationtools.Duration,
    mathtools.Infinity,
    mathtools.NegativeInfinity,
    )

functions = documentationtools.list_all_supriya_functions()


@pytest.mark.parametrize('class_', classes)
def test_supriya___init___01(class_):
    r'''All concrete classes initialize from empty input.
    '''
    if not inspect.isabstract(class_):
        instance = class_()
        assert instance is not None


@pytest.mark.parametrize('obj', classes)
def test_supriya___init___02(obj):
    r'''Make sure class initializer keyword argument values are immutable.
    '''
    for attr in inspect.classify_class_attrs(obj):
        if attr.defining_class is not obj:
            continue
        elif attr.kind != 'method':
            continue
        obj = attr.object
        if isinstance(obj, functools.partial):
            obj = obj.function
        argument_specification = inspect.getargspec(obj)
        keyword_argument_names = argument_specification.args[1:]
        keyword_argument_values = argument_specification.defaults
        if keyword_argument_values is None:
            continue
        for name, value in zip(
            keyword_argument_names, keyword_argument_values):
            assert isinstance(value, valid_types), (attr.name, name, value)
            if isinstance(value, tuple):
                assert all(isinstance(x, valid_types) for x in value)


@pytest.mark.parametrize('obj', functions)
def test_supriya___init___03(obj):
    r'''Make sure function keyword argument values are immutable.
    '''
    if isinstance(obj, functools.partial):
        obj = obj.function
    argument_specification = inspect.getargspec(obj)
    keyword_argument_names = argument_specification.args[1:]
    keyword_argument_values = argument_specification.defaults
    if keyword_argument_values is None:
        return
    for name, value in zip(
        keyword_argument_names, keyword_argument_values):
        assert isinstance(value, valid_types), (name, value)
        if isinstance(value, tuple):
            assert all(isinstance(x, valid_types) for x in value)