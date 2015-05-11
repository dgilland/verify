# -*- coding: utf-8 -*-
"""The verify module.
"""

import datetime
import operator
from functools import partial
import re

import pydash

from .__meta__ import (
    __title__,
    __summary__,
    __url__,
    __version__,
    __author__,
    __email__,
    __license__
)


__all__ = (
    'expect',
    'Not',
    'Predicate',
    'Equal',
    'Match',
    'Greater',
    'GreaterEqual',
    'Less',
    'LessEqual',
    'Between',
    'Length',
    'All',
    'Any',
    'In',
    'Contains',
    'ContainsOnly',
    'Subset',
    'Superset',
    'Unique',
    'InstanceOf',
    'Is',
    'IsTrue',
    'IsFalse',
    'IsNone',
    'Truthy',
    'Falsy',
    'Boolean',
    'String',
    'Dict',
    'List',
    'Tuple',
    'Date',
    'DateString',
    'Int',
    'Float',
    'NaN',
    'Number',
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


class _NotSet(object):
    """Represents an unset value."""
    def __repr__(self):  # pragma: no cover
        return 'NotSet'


NotSet = _NotSet()


def expect(value, *assertions):
    """Pass `value` through a set of assertable functions.

    Examples:

        This will pass:

        >>> expect(5, Truthy, Greater(4))
        True

        This will fail:

        >>> expect(5, Falsy)
        Traceback (most recent call last):
        ...
        AssertionError...


    Args:
        value (mixed): Value to test.
        *assertions (callable, optional): Callable objects that accept `value`
            as its first argument. It's expected that these callables assert
            something.

    Returns:
        bool: ``True`` if comparisons pass, otherwise, an ``AssertionError`` is
            raised.

    Raises:
        AssertionError: If the evaluation of all assertions returns ``False``.

    .. versionadded:: 0.0.1

    .. versionchanged:: 0.1.0

        - Rename from ``Expect`` to ``expect`` and change implementation from a
          class to a function.
        - Passed in `value` is no longer called if it's a callable.
        - Return ``True`` if all assertions pass.
    """
    results = all(assertable(value) for assertable in assertions)
    assert results, 'Not all expectations evaluated to true'
    return True


class Assertion(object):
    """Base class for assertions."""
    reason = ''
    op = None

    def __init__(self, value=NotSet):
        if value is not NotSet:
            self(value)

    def message(self, *args, **kargs):
        kargs.update(self.__dict__)
        return self.reason.format(*args, **kargs)

    def compare(self, value):  # pragma: no cover
        # pylint: disable=not-callable
        return self.op(value)

    def __repr__(self):  # pragma: no cover
        return '<{0}>'.format(self)

    def __str__(self):  # pragma: no cover
        return '{0}()'.format(self.__class__.__name__)

    def __call__(self, *args, **kargs):
        """Our main entry point for executing validation. Return ``True`` so
        that we can be used in ``all()``.

        Returns:
            bool: ``True`` if comparison passes, otherwise, an
                ``AssertionError`` is raised.

        Raises:
            AssertionError: If comparison returns ``False``.
        """
        assert self.compare(*args, **kargs), self.message(*args, **kargs)
        return True


class Comparator(Assertion):
    """Base class for assertions that compare two values."""
    def __init__(self, comparable, value=NotSet):
        if value is not NotSet:
            # Swap variables since the prescence of both inputs indicates we
            # are immediately executing validation.
            value, comparable = comparable, value

        # Whether we are validation now or later, set comparable on class since
        # self.compare() expects comparable to be an instance variable.
        self.comparable = comparable

        if value is not NotSet:
            # Immediately execute validation.
            self(value)

    def compare(self, value):
        # pylint: disable=not-callable
        return self.op(value, self.comparable)


class Not(Comparator):
    """Asserts that `comparable` doesn't raise an ``AssertionError``. Can be
    used to create "opposite" comparators.

    Examples:

        >>> expect(5, Not(In([1, 2, 3])))
        True
        >>> Not(5, In([1, 2, 3]))
        <Not()>
        >>> Not(In([1, 2, 3]))(5)
        True

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = ('The negation of {comparable} should not be true '
              'when evaluated with {0}')

    def compare(self, *args, **kargs):
        try:
            return not self.comparable(*args, **kargs)
        except AssertionError:
            return True


class Predicate(Comparator):
    """Asserts that `value` evaluated by the predicate `comparable` is
    ``True``.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = 'The evaluation of {0} using {comparable} is false'

    def compare(self, *args, **kargs):
        return self.comparable(*args, **kargs)


class Equal(Comparator):
    """Asserts that two values are equal.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not equal to {comparable}'
    op = operator.eq


class Match(Comparator):
    """Asserts that `value` matches the regular expression `comparable`.

    Args:
        value (mixed, optional): Value to compare.
        comparable (str|RegExp): String or RegExp object used for matching.

    Keyword Args:
        flags (int, optional): Used when compiling regular expression when
            regular expression is a string. Defaults to ``0``.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} does not match the regular expression {comparable}'

    def __init__(self, comparable, value=NotSet, **options):
        self.flags = options.get('flags', 0)
        super(Match, self).__init__(comparable, value)

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


class Greater(Comparator):
    """Asserts that `value` is greater than `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not greater than {comparable}'
    op = operator.gt


class GreaterEqual(Comparator):
    """Asserts that `value` is greater than or equal to `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not greater than or equal to {comparable}'
    op = operator.ge


class Less(Comparator):
    """Asserts that `value` is less than `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not less than {comparable}'
    op = operator.lt


