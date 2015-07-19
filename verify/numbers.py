"""Assertions related to numbers.
"""

import operator

import pydash

from .base import Assertion, Comparator, Negate, NotSet


__all__ = (
    'Greater',
    'GreaterThan',
    'GreaterEqual',
    'GreaterOrEqual',
    'Less',
    'LessThan',
    'LessEqual',
    'LessOrEqual',
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

    Aliases:
        - ``GreaterThan``
        - ``to_be_greater``
        - ``to_be_greater_than``
        - ``is_greater``
        - ``is_greater_than``

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not greater than {comparable}'
    op = operator.gt


GreaterThan = Greater
to_be_greater = Greater
to_be_greater_than = Greater
is_greater = Greater
is_greater_than = Greater


class GreaterEqual(Comparator):
    """Asserts that `value` is greater than or equal to `comparable`.

    Aliases:
        - ``GreaterThanEqual``
        - ``to_be_greater_equal``
        - ``to_be_greater_or_equal``
        - ``is_greater_equal``
        - ``is_greater_or_equal``

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not greater than or equal to {comparable}'
    op = operator.ge


GreaterOrEqual = GreaterEqual
to_be_greater_equal = GreaterEqual
to_be_greater_or_equal = GreaterEqual
is_greqter_equal = GreaterEqual
is_greater_or_equal = GreaterEqual


class Less(Comparator):
    """Asserts that `value` is less than `comparable`.

    Aliases:
        - ``LessThan``
        - ``to_be_less``
        - ``to_be_less_than``
        - ``is_less``
        - ``is_less_than``

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not less than {comparable}'
    op = operator.lt


LessThan = Less
to_be_less = Less
to_be_less_than = Less
is_less = Less
is_less_than = Less


class LessEqual(Comparator):
    """Asserts that `value` is less than or equal to `comparable`.

    Aliases:
        - ``LessThanEqual``
        - ``to_be_less_equal``
        - ``to_be_less_or_equal``
        - ``is_less_equal``
        - ``is_less_or_equal``

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not less than or equal to {comparable}'
    op = operator.le


LessOrEqual = LessEqual
to_be_less_equal = LessEqual
to_be_less_or_equal = LessEqual
is_less_equal = LessEqual
is_less_or_equal = LessEqual


class Between(Assertion):
    """Asserts that `value` is between `min` and `max` inclusively.

    Examples:

        These will pass:

        >>> assert Between(5, min=4, max=6)  # 4 <= 5 <= 6
        >>> assert Between(5, min=5, max=6)  # 5 <= 5 <= 6
        >>> assert Between(5, max=6)  # 5 <= 6
        >>> assert Between(5, min=4)  # 5 >= 4

        This will fail:

        >>> Between(5, max=4)  # 5 <= 4
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
        - ``to_be_between``
        - ``is_between``

    .. versionadded:: 0.2.0

    .. versionchanged:: 0.4.0
        Allow keyword arguments ``min`` and ``max`` to be used in place of
        positional tuple.

    .. versionchanged:: 1.0.0
        Removed positional tuple argument and only support ``min`` and ``max``
        keyword arguments.
    """
    #:
    reason = '{0} is not between {min} and {max}'

    def set_options(self, opts):
        self.min = opts.pop('min', None)
        self.max = opts.pop('max', None)

    def compare(self, value):
        return self.op(value, self.min, self.max)

    @staticmethod
    def op(value, min=None, max=None):
        ge_min = value >= min if min is not None else True
        le_max = value <= max if max is not None else True
        return ge_min and le_max


to_be_between = Between
is_between = Between


class NotBetween(Negate, Between):
    """Asserts that `value` is not between `min` and `max` inclusively.

    Aliases:
        - ``to_not_be_between``
        - ``is_not_between``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is between {min} and {max}'


to_not_be_between = NotBetween
is_not_between = NotBetween


class Positive(Assertion):
    """Asserts that `value` is a positive number.

    Aliases:
        - ``to_be_positive``
        - ``is_positive``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not a positive number'
    op = staticmethod(pydash.is_positive)


to_be_positive = Positive
is_positive = Positive


class Negative(Assertion):
    """Asserts that `value` is a negative number.

    Aliases:
        - ``to_be_negative``
        - ``is_negative``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not a negative number'
    op = staticmethod(pydash.is_negative)


to_be_negative = Negative
is_negative = Negative


class Even(Assertion):
    """Asserts that `value` is an even number.

    Aliases:
        - ``to_be_even``
        - ``is_even``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not an even number'
    op = staticmethod(pydash.is_even)


to_be_even = Even
is_even = Even


class Odd(Assertion):
    """Asserts that `value` is an odd number.

    Aliases:
        - ``to_be_odd``
        - ``is_odd``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not an odd number'
    op = staticmethod(pydash.is_odd)


to_be_odd = Odd
is_odd = Odd


class Monotone(Comparator):
    """Asserts that `value` is a monotonic with respect to `comparable`.

    Aliases:
        - ``to_be_monotone``
        - ``is_monotone``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not monotonic as evaluated by {comparable}'
    op = staticmethod(pydash.is_monotone)


to_be_monotone = Monotone
is_monotone = Monotone


class Increasing(Assertion):
    """Asserts that `value` is monotonically increasing.

    Aliases:
        - ``to_be_increasing``
        - ``is_increasing``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not monotonically increasing'
    op = staticmethod(pydash.is_increasing)


to_be_increasing = Increasing
is_increasing = Increasing


class StrictlyIncreasing(Assertion):
    """Asserts that `value` is strictly increasing.

    Aliases:
        - ``to_be_strictly_increasing``
        - ``is_strictly_increasing``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not strictly increasing'
    op = staticmethod(pydash.is_strictly_increasing)


to_be_strictly_increasing = StrictlyIncreasing
is_strictly_increasing = StrictlyIncreasing


class Decreasing(Assertion):
    """Asserts that `value` is monotonically decreasing.

    Aliases:
        - ``to_be_decreasing``
        - ``is_decreasing``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not monotonically decreasing'
    op = staticmethod(pydash.is_decreasing)


to_be_decreasing = Decreasing
is_decreasing = Decreasing


class StrictlyDecreasing(Assertion):
    """Asserts that `value` is strictly decreasing.

    Aliases:
        - ``to_be_strictly_decreasing``
        - ``is_strictly_decreasing``

    .. versionadded:: 0.3.0
    """
    #:
    reason = '{0} is not strictly decreasing'
    op = staticmethod(pydash.is_strictly_decreasing)


to_be_strictly_decreasing = StrictlyDecreasing
is_strictly_decreasing = StrictlyDecreasing
