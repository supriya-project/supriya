#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import inspect
from supriya.tools import documentationtools
from supriya.tools import synthdeftools


def template_new_property(input_name, ugen_class):
    class_name = ugen_class.__name__
    lower_name = stringtools.to_snake_case(class_name)
    template_lines = [
        ""
        "    @property"
        "    def {input_name}(self):"
        "        r'''Gets `{input_name}` input of {class_name}."
        ""
        "        ::"
        ""
        "            >>> {lower_name} = ugentools.{class_name}.ar({input_name}=0.5)"
        "            >>> {lower_name}.{input_name}"
        ""
        "        Returns input."
        "        '''"
        "        index = self._ordered_input_names.index('{}')"
        "        return self._inputs[index]"
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
    new_lines = []
    for property_name in missing_properties:
        new_property_lines = template_new_property(input_name, ugen_class)
        new_lines.extend(new_property_lines)
    ugen_source.extend(new_lines)
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