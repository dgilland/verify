"""Assertion runners.
"""

import re

import verify
from .base import Assertion, is_assertion


__all__ = (
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
        assertion = _find_assertion_class(attr)

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


def _find_assertion_class(name):
    try:
        return getattr(verify, name)
    except AttributeError:
        pass

    name_formatters = [
        _class_format,
        _to_be_prefix,
        _is_prefix,
        _reserved_names,
    ]

    for format_name in name_formatters:
        new_name = format_name(name)
        if new_name is None:
            continue

        try:
            return getattr(verify, new_name)
        except AttributeError:
            pass

    raise AttributeError(('"{0}" is not a valid assertion method'
                          .format(name)))


def _class_format(name):
    new_name = [part.capitalize() for part in name.split('_')]
    return ''.join(new_name)


def _to_be_prefix(name):
    return _prefixed_name(name, 'to_be_')


def _is_prefix(name):
    return _prefixed_name(name, 'is_')


def _prefixed_name(name, prefix):
    if re.match(prefix, name):
        return _class_format(name[len(prefix):])


def _reserved_names(name):
    if name == 'does':
        return 'Predicate'
    elif name == 'does_not':
        return 'Not'
