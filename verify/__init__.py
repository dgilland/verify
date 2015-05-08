# -*- coding: utf-8 -*-
"""The verify module.
"""

import operator

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
    'Expect',
    'Not',
    'Equal',
    'Greater',
    'GreaterEqual',
    'Less',
    'LessEqual',
    'Is',
    'In',
    'InstanceOf',
    'Truthy',
    'Falsy',
    'IsNone',
)


class _NotSet(object):
    """Represents an unset value."""
    def __repr__(self):  # pragma: no cover
        return 'NotSet'


NotSet = _NotSet()


class Expect(object):
    """Main class for piping `value` through a set of assertable functions. If
    all `assertables` pass, then the expectation is considered valid.

    Example:

        This will pass:

        >>> Expect(5, Truthy, Greater(4))
        <verify.Expect...>

        This will fail:

        >>> Expect(5, Falsy)
        Traceback (most recent call last):
        ...
        AssertionError: ...


    Args:
        value (mixed): Value to test.
        *assertables (callable, optional): Callable objects that accept `value`
            as its first argument. It's expected that these callables assert
            something.

    Raises:
        Exception: Whatever exception is raised in `assertables`. Generally,
            this should be an ``AssertionError``.

    .. versionadded:: 0.0.1
    """
    def __init__(self, value, *assertables):
        self.value = value() if callable(value) else value

        if assertables:
            self(*assertables)

    def __call__(self, *assertables):
        for assertable in assertables:
            assertable(self.value)


class Assertion(object):
    """Base class for assertions."""
    reason = ''
    op = None

    def __init__(self, value=NotSet):
        if value is not NotSet:
            self(value() if callable(value) else value)

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
        assert self.compare(*args, **kargs), self.message(*args, **kargs)
        return True


class Comparator(Assertion):
    """Base class for assertions that compare two values."""
    def __init__(self, comparable, value=NotSet):
        if value is not NotSet:
            value, comparable = comparable, value

        self.comparable = comparable

        if value is not NotSet:
            self(value)

    def compare(self, value):
        # pylint: disable=not-callable
        return self.op(value, self.comparable)


class NegateMixin(object):
    """Mixin class that negates an assertion."""
    def compare(self, *args, **kargs):
        return not super(NegateMixin, self).compare(*args, **kargs)


class Not(Assertion):
    """Asserts that the negation of `assertable` is ``True``."""
    reason = 'The negation of {0} should not be {assertable}'

    def __init__(self, assertable, value=NotSet):
        if value is not NotSet:
            value, assertable = assertable, value

        self.assertable = assertable

        if value is not NotSet:
            self(value)

    def compare(self, *args, **kargs):
        try:
            self.assertable(*args, **kargs)
        except AssertionError:
            return True
        else:
            return False


class Equal(Comparator):
    """Asserts that two values are equal."""
    reason = '{0} is not equal to {comparable}'
    op = operator.eq


class Greater(Comparator):
    """Asserts that `value` is greater than `comparable`."""
    reason = '{0} is not greater than {comparable}'
    op = operator.gt


class GreaterEqual(Comparator):
    """Asserts that `value` is greater than or equal to `comparable`."""
    reason = '{0} is not greater than or equal to {comparable}'
    op = operator.ge


class Less(Comparator):
    """Asserts that `value` is less than `comparable`."""
    reason = '{0} is not less than {comparable}'
    op = operator.lt


class LessEqual(Comparator):
    """Asserts that `value` is less than or equal to `comparable`."""
    reason = '{0} is not less than or equal to {comparable}'
    op = operator.le


class Is(Comparator):
    """Asserts that `value` is `comparable`."""
    reason = '{0} is not {comparable}'
    op = operator.is_


class In(Comparator):
    """Asserts that `value` is in `comparable`."""
    reason = '{0} is not in {comparable}'

    def op(self, value, comparable):
        """Return whether `value` is contained in `comparable`."""
        try:
            return value in comparable
        except TypeError:
            return False


class InstanceOf(Comparator):
    """Asserts that `value` is an instance of `comparable`."""
    reason = '{0} is not an instance of {comparable}'
    op = isinstance


class Truthy(Assertion):
    """Asserts that `value` is truthy."""
    reason = '{0} is not truthy'
    op = bool


class Falsy(NegateMixin, Truthy):
    """Asserts that `value` is falsy."""
    reason = '{0} is not falsy'


class IsNone(Assertion):
    """Asserts that `value` is None."""
    reason = '{0} is not None'
    op = Is(None)
