# -*- coding: utf-8 -*-
"""The verify module.
"""

import operator

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
    'Equal',
    'Greater',
    'GreaterEqual',
    'Less',
    'LessEqual',
    'In',
    'InstanceOf',
    'Is',
    'IsTrue',
    'IsFalse',
    'IsNone',
    'Predicate',
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

    Example:

        This will pass:

        >>> expect(5, Truthy, Greater(4))
        True

        This will fail:

        >>> expect(5, Falsy)
        Traceback (most recent call last):
        ...
        AssertionError: ...


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
        that we also function as a regular comparison function.

        Returns:
            True: If comparision succeeds without an ``AssertionError``

        Raises:
            AssertionError: If comparision returns ``False``.
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


class NegateMixin(object):
    """Mixin class that negates an assertion."""
    def compare(self, *args, **kargs):
        return not super(NegateMixin, self).compare(*args, **kargs)


class Not(Comparator):
    """Asserts that `comparable` doesn't raise an ``AssertionError``.

    .. versionadded:: 0.0.1
    """
    reason = 'The negation of {0} should not be {comparable}'

    def compare(self, *args, **kargs):
        try:
            self.comparable(*args, **kargs)
        except AssertionError:
            return True
        else:
            return False


class Predicate(Comparator):
    """Asserts that `value` evaluated by the predicate `comparable` is
    ``True``.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = 'The evaluation of {0} using {comparable} is false'

    def compare(self, *args, **kargs):
        return self.comparable(*args, **kargs)


class Equal(Comparator):
    """Asserts that two values are equal.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not equal to {comparable}'
    op = operator.eq


class Greater(Comparator):
    """Asserts that `value` is greater than `comparable`.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not greater than {comparable}'
    op = operator.gt


class GreaterEqual(Comparator):
    """Asserts that `value` is greater than or equal to `comparable`.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not greater than or equal to {comparable}'
    op = operator.ge


class Less(Comparator):
    """Asserts that `value` is less than `comparable`.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not less than {comparable}'
    op = operator.lt


class LessEqual(Comparator):
    """Asserts that `value` is less than or equal to `comparable`.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not less than or equal to {comparable}'
    op = operator.le


class Is(Comparator):
    """Asserts that `value` is `comparable`.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not {comparable}'
    op = operator.is_


class IsTrue(Assertion):
    """Asserts that `value` is ``True``.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not True'
    op = Is(True)


class IsFalse(Assertion):
    """Asserts that `value` is ``False``.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not False'
    op = Is(False)


class IsNone(Assertion):
    """Asserts that `value` is ``None``.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not None'
    op = Is(None)


class In(Comparator):
    """Asserts that `value` is in `comparable`.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not in {comparable}'

    def op(self, value, comparable):
        """Return whether `value` is contained in `comparable`."""
        try:
            return value in comparable
        except TypeError:
            return False


class InstanceOf(Comparator):
    """Asserts that `value` is an instance of `comparable`.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not an instance of {comparable}'
    op = isinstance


class Truthy(Assertion):
    """Asserts that `value` is truthy.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not truthy'
    op = bool


class Falsy(NegateMixin, Truthy):
    """Asserts that `value` is falsy.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not falsy'


class Boolean(Assertion):
    """Asserts that `value` is a boolean.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a boolean'
    op = Predicate(pydash.is_boolean)


class String(Assertion):
    """Asserts that `value` is a string (``str`` or ``unicode`` on Python 2).

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a string'
    op = Predicate(pydash.is_string)


class Dict(Assertion):
    """Asserts that `value` is a dictionary.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a dictionary'
    op = Predicate(pydash.is_dict)


class List(Assertion):
    """Asserts that `value` is a list.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a list'
    op = Predicate(pydash.is_list)


class Tuple(Assertion):
    """Asserts that `value` is a tuple.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a tuple'
    op = Predicate(pydash.is_tuple)


class Int(Assertion):
    """Asserts that `value` is an integer.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not an int'
    op = Predicate(pydash.is_int)


class Float(Assertion):
    """Asserts that `value` is a float.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a float'
    op = Predicate(pydash.is_float)


class Number(Assertion):
    """Asserts that `value` is a number.

    Objects considered a number are:

    - ``int``
    - ``float``
    - ``decimal.Decimal``
    - ``long (Python 2)``

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is not a number'
    op = Predicate(pydash.is_number)


class NaN(Assertion):
    """Asserts that `value` is a not a number.

    Raises:
        AssertionError: If comparision returns ``False``.

    .. versionadded:: 0.1.0
    """
    reason = '{0} is a number'
    op = Predicate(pydash.is_nan)
