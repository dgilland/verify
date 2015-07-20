"""Assertions related to equality.
"""

import operator
from functools import partial
import re

import pydash

from .base import Assertion, Comparator, Negate, NotSet


__all__ = (
    'Equal',
    'NotEqual',
    'Match',
    'NotMatch',
    'Is',
    'IsNot',
    'IsTrue',
    'IsNotTrue',
    'IsFalse',
    'IsNotFalse',
    'IsNotNone',
    'IsNone',
)


class Equal(Comparator):
    """Asserts that two values are equal.

    Aliases:
        - ``to_be_equal``
        - ``is_equal``

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not equal to {comparable}'
    op = operator.eq


to_be_equal = Equal
is_equal = Equal


class NotEqual(Negate, Equal):
    """Asserts that two values are not equal.

    Aliases:
        - ``to_not_be_equal``
        - ``is_not_equal``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is equal to {comparable}'


to_not_be_equal = NotEqual
is_not_equal = NotEqual


class Match(Comparator):
    """Asserts that `value` matches the regular expression `comparable`.

    Args:
        value (mixed, optional): Value to compare.
        comparable (str|RegExp): String or RegExp object used for matching.

    Keyword Args:
        flags (int, optional): Used when compiling regular expression when
            regular expression is a string. Defaults to ``0``.

    Aliases:
        - ``to_match``
        - ``is_match``
        - ``matches``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} does not match the regular expression {comparable}'

    def set_options(self, opts):
        self.flags = opts.pop('flags', 0)

    def compare(self, value):
        return self.op(value, self.comparable, flags=self.flags)

    @staticmethod
    def op(value, comparable, flags=0):
        if pydash.is_string(comparable):
            pattern = re.compile(comparable, flags)
        else:
            pattern = comparable

        try:
            match = bool(pattern.match(value))
        except (TypeError, ValueError):
            match = False

        return match


to_match = Match
is_match = Match
matches = Match


class NotMatch(Negate, Match):
    """Asserts that `value` does not match the regular expression `comparable`.

    Aliases:
        - ``to_not_be_match``
        - ``is_not_match``
        - ``not_matches``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} matches the regular expression {comparable}'


to_not_match = NotMatch
is_not_match = Match
does_not_match = NotMatch


class Is(Comparator):
    """Asserts that `value` is `comparable`.

    Aliases:
        - ``to_be``
        - ``is_``

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not {comparable}'
    op = operator.is_


to_be = Is
is_ = Is


class IsNot(Negate, Is):
    """Asserts that `value` is not `comparable`.

    Aliases:
        - ``to_not_be``
        - ``is_not``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is {comparable}'


to_not_be = IsNot
is_not = IsNot


class IsTrue(Assertion):
    """Asserts that `value` is ``True``.

    Aliases:
        - ``to_be_true``
        - ``is_true``

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not True'
    op = partial(operator.is_, True)


to_be_true = IsTrue
is_true = IsTrue


class IsNotTrue(Negate, IsTrue):
    """Asserts that `value` is not ``True``.

    Aliases:
        - ``to_not_be_true``
        - ``is_not_true``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is True'


to_not_be_true = IsNotTrue
is_not_true = IsNotTrue


class IsFalse(Assertion):
    """Asserts that `value` is ``False``.

    Aliases:
        - ``to_be_false``
        - ``is_false``

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not False'
    op = partial(operator.is_, False)


to_be_false = IsFalse
is_false = IsFalse


class IsNotFalse(Negate, IsFalse):
    """Asserts that `value` is not ``False``.

    Aliases:
        - ``to_not_be_false``
        - ``is_not_false``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is False'


to_not_be_false = IsNotFalse
is_not_false = IsNotFalse


class IsNone(Assertion):
    """Asserts that `value` is ``None``.

    Aliases:
        - ``to_be_none``
        - ``is_none``

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not None'
    op = staticmethod(pydash.is_none)


to_be_none = IsNone
is_none = IsNone


class IsNotNone(Negate, IsNone):
    """Asserts that `value` is not ``None``.

    Aliases:
        - ``to_be_not_none``
        - ``is_not_none``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is None'


to_not_be_none = IsNotNone
is_not_none = IsNotNone
