"""Assertion runners.
"""

import re

import verify
from .base import Assertion, is_assertion


__all__ = (
    'ensure',
    'expect',
)


class expect(object):
    """Pass `value` through a set of assertable functions.

    There are two styles for invoking ``expect``:

    1. Pass `value` and all `assertions` as arguments to the ``__init__``
       method of ``expect``.
    2. Pass `value` to the ``__init__`` method of ``expect`` and invoke
       assertions via method chaining.

    Examples:

        Passing `value` and `assertions` to ``expect.__init__``:

        >>> from verify import *
        >>> expect(5, Truthy(), Greater(4))
        <expect(5)>
        >>> expect(5, Falsy())
        Traceback (most recent call last):
        ...
        AssertionError...

        Using method chaining:

        >>> expect(5).Truthy().Greater(4)
        <expect(5)>
        >>> expect(5).Falsy()
        Traceback (most recent call last):
        ...
        AssertionError...


    Args:
        value (mixed): Value to test.
        *assertions (callable, optional): Callable objects that accept `value`
            as its first argument. It's expected that these callables assert
            something.

    Returns:
        self: Allows for method assertion chaining.

    Raises:
        AssertionError: If the evaluation of all assertions returns ``False``.

    Aliases:
        - ``ensure``

    .. versionadded:: 0.0.1

    .. versionchanged:: 0.1.0

        - Rename from ``Expect`` to ``expect`` and change implementation from a
          class to a function.
        - Passed in `value` is no longer called if it's a callable.
        - Return ``True`` if all assertions pass.

    .. versionchanged:: 0.6.0

        - Re-implement as class.
        - Support method chaining of assertion classes.
        - Wrap assertions that are not derived from Assertion in
          :class:`.Predicate` for consistent behavior from external assertion
          functions.
    """
    def __init__(self, value, *assertions):
        self.value = value

        if assertions:
            self(*assertions)

    def __repr__(self):  # pragma: no cover
        return '<{0}>'.format(self)

    def __str__(self):  # pragma: no cover
        return '{0}({1})'.format(self.__class__.__name__, self.value)

    def __getattr__(self, attr):
        """Invoke assertions via attribute access. All :mod:`verify` assertions
        are available.
        """
        assertion = getattr(verify, attr, None)

        if not callable(assertion) and not attr.endswith('_'):
            # Alias method names not ending in underscore to their underscore
            # counterpart. This allows chaining of functions that have a name
            # conflict with builtins (e.g. "any_", "all_", etc).
            assertion = getattr(verify, attr + '_', None)

        if not is_assertion(assertion):
            raise AttributeError(('"{0}" is not a valid assertion method'
                                  .format(attr)))

        def chained_assertion(*args, **kargs):
            assertion(*args, **kargs)(self.value)
            return self
        chained_assertion.assertion = assertion

        return chained_assertion

    def __call__(self, *assertions):
        for assertion in assertions:
            if not is_assertion(assertion):
                # Wrap non-verify assertions in Predicate for consistent
                # behavior.
                assertion = verify.Predicate(assertion)
            assertion(self.value)
        return self


ensure = expect
