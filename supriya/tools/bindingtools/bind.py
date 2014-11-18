# -*- encoding: utf -*-


def bind(source, target):
    from supriya.tools import servertools
    binding = servertools.Binding()
    binding.bind(source, target)
    return binding