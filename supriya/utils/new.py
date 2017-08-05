import inspect


def new(expr, *args, **kwargs):
    """
    Template an object.
    """
    #print('I', expr, args, kwargs)
    try:
        signature = inspect.signature(expr)
    except TypeError:
        signature = inspect.signature(expr.__init__)
    new_args = []
    new_kwargs = {}
    for name, parameter in signature.parameters.items():
        #print('    P', name, repr(parameter))
        if parameter.kind is inspect._POSITIONAL_ONLY:
            try:
                new_args.append(getattr(expr, name))
            except AttributeError:
                new_args.append(expr[name])
        elif parameter.kind is inspect._POSITIONAL_OR_KEYWORD:
            try:
                new_kwargs[name] = getattr(expr, name)
            except AttributeError:
                new_kwargs[name] = expr[name]
        elif parameter.kind is inspect._VAR_POSITIONAL:
            try:
                new_args.extend(expr[:])
            except TypeError:
                new_args.extend(getattr(expr, name))
        elif parameter.kind is inspect._KEYWORD_ONLY:
            try:
                new_kwargs[name] = getattr(expr, name)
            except AttributeError:
                new_kwargs[name] = expr[name]
        elif parameter.kind is inspect._VAR_KEYWORD:
            if hasattr(expr, 'items'):
                new_kwargs.update(expr)
            else:
                new_kwargs.update(getattr(expr, name))
    if args:
        new_args = args
    new_kwargs.update(kwargs)
    return type(expr)(*new_args, **new_kwargs)
