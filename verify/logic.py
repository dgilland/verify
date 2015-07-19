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

    Aliases:
        - ``to_be_truthy``
        - ``is_truthy``

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not truthy'
    op = bool


to_be_truthy = Truthy
is_truthy = Truthy


class Falsy(Assertion):
    """Asserts that `value` is falsy.

    Aliases:
        - ``to_be_falsy``
        - ``is_falsy``

    .. versionadded:: 0.0.1
    """
    #:
    reason = '{0} is not falsy'
    op = pydash.negate(bool)


to_be_falsy = Falsy
is_falsy = Falsy


class Not(Comparator):
    """Asserts that `comparable` doesn't raise an ``AssertionError``. Can be
    used to create "opposite" comparators.

    Examples:

        >>> from verify import *
        >>> expect(5, Not(In([1, 2, 3])))
        <expect(5)>
        >>> Not(5, In([1, 2, 3]))
        <Not()>
        >>> Not(In([1, 2, 3]))(5)
        True

    Aliases:
        - ``not_``
        - ``does_not``
        - ``to_fail``
        - ``fails``

    .. versionadded:: 0.0.1
    """
    #:
    reason = ('The negation of {comparable} should not be true '
              'when evaluated with {0}')

    def compare(self, *args, **opts):
        try:
            return not self.comparable(*args, **opts)
        except AssertionError:
            return True


not_ = Not
does_not = Not
to_fail = Not
fails = Not


class Predicate(Comparator):
    """Asserts that `value` evaluated by the predicate `comparable` is
    ``True``.

    Aliases:
        - ``does``
        - ``to_pass``
        - ``passes``

    .. versionadded:: 0.1.0

    .. versionchanged:: 0.6.0
        Catch ``AssertionError`` thrown by `comparable` and return ``False``
        as comparison value instead.
    """
    #:
    reason = 'The evaluation of {0} using {comparable} is false'

    def compare(self, *args, **opts):
        try:
            result = self.comparable(*args, **opts)
        except AssertionError as ex:
            # Catch AssertionError so that our class will emit it's own error
            # message when False is returned.
            result = False

        if result is None:
            # Consider predicates that return None to pass. This is done to
            # support predicates that assert internally but don't have a return
            # value.
            result = True

        return result


does = Predicate
to_pass = Predicate
passes = Predicate


class All(Comparator):
    """Asserts that `value` evaluates as truthy for **all** predicates in
    `comparable`.

    Aliases:
        - ``all_``
        - ``does_all``
        - ``passes_all``

    .. versionadded:: 0.2.0
    """
    #:
    reason = '{0} is not true for all {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether all results from evaluating `value` in `comparable`
        predicates return truthy.
        """
        return all(pydash.juxtapose(*comparable)(value))

all_ = All
does_all = All
passes_all = All


class NotAll(Negate, All):
    """Asserts that `value` evaluates as falsy for **all** predicates in
    `comparable`.

    Aliases:
        - ``to_be_not_all``
        - ``does_not_all``
        - ``fails_all``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is true for all {comparable}'


not_all = NotAll
does_not_all = NotAll
fails_all = NotAll


class Any(Comparator):
    """Asserts that `value` evaluates as truthy for **any** predicates in
    `comparable`.

    Aliases:
        - ``any_``
        - ``does_any``
        - ``passes_any``

    .. versionadded:: 0.2.0
    """
    #:
    reason = '{0} is not true for any {comparable}'

    @staticmethod
    def op(value, comparable):
        """Return whether any results from evaluating `value` in `comparable`
        predicates return truthy.
        """
        return any(pydash.juxtapose(*comparable)(value))


any_ = Any
does_any = Any
passes_any = Any


class NotAny(Negate, Any):
    """Asserts that `value` evaluates as falsy for **any** predicates in
    `comparable`.

    Aliases:
        - ``not_any``
        - ``does_not_any``
        - ``fails_any``

    .. versionadded:: 0.5.0
    """
    #:
    reason = '{0} is true for some {comparable}'


not_any = NotAny
does_not_any = NotAny
fails_any = NotAny
