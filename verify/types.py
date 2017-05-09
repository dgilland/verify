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

    Aliases:
        - ``to_be_type``
        - ``is_type``

    .. versionadded:: 0.0.1

    .. versionchanged:: 0.6.0
        Renamed from ``InstanceOf`` to ``Type``
    """
    #:
    reason = '{0} is not an instance of {comparable}'
    op = isinstance


to_be_type = Type
is_type = Type


class NotType(Negate, Type):
    """Asserts that `value` is a not an instance of `comparable`.

    Aliases:
        - ``to_be_not_type``
        - ``is_not_type``

    .. versionadded:: 0.5.0

    .. versionchanged:: 0.6.0
        Renamed from ``NotInstanceOf`` to ``NotType``
    """
    #:
    reason = '{0} is an instance of {comparable}'


to_not_be_type = NotType
is_not_type = NotType


class Boolean(Assertion):
    """Asserts that `value` is a boolean.

    Aliases:
        - ``to_be_boolean``
        - ``is_boolean``

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a boolean'
    op = staticmethod(pydash.is_boolean)


to_be_boolean = Boolean
is_boolean = Boolean


class NotBoolean(Negate, Boolean):
    """Asserts that `value` is a not a boolean.

    Aliases:
        - ``to_be_not_boolean``
        - ``is_not_boolean``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a boolean'


to_not_be_boolean = NotBoolean
is_not_boolean = NotBoolean


class String(Assertion):
    """Asserts that `value` is a string (``str`` or ``unicode`` on Python 2).

    Aliases:
        - ``to_be_string``
        - ``is_string``

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a string'
    op = staticmethod(pydash.is_string)


to_be_string = String
is_string = String


class NotString(Negate, String):
    """Asserts that `value` is a not a string.

    Aliases:
        - ``to_be_not_string``
        - ``is_not_string``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a string'


to_not_be_string = NotString
is_not_string = NotString


class Dict(Assertion):
    """Asserts that `value` is a dictionary.

    Aliases:
        - ``to_be_dict``
        - ``is_dict``

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a dictionary'
    op = staticmethod(pydash.is_dict)


to_be_dict = Dict
is_dict = Dict


class NotDict(Negate, Dict):
    """Asserts that `value` is a not a dict.

    Aliases:
        - ``to_be_not_dict``
        - ``is_dict``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a dict'


to_not_be_dict = NotDict
is_not_dict = NotDict


class List(Assertion):
    """Asserts that `value` is a list.

    Aliases:
        - ``to_be_list``
        - ``is_list``

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a list'
    op = staticmethod(pydash.is_list)


to_be_list = List
is_list = List


class NotList(Negate, List):
    """Asserts that `value` is a not a list.

    Aliases:
        - ``to_be_not_list``
        - ``is_not_list``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a list'


to_not_be_list = NotList
is_not_list = NotList


class Tuple(Assertion):
    """Asserts that `value` is a tuple.

    Aliases:
        - ``to_be_tuple``
        - ``is_tuple``

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a tuple'
    op = staticmethod(pydash.is_tuple)


to_be_tuple = Tuple
is_tuple = Tuple


class NotTuple(Negate, Tuple):
    """Asserts that `value` is a not a tuple.

    Aliases:
        - ``to_be_not_tuple``
        - ``is_not_tuple``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a tuple'


to_not_be_tuple = NotTuple
is_not_tuple = NotTuple


class Date(Assertion):
    """Asserts that `value` is an instance of ``datetime.date`` or
    ``datetime.datetime``.

    Aliases:
        - ``to_be_date``
        - ``is_date``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not a date or datetime object'
    op = staticmethod(pydash.is_date)


to_be_date = Date
is_date = Date


class NotDate(Negate, Date):
    """Asserts that `value` is a not a date or datetime object.

    Aliases:
        - ``to_be_not_date``
        - ``is_not_date``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a date or datetime object'


to_not_be_date = NotDate
is_not_date = NotDate


class DateString(Comparator):
    """Asserts that `value` is matches the datetime format string `comparable`.

    Aliases:
        - ``to_be_date_string``
        - ``is_date_string``

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


to_be_date_string = DateString
is_date_string = DateString


class NotDateString(Negate, DateString):
    """Asserts that `value` does not match datetime format string `comparable`.

    Aliases:
        - ``to_be_not_date_string``
        - ``is_not_date_string``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} matches the datetime format {comparable}'


to_not_be_date_string = NotDateString
is_not_date_string = NotDateString


class Int(Assertion):
    """Asserts that `value` is an integer.

    Aliases:
        - ``to_be_int``
        - ``is_int``

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not an integer'
    op = staticmethod(pydash.is_integer)


to_be_int = Int
is_int = Int


class NotInt(Negate, Int):
    """Asserts that `value` is a not an integer.

    Aliases:
        - ``to_be_not_int``
        - ``is_not_int``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is an integer'


to_not_be_int = NotInt
is_not_int = NotInt


class Float(Assertion):
    """Asserts that `value` is a float.

    Aliases:
        - ``to_be_float``
        - ``is_float``

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a float'
    op = staticmethod(pydash.is_float)


to_be_float = Float
is_float = Float


class NotFloat(Negate, Float):
    """Asserts that `value` is a not a float.

    Aliases:
        - ``to_be_not_float``
        - ``is_not_float``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a float'


to_not_be_float = NotFloat
is_not_float = NotFloat


class Number(Assertion):
    """Asserts that `value` is a number.

    Objects considered a number are:

    - ``int``
    - ``float``
    - ``decimal.Decimal``
    - ``long (Python 2)``

    Aliases:
        - ``to_be_number``
        - ``is_number``

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not a number'
    op = staticmethod(pydash.is_number)


to_be_number = Number
is_number = Number


class NotNumber(Negate, Number):
    """Asserts that `value` is a not a number.

    Aliases:
        - ``to_be_not_number``
        - ``is_not_number``

    .. versionadded:: 0.1.0

    .. versionchanged:: 0.5.0
        Renamed from ``NaN`` to ``NotNumber``.
    """
    #:
    reason = '{0} is a number'


to_not_be_number = NotNumber
is_not_number = NotNumber
