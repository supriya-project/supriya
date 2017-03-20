# -*- encoding: utf -*-


def render(
    expr,
    output_file_path=None,
    render_directory_path=None,
    **kwargs
    ):
    if not hasattr(expr, '__render__'):
        raise ValueError(expr)
    return expr.__render__(
        output_file_path=output_file_path,
        render_directory_path=render_directory_path,
        **kwargs
        )
