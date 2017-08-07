def new(expr, *args, **kwargs):
    """
    Template an object.
    """
    # TODO: Clarify old vs. new variable naming here.
    from supriya import utils
    new_args, new_var_args, new_kwargs = utils.get_object_vars(expr)
    #print('OLD', new_args, new_var_args, new_kwargs)
    #print('NEW', type(expr), args, kwargs)
    if args:
        new_var_args = args
    for key, value in kwargs.items():
        if key in new_args:
            new_args[key] = value
        else:
            new_kwargs[key] = value
    new_args = list(new_args.values()) + list(new_var_args)
    return type(expr)(*new_args, **new_kwargs)
