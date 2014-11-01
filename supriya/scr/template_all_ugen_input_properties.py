#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import inspect
from abjad.tools import stringtools
from supriya.tools import documentationtools
from supriya.tools import synthdeftools


def template_new_property(input_name, ugen_class):
    class_name = ugen_class.__name__
    lower_name = stringtools.to_snake_case(class_name)
    template_lines = [
        "",
        "    @property",
        "    def {input_name}(self):",
        "        r'''Gets `{input_name}` input of {class_name}.",
        "",
        "        ::",
        "",
        "            >>> {input_name} = None",
        "            >>> {lower_name} = ugentools.{class_name}.ar(",
        "            ...     {input_name}={input_name},",
        "            ...     )",
        "            >>> {lower_name}.{input_name}",
        "",
        "        Returns input.",
        "        '''",
        "        index = self._ordered_input_names.index('{input_name}')",
        "        return self._inputs[index]",
        ]
    formatted_lines = [
        line.format(
            class_name=class_name,
            input_name=input_name,
            lower_name=lower_name,
            )
        for line in template_lines
        ]
    return formatted_lines


def rebuild_ugen_source(ugen_class):
    attrs = dict(
        (attr.name, attr) for attr in
        inspect.classify_class_attrs(ugen_class)
        )
    missing_property_names = []
    for input_name in ugen_class._ordered_input_names:
        if input_name not in attrs:
            missing_property_names.append(input_name)
    ugen_source = inspect.findsource(ugen_class)[0]
    ugen_source = ''.join(ugen_source).splitlines()
    if missing_property_names:
        new_lines = []
        new_lines.append('')
        new_lines.append('    ### PUBLIC PROPERTIES ###')
        for property_name in sorted(missing_property_names):
            new_property_lines = template_new_property(
                property_name, ugen_class)
            new_lines.extend(new_property_lines)
        ugen_source.extend(new_lines)
    ugen_source = '\n'.join(ugen_source)
    return ugen_source


def run():
    all_ugen_classes = documentationtools.list_all_supriya_classes(
        bases=synthdeftools.UGen,
        )
    for ugen_class in all_ugen_classes:
        new_ugen_source = rebuild_ugen_source(ugen_class)
        source_file_name = inspect.getabsfile(ugen_class)
        with open(source_file_name, 'w') as file_pointer:
            file_pointer.write(new_ugen_source)


if __name__ == '__main__':
    run()