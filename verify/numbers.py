"""Assertions related to numbers.
"""

import operator

import pydash

from .base import Assertion, Comparator, Negate, NotSet


__all__ = (
    'Greater',
    'GreaterEqual',
    'Less',
    'LessEqual',
    'Between',
    'NotBetween',
    'Positive',
    'Negative',
    'Even',
    'Odd',
    'Monotone',
    'Increasing',
    'StrictlyIncreasing',
    'Decreasing',
    'StrictlyDecreasing',
)


class Greater(Comparator):
    """Asserts that `value` is greater than `comparable`.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not greater than {comparable}'
    op = operator.gt


class GreaterEqual(Comparator):
    """Asserts that `value` is greater than or equal to `comparable`.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not greater than or equal to {comparable}'
    op = operator.ge


class Less(Comparator):
    """Asserts that `value` is less than `comparable`.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not less than {comparable}'
    op = operator.lt


class LessEqual(Comparator):
    """Asserts that `value` is less than or equal to `comparable`.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not less than or equal to {comparable}'
    op = operator.le


class Between(Comparator):
    """Asserts that `value` is between `min` and `max` inclusively.

    Examples:

        These will pass:

        >>> assert Between(5, (4, 6))  # 4 <= 5 <= 6
        >>> assert Between(5, (5, 6))  # 5 <= 5 <= 6
        >>> assert Between(5, 6)  # 5 <= 6
        >>> assert Between(5, (None, 6))  # 5 <= 6
        >>> assert Between(5, (4, None))  # 5 >= 4
        >>> assert Between(5, min=4, max=6)  # 4 <= 5 <= 6

        This will fail:

        >>> Between(5, 4)  # 5 <= 4
        Traceback (most recent call last):
        ...
        AssertionError...

    Args:
        value (mixed, optional): Value to compare.
        comparable (tuple): The ``(min, max)`` values for Between comparison.
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
        Allow keyword arguments ``min`` and ``max`` to be used in place of
        positional tuple.
    """
    reason = '{0} is not between {min} and {max}'

    def __init__(self, comparable=NotSet, value=NotSet, **options):
        if (value is not NotSet) or (comparable is not NotSet and options):
            value, comparable = comparable, value

        if comparable is NotSet:
            self.min = options.get('min')
            self.max = options.get('max')
        elif isinstance(comparable, (list, tuple)):
            self.min = pydash.get_path(comparable, 0)
            self.max = pydash.get_path(comparable, 1)
        else:
            self.min = None
            self.max = comparable

        if value is not NotSet:
            self(value)

    def compare(self, value):
        return self.op(value, self.min, self.max)

    @staticmethod
    def op(value, min=None, max=None):
        ge_min = True
        le_max = True

        if min is not None:
            ge_min = value >= min

        if max is not None:
            le_max = value <= max

        return ge_min and le_max


class NotBetween(Negate, Between):
    """Asserts that `value` is not between `min` and `max` inclusively.

    .. versionadded:: 0.5.0
    """
    reason = '{0} is between {min} and {max}'


class Positive(Assertion):
    """Asserts that `value` is a positive number.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not a positive number'
    op = staticmethod(pydash.is_positive)


class Negative(Assertion):
    """Asserts that `value` is a negative number.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not a negative number'
    op = staticmethod(pydash.is_negative)


class Even(Assertion):
    """Asserts that `value` is an even number.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not an even number'
    op = staticmethod(pydash.is_even)


class Odd(Assertion):
    """Asserts that `value` is an odd number.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not an odd number'
    op = staticmethod(pydash.is_odd)


class Monotone(Comparator):
    """Asserts that `value` is a monotonic with respect to `comparable`.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not monotonic as evaluated by {comparable}'
    op = staticmethod(pydash.is_monotone)


class Increasing(Assertion):
    """Asserts that `value` is monotonically increasing.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not monotonically increasing'
    op = staticmethod(pydash.is_increasing)


class StrictlyIncreasing(Assertion):
    """Asserts that `value` is strictly increasing.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not strictly increasing'
    op = staticmethod(pydash.is_strictly_increasing)


class Decreasing(Assertion):
    """Asserts that `value` is monotonically decreasing.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not monotonically decreasing'
    op = staticmethod(pydash.is_decreasing)


class StrictlyDecreasing(Assertion):
    """Asserts that `value` is strictly decreasing.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not strictly decreasing'
    op = staticmethod(pydash.is_strictly_decreasing)
