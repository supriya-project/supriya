import collections
import inspect


def get_object_vars(expr):
    #print('VARS?', type(expr))
    if hasattr(expr, '__init__'):
        signature = inspect.signature(expr.__init__)
    elif hasattr(expr, '__new__'):
        signature = inspect.signature(expr.__new__)
    else:
        raise TypeError(type(expr))
    args = collections.OrderedDict()
    var_args = []
    kwargs = {}
    for i, (name, parameter) in enumerate(signature.parameters.items()):
        #print('   ', parameter)
        if parameter.kind is inspect._POSITIONAL_ONLY:
            try:
                args[name] = getattr(expr, name)
            except AttributeError:
                args[name] = expr[name]
        elif parameter.kind is inspect._POSITIONAL_OR_KEYWORD:
            try:
                args[name] = getattr(expr, name)
            except AttributeError:
                args[name] = expr[name]
        elif parameter.kind is inspect._VAR_POSITIONAL:
            try:
                var_args.extend(expr[:])
            except TypeError:
                var_args.extend(getattr(expr, name))
        elif parameter.kind is inspect._KEYWORD_ONLY:
            try:
                kwargs[name] = getattr(expr, name)
            except AttributeError:
                kwargs[name] = expr[name]
        elif parameter.kind is inspect._VAR_KEYWORD:
            if hasattr(expr, 'items'):
                items = expr.items()
            else:
                items = getattr(expr, name).items()
            for key, value in items:
                if key not in args:
                    kwargs[key] = value
    return args, var_args, kwargs
