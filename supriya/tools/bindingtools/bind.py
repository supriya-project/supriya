# -*- encoding: utf -*-


def bind(source, target, range_=None, exponent=None):
    from supriya.tools import bindingtools
    binding = bindingtools.Binding()
    binding.bind(source, target, range_=range_, exponent=exponent)
    return binding
