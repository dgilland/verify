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
    'NotLength',
)


class In(Comparator):
    """Asserts that `value` is in `comparable`.

    Aliases:
        - ``to_be_in``
        - ``is_in``

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not in {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether `value` is contained in `comparable`."""
        try:
            return value in comparable
        except (TypeError, ValueError):
            return False


to_be_in = In
is_in = In


class NotIn(Negate, In):
    """Asserts that `value` is not in `comparable`.

    Aliases:
        - ``to_not_be_in``
        - ``is_not_in``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is in {comparable}'


to_not_be_in = NotIn
is_not_in = NotIn


class Contains(Comparator):
    """Asserts that `value` is an iterable and contains `comparable`.

    Aliases:
        - ``to_contain``
        - ``contains``

    .. versionadded:: 0.2.0
    """
    #:
    reason = '{0} does not contain {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether `value` contains `comparable`."""
        try:
            return comparable in value
        except (TypeError, ValueError):
            return False


to_contain = Contains
contains = Contains


class NotContains(Negate, Contains):
    """Asserts that `value` does not contain `comparable`.

    Aliases:
        - ``to_not_contain``
        - ``does_not_contain``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} contains {comparable}'


to_not_contain = NotContains
does_not_contain = NotContains


class ContainsOnly(Comparator):
    """Asserts that `value` is an iterable and only contains `comparable`.

    Aliases:
        - ``to_contain_only``
        - ``contains_only``

    .. versionadded:: 0.2.0
    """
    #:
    reason = '{0} does not only contain values in {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether `value` contains only values in `comparable`."""
        try:
            return all(val in comparable for val in value)
        except (TypeError, ValueError):
            return False


to_contain_only = ContainsOnly
contains_only = ContainsOnly


class NotContainsOnly(Negate, ContainsOnly):
    """Asserts that `value` does not contain only `comparable`.

    Aliases:
        - ``to_not_contain_only``
        - ``does_not_contain_only``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} contains only {comparable}'


to_not_contain_only = NotContainsOnly
does_not_contain_only = NotContainsOnly


class Subset(Comparator):
    """Asserts that `value` is a subset of `comparable`. Comparison supports
    nested ``dict``, ``list``, and ``tuple`` objects.

    Aliases:
        - ``to_be_subset``
        - ``is_subset``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not a subset of {comparable}'
    op = pydash.rearg(pydash.is_match, 1, 0)


to_be_subset = Subset
is_subset = Subset


class NotSubset(Negate, Subset):
    """Asserts that `value` is a not a subset of `comparable`.

    Aliases:
        - ``to_not_be_subset``
        - ``is_not_subset``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a subset of {comparable}'


to_not_be_subset = NotSubset
is_not_subset = NotSubset


class Superset(Comparator):
    """Asserts that `value` is a superset of `comparable`. Comparison supports
    nested ``dict``, ``list``, and ``tuple`` objects.

    Aliases:
        - ``to_be_superset``
        - ``is_superset``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not a supserset of {comparable}'
    op = staticmethod(pydash.is_match)


to_be_superset = Superset
is_superset = Superset


class NotSuperset(Negate, Superset):
    """Asserts that `value` is a not a superset of `comparable`.

    Aliases:
        - ``to_not_be_superset``
        - ``is_not_superset``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is a superset of {comparable}'


to_not_be_superset = NotSuperset
is_not_superset = NotSuperset


class Unique(Assertion):
    """Asserts that `value` contains only unique values. If `value` is a
    ``dict``, then its ``values()`` will be compared.

    Aliases:
        - ``to_be_unique``
        - ``is_unique``

    .. versionadded:: 0.3.0
    """
    #:
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


to_be_unique = Unique
is_unique = Unique


class NotUnique(Negate, Unique):
    """Asserts that `value` is a not a unique.

    Aliases:
        - ``to_not_be_unique``
        - ``is_not_unique``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is unique'


to_not_be_unique = NotUnique
is_not_unique = NotUnique


class Length(Between):
    """Asserts that `value` is an iterable with length between `min` and `max`
    inclusively.

    Examples:

        These will pass:

        >>> assert Length([1, 2, 3], min=3, max=3)  # 3 <= len(a) <= 3
        >>> assert Length([1, 2, 3, 4, 5], min=5, max=6)  # 5 <= len(a) <= 6
        >>> assert Length([1, 2, 3], max=6)  # len(a) <= 6
        >>> assert Length([1, 2, 3, 4], min=4)  # len(a) >= 4

        This will fail:

        >>> Length([1, 2, 4], max=2)  # len(a) <= 2
        Traceback (most recent call last):
        ...
        AssertionError...

    Args:
        value (mixed, optional): Value to compare.

    Keyword Args:
        min (int, optional): Minimum value that `value` must be greater than or
            equal to.
        max (int, optional): Maximum value that `value` must be less than or
            equal to.

    Aliases:
        - ``to_have_length``
        - ``has_length``

    .. versionadded:: 0.2.0

    .. versionchanged:: 0.4.0

        - Change comparison to function like :class:`Between` meaning length is
          compared to min and max values.
        - Allow keyword arguments ``min`` and ``max`` to be used in place of
          positional tuple

    .. versionchanged:: 1.0.0
        Removed positional tuple argument and only support ``min`` and ``max``
        keyword arguments.
    """
    #:
    reason = '{0} does not have length between {min} and {max}'

    @staticmethod
    def op(value, min=None, max=None):
        try:
            return Between.op(len(value), min=min, max=max)
        except (TypeError, ValueError):
            return False


to_have_length = Length
has_length = Length


class NotLength(Negate, Length):
    """Asserts that `value` is an iterable with length not between `min` and
    `max` inclusively.

    Aliases:
        - ``to_not_have_length``
        - ``does_not_have_length``

    .. versionadded:: 1.0.0
    """
    #:
    reason = '{0} has length between {min} and {max}'


to_not_have_length = NotLength
does_not_have_length = NotLength
