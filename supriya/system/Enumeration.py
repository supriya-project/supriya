import enum
import uqbar.strings


class Enumeration(enum.IntEnum):
    r'''Enumeration.

    ..  container:: example

        ::

            >>> class Colors(supriya.Enumeration):
            ...     RED = 1
            ...     BLUE = 2
            ...     LIGHT_GREEN = 3
            ...

        ::

            >>> color = Colors.RED
            >>> print(repr(color))
            Colors.RED

        ::

            >>> Colors.from_expr('light green')
            Colors.LIGHT_GREEN

    '''

    ### SPECIAL METHODS ###

    def __dir__(self):
        names = [
            '__class__',
            '__doc__',
            '__format__',
            '__members__',
            '__module__',
            '__repr__',
            '_get_format_specification',
            'from_expr',
            ]
        names += self._member_names_
        names += [
            ]
        return sorted(names)

    def __repr__(self):
        return '{}.{}'.format(
            type(self).__name__,
            self.name,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_expr(cls, expr):
        r'''Convenience constructor for enumerations.

        Returns new enumeration item.
        '''
        if isinstance(expr, cls):
            return expr
        elif isinstance(expr, int):
            return cls(expr)
        elif isinstance(expr, str):
            expr = expr.strip()
            expr = uqbar.strings.to_snake_case(expr)
            expr = expr.upper()
            try:
                return cls[expr]
            except KeyError:
                return cls[expr.replace('_', '')]
        elif expr is None:
            return cls(0)
        message = 'Cannot instantiate {} from {}.'.format(
            cls.__name__,
            expr,
            )
        raise ValueError(message)
