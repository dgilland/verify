"""Assertions related to logical operations.
"""

import pydash

from .base import Assertion, Comparator, Negate


__all__ = (
    'Truthy',
    'Falsy',
    'Not',
    'Predicate',
    'All',
    'NotAll',
    'Any',
    'NotAny',
)


class Truthy(Assertion):
    """Asserts that `value` is truthy.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not truthy'
    op = bool


class Falsy(Assertion):
    """Asserts that `value` is falsy.

    .. versionadded:: 0.0.1
    """
    reason = '{0} is not falsy'
    op = pydash.negate(bool)


class Not(Comparator):
    """Asserts that `comparable` doesn't raise an ``AssertionError``. Can be
    used to create "opposite" comparators.

    Examples:

        >>> from verify import *
        >>> expect(5, Not(In([1, 2, 3])))
        True
        >>> Not(5, In([1, 2, 3]))
        <Not()>
        >>> Not(In([1, 2, 3]))(5)
        True

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

    .. versionadded:: 0.1.0
    """
    reason = 'The evaluation of {0} using {comparable} is false'

    def compare(self, *args, **kargs):
        return self.comparable(*args, **kargs)


class All(Comparator):
    """Asserts that `value` evaluates as truthy for **all** predicates in
    `comparable`.

    .. versionadded:: 0.2.0
    """
    reason = '{0} is not true for all {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether all results from evaluating `value` in `comparable`
        predicates return truthy.
        """
        return all(pydash.juxtapose(*comparable)(value))


class NotAll(Negate, All):
    """Asserts that `value` evaluates as falsy for **all** predicates in
    `comparable`.

    .. versionadded:: 0.5.0
    """
    reason = '{0} is true for all {comparable}'


class Any(Comparator):
    """Asserts that `value` evaluates as truthy for **any** predicates in
    `comparable`.

    .. versionadded:: 0.2.0
    """
    reason = '{0} is not true for any {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether any results from evaluating `value` in `comparable`
        predicates return truthy.
        """
        return any(pydash.juxtapose(*comparable)(value))


class NotAny(Negate, Any):
    """Asserts that `value` evaluates as falsy for **any** predicates in
    `comparable`.

    .. versionadded:: 0.5.0
    """
    reason = '{0} is true for some {comparable}'
