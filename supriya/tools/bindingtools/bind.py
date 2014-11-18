# -*- encoding: utf -*-


def bind(source, target):
    from supriya.tools import bindingtools
    binding = bindingtools.Binding()
    binding.bind(source, target)
    return binding