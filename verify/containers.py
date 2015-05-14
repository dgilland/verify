"""Assertions related to containers/iterables.
"""

import operator

import pydash

from .base import Assertion, Comparator, Negate
from .numbers import Between


__all__ = (
    'In',
    'NotIn',
    'Contains',
    'NotContains',
    'ContainsOnly',
    'NotContainsOnly',
    'Subset',
    'NotSubset',
    'Superset',
    'NotSuperset',
    'Unique',
    'NotUnique',
    'Length',
)


class In(Comparator):
    """Asserts that `value` is in `comparable`.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not in {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether `value` is contained in `comparable`."""
        try:
            return value in comparable
        except (TypeError, ValueError):
            return False


class NotIn(Negate, In):
    """Asserts that `value` is not in `comparable`.

    .. versionadded:: 0.5.0
    """
    reason = '{0} is in {comparable}'


class Contains(Comparator):
    """Asserts that `value` is an iterable and contains `comparable`.

    .. versionadded:: 0.2.0
    """
    reason = '{0} does not contain {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether `value` contains `comparable`."""
        try:
            return comparable in value
        except (TypeError, ValueError):
            return False


class NotContains(Negate, Contains):
    """Asserts that `value` does not contain `comparable`.

    .. versionadded:: 0.5.0
    """
    reason = '{0} contains {comparable}'


class ContainsOnly(Comparator):
    """Asserts that `value` is an iterable and only contains `comparable`.

    .. versionadded:: 0.2.0
    """
    reason = '{0} does not only contain values in {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether `value` contains only values in `comparable`."""
        try:
            return all(val in comparable for val in value)
        except (TypeError, ValueError):
            return False


class NotContainsOnly(Negate, ContainsOnly):
    """Asserts that `value` does not contain only `comparable`.

    .. versionadded:: 0.5.0
    """
    reason = '{0} contains only {comparable}'


class Subset(Comparator):
    """Asserts that `value` is a subset of `comparable`. Comparison supports
    nested ``dict``, ``list``, and ``tuple`` objects.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not a subset of {comparable}'
    op = pydash.rearg(pydash.is_match, 1, 0)


class NotSubset(Negate, Subset):
    """Asserts that `value` is a not a subset of `comparable`.

    .. versionadded:: 0.5.0
    """
    reason = '{0} is a subset of {comparable}'


class Superset(Comparator):
    """Asserts that `value` is a superset of `comparable`. Comparison supports
    nested ``dict``, ``list``, and ``tuple`` objects.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not a supserset of {comparable}'
    op = staticmethod(pydash.is_match)


class NotSuperset(Negate, Superset):
    """Asserts that `value` is a not a superset of `comparable`.

    .. versionadded:: 0.5.0
    """
    reason = '{0} is a superset of {comparable}'


class Unique(Assertion):
    """Asserts that `value` contains only unique values. If `value` is a
    ``dict``, then its ``values()`` will be compared.

    .. versionadded:: 0.3.0
    """
    reason = '{0} contains duplicate items'

    @staticmethod
    def op(value):
        if isinstance(value, dict):
            value = value.values()

        is_unique = True
        seen = []

        for item in value:
            if item in seen:
                is_unique = False
                break
            seen.append(item)

        return is_unique


class NotUnique(Negate, Unique):
    """Asserts that `value` is a not a unique.

    .. versionadded:: 0.5.0
    """
    reason = '{0} is unique'


class Length(Between):
    """Asserts that `value` is an iterable with length between `min` and `max`
    inclusively.

    Examples:

        These will pass:

        >>> assert Length([1, 2, 3], 3)  # 3 <= len(a) <= 3
        >>> assert Length([1, 2, 3, 4, 5], (5, 6))  # 5 <= len(a) <= 6
        >>> assert Length([1, 2, 3], (None, 6))  # len(a) <= 6
        >>> assert Length([1, 2, 3, 4], (4, None))  # len(a) >= 4
        >>> assert Length([1, 2, 3], min=2, max=4)  # 2 <= len(a) <= 4

        This will fail:

        >>> Length([1, 2, 4], 2)  # len(a) <= 2
        Traceback (most recent call last):
        ...
        AssertionError...

    Args:
        value (mixed, optional): Value to compare.
        comparable (tuple): The ``(min, max)`` values for length comparison.
            Pass ``None`` for either position to skip that comparison.

    Keyword Args:
        min (int, optional): Minimum value that `value` must be greater than or
            equal to.
        max (int, optional): Maximum value that `value` must be less than or
            equal to.

    Warning:
        Specify the min/max using either a positional ``tuple`` or keyword
        arguments, but don't mix the two styles. Passing `comparable` by
        position has precedence.

    .. versionadded:: 0.2.0

    .. versionchanged:: 0.4.0

        - Change comparison to function like :class:`Between` meaning length is
          compared to min and max values.
        - Allow keyword arguments ``min`` and ``max`` to be used in place of
          positional tuple
    """
    reason = '{0} does not have length between {min} and {max}'

    @staticmethod
    def op(value, min=None, max=None):
        try:
            return Between.op(len(value), min=min, max=max)
        except (TypeError, ValueError):
            return False
