# -*- encoding: utf-8 -*-
import enum
from abjad.tools import systemtools


class Enumeration(enum.IntEnum):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats enumeration.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __repr__(self):
        r'''Gets interpreter representation of enumeration.

        Returns string.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        storage_format_pieces = (str(self),)
        return systemtools.StorageFormatSpecification(
            self,
            storage_format_pieces=storage_format_pieces,
            )

    @property
    def _storage_format_specification(self):
        manager = systemtools.StorageFormatManager
        storage_format_pieces = '{}.{}'.format(
            manager.get_tools_package_name(self),
            str(self),
            )
        storage_format_pieces = (storage_format_pieces,)
        return systemtools.StorageFormatSpecification(
            self,
            storage_format_pieces=storage_format_pieces,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_expr(cls, expr):
        if isinstance(expr, cls):
            return expr
        elif isinstance(expr, int):
            return cls(expr)
        elif isinstance(expr, str):
            expr = expr.upper()
            expr = expr.strip()
            expr = expr.replace(' ', '_')
            return cls[expr]
        elif expr is None:
            return cls(0)
        message = 'Cannot instantiate {} from {}.'.format(cls.__name__, expr)
        raise ValueError(message)