import collections
import inspect


def dispatch_formatting(expr):
    if isinstance(expr, (list, tuple)):
        return get_sequence_repr(expr)
    return repr(expr)


def get_sequence_repr(expr):
    prototype = (bool, int, float, str, type(None))
    if all(isinstance(x, prototype) for x in expr):
        result = repr(expr)
        if len(result) < 50:
            return result
    if isinstance(expr, list):
        braces = '[', ']'
    else:
        braces = '(', ')'
    result = [braces[0]]
    for x in expr:
        for line in repr(x).splitlines():
            result.append('    ' + line)
        result[-1] += ','
    result.append('    ' + braces[-1])
    return '\n'.join(result)


def get_object_repr(expr, multiline=False):
    from supriya import utils

    signature = utils.get_object_signature(expr)
    defaults = {}
    for name, parameter in signature.parameters.items():
        if parameter.default is not inspect._empty:
            defaults[name] = parameter.default

    new_args, new_var_args, new_kwargs = utils.get_object_vars(expr)
    args_parts = collections.OrderedDict()
    var_args_parts = []
    kwargs_parts = {}
    has_new_lines = multiline
    parts = []

    # Format keyword-optional arguments.
    for key, value in new_args.items():
        arg_repr = dispatch_formatting(value)
        if '\n' in arg_repr:
            has_new_lines = True
        # If we don't have *args, we can use key=value formatting.
        # We can also omit arguments which match the signature's defaults.
        if not new_var_args:
            if key in defaults and value == defaults[key]:
                continue
            arg_repr = '{}={}'.format(key, arg_repr)
        args_parts[key] = arg_repr

    # Format *args
    for arg in new_var_args:
        arg_repr = dispatch_formatting(arg)
        if '\n' in arg_repr:
            has_new_lines = True
        var_args_parts.append(arg_repr)

    # Format **kwargs
    for key, value in sorted(new_kwargs.items()):
        if key in defaults and value == defaults[key]:
            continue
        value = dispatch_formatting(value)
        arg_repr = '{}={}'.format(key, value)
        has_new_lines = True
        kwargs_parts[key] = arg_repr

    # If we have *args, the initial args cannot use key/value formatting.
    if var_args_parts:
        for part in args_parts.values():
            parts.append(part)
        parts.extend(var_args_parts)
        for _, part in sorted(kwargs_parts.items()):
            parts.append(part)

    # Otherwise, we can combine and sort all key/value pairs.
    else:
        args_parts.update(kwargs_parts)
        for _, part in sorted(args_parts.items()):
            parts.append(part)

    # If we should format on multiple lines, add the appropriate formatting.
    if has_new_lines and parts:
        for i, part in enumerate(parts):
            parts[i] = '\n'.join('    ' + line for line in part.split('\n'))
        parts.append('    )')
        parts = ',\n'.join(parts)
        return '{}(\n{}'.format(type(expr).__name__, parts)

    parts = ', '.join(parts)
    return '{}({})'.format(type(expr).__name__, parts)
