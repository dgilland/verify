"""Assertion runners.
"""


__all__ = (
    'expect',
)


def expect(value, *assertions):
    """Pass `value` through a set of assertable functions.

    Examples:

        This will pass:

        >>> from verify import *
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
    results = (assertable(value) for assertable in assertions)
    # Consider results that evaluate to None as passing.
    results = all(result for result in results if result is not None)
    assert results, 'Not all expectations evaluated to true'
    return True
