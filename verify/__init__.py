# -*- coding: utf-8 -*-
"""The verify module.
"""

import operator
from functools import partial

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
    'Int',
    'Float',
    'NaN',
    'Number',
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
        bool: Whether all assertions pass.

    Raises:
        AssertionError: If the evaluation of all assertions returns ``False``.
        Exception: Whatever exception is raised in `assertions`. Generally,
            this should be an ``AssertionError``.

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
        return self.__class__.__name__

    def __call__(self, *args, **kargs):
        """Our main entry point for executing validation. Return ``True`` so
        that we can be used in ``all()``.

        Returns:
            True: If comparison succeeds without an ``AssertionError``

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
    """Asserts that `comparable` doesn't raise an ``AssertionError``.

    .. versionadded:: 0.0.1
    """
    reason = ('The negation of {0} should not be true '
              'when evaluated by {comparable}')

    def compare(self, *args, **kargs):
        try:
            return not self.comparable(*args, **kargs)
        except AssertionError:
            return True


class Predicate(Comparator):
    """Asserts that `value` evaluated by the predicate `comparable` is
    ``True``.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = 'The evaluation of {0} using {comparable} is false'

    def compare(self, *args, **kargs):
        return self.comparable(*args, **kargs)


class Equal(Comparator):
    """Asserts that two values are equal.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not equal to {comparable}'
    op = operator.eq


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
    """Asserts that `value` is between `comparable[0]` and `comparable[1]`
    inclusively.

    Examples:

        These will pass:

        >>> assert Between(5, (4, 5))  # 4 <= 5 <= 5
        >>> assert Between(5, (5, 5))  # 5 <= 5 <= 5
        >>> assert Between(5, 5)  # 5 <= 5
        >>> assert Between(5, (None, 6))  # 5 <= 6
        >>> assert Between(5, (4, None))  # 5 >= 4

        This will fail:

        >>> Between(5, 4)  # 5 <= 4
        Traceback (most recent call last):
        ...
        AssertionError...

    Args:
        comparable (tuple): The (min, max) values for Between comparison. Pass
            ``None`` for min or max to skip that comparison.
        value (mixed, optional): Value to compare.

    Returns:
        bool: ``True`` if comparison passes, otherwise, an ``AssertionError``
            is raised.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.2.0
    """
    reason = '{0} is not between {comparable[0]} and {comparable[1]}'

    def __init__(self, comparable, value=NotSet):
        if value is not NotSet:
            value, comparable = comparable, value

        if not isinstance(comparable, (tuple, list)) or len(comparable) == 1:
            # If comparable is a single value, then assume it's the maximum.
            comparable = (None, comparable)

        self.comparable = comparable

        if value is not NotSet:
            self(value)

    def op(self, value, comparable):
        ge_min = True
        le_max = True

        if comparable[0] is not None:
            ge_min = value >= comparable[0]

        if comparable[1] is not None:
            le_max = value <= comparable[1]

        return ge_min and le_max


class Length(Comparator):
    """Asserts that `value` is an iterable with length equal to `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.2.0
    """
    reason = '{0} does not have length {comparable}'

    def op(self, value, comparable):
        try:
            return len(value) == comparable
        except TypeError:
            return False


class Is(Comparator):
    """Asserts that `value` is `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not {comparable}'
    op = operator.is_


class IsTrue(Assertion):
    """Asserts that `value` is ``True``.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not True'
    op = partial(operator.is_, True)


class IsFalse(Assertion):
    """Asserts that `value` is ``False``.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not False'
    op = partial(operator.is_, False)


class IsNone(Assertion):
    """Asserts that `value` is ``None``.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not None'
    op = partial(pydash.is_none)


class All(Comparator):
    """Asserts that `value` evaluates as truthy for **all** predicates in
    `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.2.0
    """
    reason = '{0} is not true for all {comparable}'

    def op(self, value, comparable):
        """Return whether all results from evaluating `value` in `comparable`
        predicates return truthy.
        """
        return all(pydash.juxtapose(*comparable)(value))


class Any(Comparator):
    """Asserts that `value` evaluates as truthy for **any** predicates in
    `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.2.0
    """
    reason = '{0} is not true for any {comparable}'

    def op(self, value, comparable):
        """Return whether any results from evaluating `value` in `comparable`
        predicates return truthy.
        """
        return any(pydash.juxtapose(*comparable)(value))


class In(Comparator):
    """Asserts that `value` is in `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not in {comparable}'

    def op(self, value, comparable):
        """Return whether `value` is contained in `comparable`."""
        try:
            return value in comparable
        except TypeError:
            return False


class Contains(Comparator):
    """Asserts that `value` is an iterable and contains `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.2.0
    """
    reason = '{0} does not contain {comparable}'

    def op(self, value, comparable):
        """Return whether `value` contains `comparable`."""
        try:
            return comparable in value
        except TypeError:
            return False


class ContainsOnly(Comparator):
    """Asserts that `value` is an iterable and only contains `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.2.0
    """
    reason = '{0} does not only contain values in {comparable}'

    def op(self, value, comparable):
        """Return whether `value` contains only values in `comparable`."""
        try:
            return all(val in comparable for val in value)
        except TypeError:
            return False


class InstanceOf(Comparator):
    """Asserts that `value` is an instance of `comparable`.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not an instance of {comparable}'
    op = isinstance


class Truthy(Assertion):
    """Asserts that `value` is truthy.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not truthy'
    op = bool


class Falsy(Assertion):
    """Asserts that `value` is falsy.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not falsy'
    op = pydash.negate(bool)


class Boolean(Assertion):
    """Asserts that `value` is a boolean.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a boolean'
    op = partial(pydash.is_boolean)


class String(Assertion):
    """Asserts that `value` is a string (``str`` or ``unicode`` on Python 2).

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a string'
    op = partial(pydash.is_string)


class Dict(Assertion):
    """Asserts that `value` is a dictionary.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a dictionary'
    op = partial(pydash.is_dict)


class List(Assertion):
    """Asserts that `value` is a list.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a list'
    op = partial(pydash.is_list)


class Tuple(Assertion):
    """Asserts that `value` is a tuple.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a tuple'
    op = partial(pydash.is_tuple)


class Int(Assertion):
    """Asserts that `value` is an integer.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not an int'
    op = partial(pydash.is_int)


class Float(Assertion):
    """Asserts that `value` is a float.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a float'
    op = partial(pydash.is_float)


class Number(Assertion):
    """Asserts that `value` is a number.

    Objects considered a number are:

    - ``int``
    - ``float``
    - ``decimal.Decimal``
    - ``long (Python 2)``

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a number'
    op = partial(pydash.is_number)


class NaN(Assertion):
    """Asserts that `value` is a not a number.

    Raises:
        AssertionError: If comparison returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is a number'
    op = partial(pydash.is_nan)
