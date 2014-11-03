#! /usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import print_function
import os
import supriya
from abjad import stringtools
from supriya.etc.ugens import ugens as ugen_definitions
from supriya.tools import ugentools


def make_class_methods(ugen_definition):
    result = [
        '    ### PUBLIC METHODS ###',
        '',
        ]
    if 'methods' not in ugen_definition:
        return []
    for method_name in sorted(ugen_definition['methods']):
        if method_name not in ('ar', 'ir', 'kr', 'new', 'tr'):
            result.append('    # def {}(): ...'.format(method_name))
            result.append('')
            continue
        method_signature = ugen_definition['methods'][method_name]
        method_signature = process_method_signature(method_signature)
        result.append('    @classmethod')
        result.append('    def {}('.format(method_name))
        result.append('        cls,')
        for name, value in method_signature:
            result.append('        {}={},'.format(name, value))
        result.append('        ):')
        result.append('        from supriya.tools import synthdeftools')
        result.append('        rate = None')
        result.append('        ugen = cls._new_expanded(')
        result.append('            rate=rate,')
        for name, value in method_signature:
            result.append('            {}={},'.format(name, name))
        result.append('            )')
        result.append('        return ugen')
        result.append('')
    return result


def make_class_variables():
    result = [
        '    ### CLASS VARIABLES ###',
        '',
        '    __documentation_section__ = None',
        '',
        '    __slots__ = ()',
        '',
        '    _ordered_input_names = (',
        '        )',
        '',
        '    _valid_rates = None',
        '',
        ]
    return result


def make_import(ugen_parent):
    result = []
    if ugen_parent == 'UGen':
        string = 'from supriya.tools.synthdeftools.UGen import UGen'
    else:
        string = 'from supriya.tools.ugentools.{parent} import {parent}'
    string = string.format(parent=ugen_parent)
    result.extend([string, '', ''])
    return result


def process_method_signature(method_signature):
    result = []
    for name, value in method_signature:
        if name == 'in':
            name = 'source' 
        elif name == 'freq':
            name = 'frequency'
        elif name == 'trig':
            name = 'trigger'
        elif name == 'rq':
            name = 'reciprocal_of_q'
        elif name == 'dur':
            name = 'duration'
        elif name == 'buffernum':
            name = 'buffer_id',
        elif name == 'num_channels':
            name = 'channel_count'
        name = stringtools.to_snake_case(name)
        if name.endswith('freq'):
            name = name.replace('freq', 'frequency')
        if name in ('add', 'mul', 'nil', 'this'):
            continue
        result.append((name, value))
    result.sort()
    return result


def make_initializer(ugen_definition):
    result = [
        '    ### INITIALIZER ###',
        '',
        ]
    if 'methods' not in ugen_definition:
        result.append('    def __init__(self):')
        result.append('        pass')
        result.append('')
        return result
    methods = ugen_definition['methods']
    method_signature = None
    if 'ar' in methods:
        method_signature = methods['ar']
    elif 'ir' in methods:
        method_signature = methods['ir']
    elif 'kr' in methods:
        method_signature = methods['kr']
    if method_signature is not None:
        method_signature = process_method_signature(method_signature)
        result.append('    def __init__(')
        result.append('        self,')
        result.append('        rate=None')
        for name, value in method_signature:
            result.append('        {}={},'.format(name, value))
        result.append('        ):')
        result.append('        {}.__init__('.format(ugen_definition['parent']))
        result.append('            self,')
        for name, value in method_signature:
            result.append('            {}={},'.format(name, name))
        result.append('            )')
        result.append('')
    return result


def make_ugen_module(ugen_name, ugen_definition):
    result = []
    result.append('# -*- encoding: utf-8 -*-')
    result.extend(make_import(ugen_definition['parent']))
    result.append('class {}({}):'.format(ugen_name, ugen_definition['parent']))
    result.append('')
    result.extend(make_class_variables())
    result.extend(make_initializer(ugen_definition))
    result.extend(make_class_methods(ugen_definition))
    result = '\n'.join(result)
    return result


def run():
    counter = 0
    for ugen_name in ugen_definitions:
        if ugen_name == 'UGen':
            continue
        elif ugen_name in dir(ugentools):
            continue
        counter += 1
        print()
        print('COUNTER:', counter)
        print()
        ugen_definition = ugen_definitions[ugen_name]
        ugen_module_string = make_ugen_module(ugen_name, ugen_definition)
        ugen_module_path = os.path.join(
            supriya.__path__[0],
            'tools',
            'pendingugens',
            '{}.py'.format(ugen_name),
            )
        with open(ugen_module_path, 'w') as file_pointer:
            file_pointer.write(ugen_module_string)
        #print(ugen_module_string)


if __name__ == '__main__':
    run()