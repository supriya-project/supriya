def repr(expr):
    from supriya import utils
    new_args, new_var_args, new_kwargs = utils.get_signature_data(expr)
    parts = []
    has_new_lines = False
    for key, value in new_args.items():
        arg_repr = repr(value)
        if '\n' in arg_repr:
            has_new_lines = True
        if not new_var_args:
            arg_repr = '{}={}'.format(key, arg_repr)
        parts.append(arg_repr)
    for arg in new_var_args:
        arg_repr = repr(arg)
        if '\n' in arg_repr:
            has_new_lines = True
        parts.append(arg_repr)
    for key, value in new_kwargs.items():
        arg_repr = '{}={!r}'.format(key, value)
        has_new_lines = True
        parts.append(arg_repr)
    if has_new_lines:
        for i, part in enumerate(parts):
            parts[i] = '\n'.join('    ' + line for line in part.split('\n'))
        parts.append('    )')
        parts = ',\n'.join(parts)
        return '{}(\n{}'.format(type(expr).__name__, parts)
    parts = ', '.join(parts)
    return '{}({})'.format(type(expr).__name__, parts)
