.. _api:

API Reference
=============

.. testsetup::

    from verify import *


The verify module is composed of various assertion callables (in this case, callable classes) that can be called in two contexts:

1. By themselves as in ``Equal(a, b)`` which will raise an ``AssertionError`` if ``a`` does not equal ``b``.
2. In combination with :func:`.expect` as in ``expect(a, Equal(b))`` which could also raise an ``AssertionError``.

Thus, for all assertion classes below, the `value` argument defaults to ``NotSet`` which is a custom singleton to indicate that nothing was passed in for `value`. Whether `value` is set or ``NotSet`` is used to indicate which context the assertion class is being used. Whenever `value` is set, the `comparable` is swapped with `value` (internally inside the class' ``__init__`` method). This allows the assertion to be used in the two contexts above.

This module's main focus is on testing, which is why all assertions raise an ``AssertionError`` on failure. Therefore, all assertion classes function similarly:

- If the evaluation of `value` with `comparable` returns ``False``, then an ``AssertionError`` is raised with a custom message.
- If the evaluation of `value` with `comparable` returns ``True`` and the class was only created (e.g. ``Equal(a, b)``), then nothing is raised or returned (obviously, since all we did was create a class instance).
- If the evaluation of `value` with `comparable` returns ``True`` and the class was called (e.g. ``expect(a, Equal(b))`` or ``Equal(b)(a)``), then ``True`` is returned from the class call.

There are two general types of assertions within this module:

1. Assertions that evaulate a single object: `value`. Referred to here as a plain assertion.
2. Assertions that evaulate two objects: `value` and `comparable`. Referred to here as a comparator assertion.

When using plain assertions with :func:`.expect`, you can pass the bare assertion or initialize it.

.. doctest::

    >>> expect(True, Truthy)
    True
    >>> expect(True, Truthy())
    True

When using any of the assertions, inserting ``assert`` in front is optional as each assertion will raise if the evaluation is false. However, having that ``assert`` in front may be aesthetically appealing to you, but keep in mind
that any assert message included will not be shown since the assertion error will occur within the class itself and raised with it's own custom error message.

.. doctest::

    >>> Truthy(True)
    <Truthy()>
    >>> assert Truthy(True)

.. doctest::

    # Both of these would raise an assertion error.
    >>> Falsy(True)
    Traceback (most recent call last):
    ...
    AssertionError...
    >>> assert Falsy(True)
    Traceback (most recent call last):
    ...
    AssertionError...

    # But assert messages will not make it to the traceback.
    >>> assert Falsy(True), 'this message will not be shown'
    Traceback (most recent call last):
    ...
    AssertionError...


Assertion Runner
----------------

The :func:`.expect` function is basically an assertion runner that takes an input `value` and passes it through any number of assertions or predicate functions. If all assertions pass **and** return truthy, then all is well and ``True`` is returned. Otherwise, either one of the assertion functions will raise an ``AssertionError`` or no exceptiosn were raised but at least one of the functions returned a non-truthy value which means that :func:`.expect` will return ``False``.

.. autofunction:: verify.expect


Assertions
----------

For all assertion classes, the `value` argument is optional, but when provided the assertion will be evaluated immediately. When passing both the `value` and `comparable` arguments, be sure that `value` comes first even though `comparable` is listed as the first argument. Internally, when both variables are passed in, `value` and `comparable` are swapped in order to support late evaulation, i.e., all of the following are equivalent ways to assert validity:


.. doctest::

    >>> Less(5, 10)
    <Less()>
    >>> Less(10)(5)
    True
    >>> expect(5, Less(10))
    True
    >>> Truthy(5)
    <Truthy()>
    >>> Truthy()(5)
    True
    >>> expect(5, Truthy())
    True

Below are the various assertion classes that can be used for validation.

.. autoclass:: verify.Not
.. autoclass:: verify.Predicate
.. autoclass:: verify.Equal
.. autoclass:: verify.Match
.. autoclass:: verify.Greater
.. autoclass:: verify.GreaterEqual
.. autoclass:: verify.Less
.. autoclass:: verify.LessEqual
.. autoclass:: verify.Between
.. autoclass:: verify.Length
.. autoclass:: verify.All
.. autoclass:: verify.Any
.. autoclass:: verify.In
.. autoclass:: verify.Contains
.. autoclass:: verify.ContainsOnly
.. autoclass:: verify.Subset
.. autoclass:: verify.Superset
.. autoclass:: verify.Unique
.. autoclass:: verify.Type
.. autoclass:: verify.Is
.. autoclass:: verify.IsTrue
.. autoclass:: verify.IsFalse
.. autoclass:: verify.IsNone
.. autoclass:: verify.Truthy
.. autoclass:: verify.Falsy
.. autoclass:: verify.Boolean
.. autoclass:: verify.String
.. autoclass:: verify.Dict
.. autoclass:: verify.List
.. autoclass:: verify.Tuple
.. autoclass:: verify.Date
.. autoclass:: verify.DateString
.. autoclass:: verify.Int
.. autoclass:: verify.Float
.. autoclass:: verify.Number
.. autoclass:: verify.Positive
.. autoclass:: verify.Negative
.. autoclass:: verify.Even
.. autoclass:: verify.Odd
.. autoclass:: verify.Monotone
.. autoclass:: verify.Increasing
.. autoclass:: verify.StrictlyIncreasing
.. autoclass:: verify.Decreasing
.. autoclass:: verify.StrictlyDecreasing
.. autoclass:: verify.NotEqual
.. autoclass:: verify.NotMatch
.. autoclass:: verify.NotBetween
.. autoclass:: verify.IsNot
.. autoclass:: verify.IsNotTrue
.. autoclass:: verify.IsNotFalse
.. autoclass:: verify.IsNotNone
.. autoclass:: verify.NotAll
.. autoclass:: verify.NotAny
.. autoclass:: verify.NotIn
.. autoclass:: verify.NotContains
.. autoclass:: verify.NotContainsOnly
.. autoclass:: verify.NotSubset
.. autoclass:: verify.NotSuperset
.. autoclass:: verify.NotUnique
.. autoclass:: verify.NotType
.. autoclass:: verify.NotBoolean
.. autoclass:: verify.NotString
.. autoclass:: verify.NotDict
.. autoclass:: verify.NotList
.. autoclass:: verify.NotTuple
.. autoclass:: verify.NotDate
.. autoclass:: verify.NotDateString
.. autoclass:: verify.NotInt
.. autoclass:: verify.NotFloat
.. autoclass:: verify.NotNumber
