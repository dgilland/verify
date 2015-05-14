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

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not equal to {comparable}'
    op = operator.eq


class NotEqual(Negate, Equal):
    """Asserts that two values are not equal.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is equal to {comparable}'


class Match(Comparator):
    """Asserts that `value` matches the regular expression `comparable`.

    Args:
        value (mixed, optional): Value to compare.
        comparable (str|RegExp): String or RegExp object used for matching.

    Keyword Args:
        flags (int, optional): Used when compiling regular expression when
            regular expression is a string. Defaults to ``0``.

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


class NotMatch(Negate, Match):
    """Asserts that `value` does not match the regular expression `comparable`.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} matches the regular expression {comparable}'


class Is(Comparator):
    """Asserts that `value` is `comparable`.

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not {comparable}'
    op = operator.is_


class IsNot(Negate, Is):
    """Asserts that `value` is not `comparable`.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is {comparable}'


class IsTrue(Assertion):
    """Asserts that `value` is ``True``.

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not True'
    op = partial(operator.is_, True)


class IsNotTrue(Negate, IsTrue):
    """Asserts that `value` is not ``True``.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is True'


class IsFalse(Assertion):
    """Asserts that `value` is ``False``.

    .. versionadded:: 0.1.0
    """
    #:
    reason = '{0} is not False'
    op = partial(operator.is_, False)


class IsNotFalse(Negate, IsFalse):
    """Asserts that `value` is not ``False``.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is False'


class IsNone(Assertion):
    """Asserts that `value` is ``None``.

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not None'
    op = staticmethod(pydash.is_none)


class IsNotNone(Negate, IsNone):
    """Asserts that `value` is not ``None``.

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is None'
