def new(expr, *args, **kwargs):
    """
    Template an object.
    """
    from supriya import utils
    new_args, new_var_args, new_kwargs = utils.get_signature_data(expr)
    if args:
        new_var_args = args
    for key, value in kwargs.items():
        if key in new_args:
            new_args[key] = value
        else:
            new_kwargs[key] = value
    new_args = list(new_args.values()) + list(new_var_args)
    return type(expr)(*new_args, **new_kwargs)