class LessEqual(Comparator):
    """Asserts that `value` is less than or equal to `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

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

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

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

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

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


class Is(Comparator):
    """Asserts that `value` is `comparable`.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not {comparable}'
    op = operator.is_


class IsTrue(Assertion):
    """Asserts that `value` is ``True``.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not True'
    op = partial(operator.is_, True)


class IsFalse(Assertion):
    """Asserts that `value` is ``False``.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not False'
    op = partial(operator.is_, False)


class IsNone(Assertion):
    """Asserts that `value` is ``None``.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not None'
    op = staticmethod(pydash.is_none)


class All(Comparator):
    """Asserts that `value` evaluates as truthy for **all** predicates in
    `comparable`.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.2.0
    """
    reason = '{0} is not true for all {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether all results from evaluating `value` in `comparable`
        predicates return truthy.
        """
        return all(pydash.juxtapose(*comparable)(value))


class Any(Comparator):
    """Asserts that `value` evaluates as truthy for **any** predicates in
    `comparable`.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.2.0
    """
    reason = '{0} is not true for any {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether any results from evaluating `value` in `comparable`
        predicates return truthy.
        """
        return any(pydash.juxtapose(*comparable)(value))


class In(Comparator):
    """Asserts that `value` is in `comparable`.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

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


class Contains(Comparator):
    """Asserts that `value` is an iterable and contains `comparable`.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

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


class ContainsOnly(Comparator):
    """Asserts that `value` is an iterable and only contains `comparable`.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

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


class Subset(Comparator):
    """Asserts that `value` is a subset of `comparable`. Comparison supports
    nested ``dict``, ``list``, and ``tuple`` objects.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not a subset of {comparable}'
    op = pydash.rearg(pydash.is_match, 1, 0)


class Superset(Comparator):
    """Asserts that `value` is a superset of `comparable`. Comparison supports
    nested ``dict``, ``list``, and ``tuple`` objects.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not a supserset of {comparable}'
    op = staticmethod(pydash.is_match)


class Unique(Assertion):
    """Asserts that `value` contains only unique values. If `value` is a
    ``dict``, then its ``values()`` will be compared.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

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


class InstanceOf(Comparator):
    """Asserts that `value` is an instance of `comparable`.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not an instance of {comparable}'
    op = isinstance


class Truthy(Assertion):
    """Asserts that `value` is truthy.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not truthy'
    op = bool


class Falsy(Assertion):
    """Asserts that `value` is falsy.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not falsy'
    op = pydash.negate(bool)


class Boolean(Assertion):
    """Asserts that `value` is a boolean.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a boolean'
    op = staticmethod(pydash.is_boolean)


class String(Assertion):
    """Asserts that `value` is a string (``str`` or ``unicode`` on Python 2).

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a string'
    op = staticmethod(pydash.is_string)


class Dict(Assertion):
    """Asserts that `value` is a dictionary.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a dictionary'
    op = staticmethod(pydash.is_dict)


class List(Assertion):
    """Asserts that `value` is a list.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a list'
    op = staticmethod(pydash.is_list)


class Tuple(Assertion):
    """Asserts that `value` is a tuple.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a tuple'
    op = staticmethod(pydash.is_tuple)


class Date(Assertion):
    """Asserts that `value` is an instance of ``datetime.date`` or
    ``datetime.datetime``.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not a date or datetime object'
    op = staticmethod(pydash.is_date)


class DateString(Comparator):
    """Asserts that `value` is matches the datetime format string `comparable`.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} does not match the datetime format {comparable}'

    @staticmethod
    def op(value, comparable):
        try:
            datetime.datetime.strptime(value, comparable)
            return True
        except (TypeError, ValueError):
            return False


class Int(Assertion):
    """Asserts that `value` is an integer.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not an int'
    op = staticmethod(pydash.is_int)


class Float(Assertion):
    """Asserts that `value` is a float.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a float'
    op = staticmethod(pydash.is_float)


class Number(Assertion):
    """Asserts that `value` is a number.

    Objects considered a number are:

    - ``int``
    - ``float``
    - ``decimal.Decimal``
    - ``long (Python 2)``

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a number'
    op = staticmethod(pydash.is_number)


class NaN(Assertion):
    """Asserts that `value` is a not a number.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is a number'
    op = staticmethod(pydash.is_nan)


class Positive(Assertion):
    """Asserts that `value` is a positive number.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not a positive number'
    op = staticmethod(pydash.is_positive)


class Negative(Assertion):
    """Asserts that `value` is a negative number.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not a negative number'
    op = staticmethod(pydash.is_negative)


class Even(Assertion):
    """Asserts that `value` is an even number.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not an even number'
    op = staticmethod(pydash.is_even)


class Odd(Assertion):
    """Asserts that `value` is an odd number.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not an odd number'
    op = staticmethod(pydash.is_odd)


class Monotone(Comparator):
    """Asserts that `value` is a monotonic with respect to `comparable`.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not monotonic as evaluated by {comparable}'
    op = staticmethod(pydash.is_monotone)


class Increasing(Assertion):
    """Asserts that `value` is monotonically increasing.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not monotonically increasing'
    op = staticmethod(pydash.is_increasing)


class StrictlyIncreasing(Assertion):
    """Asserts that `value` is strictly increasing.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not strictly increasing'
    op = staticmethod(pydash.is_strictly_increasing)


class Decreasing(Assertion):
    """Asserts that `value` is monotonically decreasing.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not monotonically decreasing'
    op = staticmethod(pydash.is_decreasing)


class StrictlyDecreasing(Assertion):
    """Asserts that `value` is strictly decreasing.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.3.0
    """
    reason = '{0} is not strictly decreasing'
    op = staticmethod(pydash.is_strictly_decreasing)
