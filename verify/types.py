"""Assertions related to types.
"""

import datetime

import pydash

from .base import Assertion, Comparator, Negate


__all__ = (
    'Type',
    'NotType',
    'Boolean',
    'NotBoolean',
    'String',
    'NotString',
    'Dict',
    'NotDict',
    'List',
    'NotList',
    'Tuple',
    'NotTuple',
    'Date',
    'NotDate',
    'DateString',
    'NotDateString',
    'Int',
    'NotInt',
    'NotFloat',
    'Float',
    'Number',
    'NotNumber',
)


class Type(Comparator):
    """Asserts that `value` is an instance of `comparable`.

    .. versionadded:: 0.0.1

    .. versionchanged:: 0.6.0
        Renamed from ``InstanceOf`` to ``Type``
    """
    #:
    reason = '{0} is not an instance of {comparable}'
    op = isinstance


class NotType(Negate, Type):
    """Asserts that `value` is a not an instance of `comparable`.

    .. versionadded:: 0.5.0

    .. versionchanged:: 0.6.0
        Renamed from ``NotInstanceOf`` to ``NotType``
    """
    #:
    reason = '{0} is an instance of {comparable}'


class Boolean(Assertion):
    """Asserts that `value` is a boolean.

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a boolean'
    op = staticmethod(pydash.is_boolean)


class NotBoolean(Negate, Boolean):
    """Asserts that `value` is a not a boolean.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a boolean'


class String(Assertion):
    """Asserts that `value` is a string (``str`` or ``unicode`` on Python 2).

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a string'
    op = staticmethod(pydash.is_string)


class NotString(Negate, String):
    """Asserts that `value` is a not a string.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a string'


class Dict(Assertion):
    """Asserts that `value` is a dictionary.

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a dictionary'
    op = staticmethod(pydash.is_dict)


class NotDict(Negate, Dict):
    """Asserts that `value` is a not a dict.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a dict'


class List(Assertion):
    """Asserts that `value` is a list.

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a list'
    op = staticmethod(pydash.is_list)


class NotList(Negate, List):
    """Asserts that `value` is a not a list.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a list'


class Tuple(Assertion):
    """Asserts that `value` is a tuple.

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a tuple'
    op = staticmethod(pydash.is_tuple)


class NotTuple(Negate, Tuple):
    """Asserts that `value` is a not a tuple.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a tuple'


class Date(Assertion):
    """Asserts that `value` is an instance of ``datetime.date`` or
    ``datetime.datetime``.

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not a date or datetime object'
    op = staticmethod(pydash.is_date)


class NotDate(Negate, Date):
    """Asserts that `value` is a not a date or datetime object.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a date or datetime object'


class DateString(Comparator):
    """Asserts that `value` is matches the datetime format string `comparable`.

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} does not match the datetime format {comparable}'

    @staticmethod
    def op(value, comparable):
        try:
            datetime.datetime.strptime(value, comparable)
            return True
        except (TypeError, ValueError):
            return False


class NotDateString(Negate, DateString):
    """Asserts that `value` does not match datetime format string `comparable`.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} matches the datetime format {comparable}'


class Int(Assertion):
    """Asserts that `value` is an integer.

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not an integer'
    op = staticmethod(pydash.is_int)


class NotInt(Negate, Int):
    """Asserts that `value` is a not an integer.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is an integer'


class Float(Assertion):
    """Asserts that `value` is a float.

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a float'
    op = staticmethod(pydash.is_float)


class NotFloat(Negate, Float):
    """Asserts that `value` is a not a float.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a float'


class Number(Assertion):
    """Asserts that `value` is a number.

    Objects considered a number are:

    - ``int``
    - ``float``
    - ``decimal.Decimal``
    - ``long (Python 2)``

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a number'
    op = staticmethod(pydash.is_number)


class NotNumber(Negate, Number):
    """Asserts that `value` is a not a number.

    .. versionadded:: 0.1.0

    .. versionchanged:: 0.5.0
        Renamed from ``NaN`` to ``NotNumber``.
    """
    #:
    reason = '{0} is a number'
