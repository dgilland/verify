******
verify
******

|version| |travis| |coveralls| |license|

Verify is a painless assertion library for Python.


Links
=====

- Project: https://github.com/dgilland/verify
- Documentation: http://verify.readthedocs.org
- PyPI: https://pypi.python.org/pypi/verify/
- TravisCI: https://travis-ci.org/dgilland/verify


Quickstart
==========

Install using pip:


::

    pip install verify


Verify some value using multiple assertions:


.. code-block:: python

    from verify import expect, Not, Truthy, Falsy, Less, Greater

    expect(5 * 5,
           Truthy(),
           Not(Falsy),
           Greater(15),
           Less(30))


Verify using your own assert functions:


.. code-block:: python

    def is_just_right(value):
        assert value != 'too cold' and value != 'too hot', 'Not just right!'

    # Passes
    expect(25, is_just_right)

    # Fails
    try:
        expect(31, is_just_right)
    expect AssertionError:
        raise

Or your own predicate functions:


.. code-block:: python

    def is_awesome(value):
        return 'awesome' in value

    def is_more_awesome(value):
        return value > 'awesome'

    expect('so awesome', is_awesome, is_more_awesome)


But you don't have to use ``expect`` since the ``verify`` assertions can be used on their own:


.. code-block:: python

    import verify

    # These would pass.
    verify.Truthy(1)
    verify.Equal(2, 2)
    verify.Greater(3, 2)

    # These would fail with an AssertionError
    verify.Truthy(0)
    verify.Equal(2, 3)
    verify.Greater(2, 3)


And if you'd prefer to see ``assert`` being used, all ``verify`` assertions will return ``True`` if no ``AssertionError`` is raised:


.. code-block:: python

    assert Truthy(1)
    assert Expect(1, Truthy(), Number())


Validators
==========

All of the validators in ``verify`` are callables that can be used in two contexts:

1. By themselves as in ``Equal(a, b)`` which will raise an ``AssertionError`` if false.
2. In combination with ``expect`` as in ``expect(a, Equal(b))`` which could also raise an ``AssertionError``.

The available validators are:

======================  ===========
Validator               Description
======================  ===========
``Not``                 Assert that a callable doesn't raise an ``AssertionError``.
``Predicate``           Assert that ``predicate(a)`` (``predicate()`` should return a boolean).
``Equal``               Assert that ``a == b``.
``Match``               Assert that ``a`` matches regular expression ``b``.
``Greater``             Assert that ``a > b``.
``GreaterEqual``        Assert that ``a >= b``.
``Less``                Assert that ``a < b``.
``LessEqual``           Assert that ``a <= b``.
``Between``             Assert that ``b <= a <= c``.
``Length``              Assert that ``b <= len(a) <= c``.
``Is``                  Assert that ``a is b``.
``IsTrue``              Assert that ``a is True``.
``IsFalse``             Assert that ``a is False``.
``IsNone``              Assert that ``a is None``.
``All``                 Assert that all of the list of predicates evaluate ``a`` as truthy.
``Any``                 Assert that any of the list of predicates evaluate ``a`` as truthy.
``In``                  Assert that ``a in b``.
``Contains``            Assert that ``b in a``.
``ContainsOnly``        Assert that values from ``b`` are the only ones contained in ``a``.
``Subset``              Assert that ``a`` is a subset of ``b``.
``Superset``            Assert that ``a`` is a superset of ``b``.
``Unique``              Assert that ``a`` contains unique items.
``InstanceOf``          Assert that ``isinstance(a, b)``.
``Truthy``              Assert that ``bool(a)``.
``Falsy``               Assert that ``not bool(a)``.
``Boolean``             Assert that ``isinstance(a, bool)``.
``String``              Assert that ``isinstance(a, (str, unicode))``.
``Dict``                Assert that ``isinstance(a, dict)``.
``List``                Assert that ``isinstance(a, list)``.
``Tuple``               Assert that ``isinstance(a, tuple)``.
``Int``                 Assert that ``isinstance(a, int)``.
``Float``               Assert that ``isinstance(a, float)``.
``Number``              Assert that ``isinstance(a, (int, float, Decimal, long))``.
``NaN``                 Assert that ``not isinstance(a, (int, float, Decimal, long))``.
``Positive``            Assert that ``a > 0``.
``Negative``            Assert that ``a < 0``.
``Even``                Assert that ``a % 2 == 0``.
``Odd``                 Assert that ``a % 2 != 1``.
``Monotone``            Assert that ``a`` is monotonic with respect to ``b()``.
``Increasing``          Assert that ``a`` is monotonically increasing.
``StrictlyIncreasing``  Assert that ``a`` is strictly increasing.
``Decreasing``          Assert that ``a`` is monotonically decreasing.
``StrictlyDecreasing``  Assert that ``a`` is strictly decreasing.
``Date``                Assert that ``isinstance(a, datetime.date)``.
``DateString``          Assert that ``a`` matches the datetime format string ``b``.
======================  ===========


For more details, please see the full documentation at http://verify.readthedocs.org.


.. |version| image:: http://img.shields.io/pypi/v/verify.svg?style=flat-square
    :target: https://pypi.python.org/pypi/verify/

.. |travis| image:: http://img.shields.io/travis/dgilland/verify/master.svg?style=flat-square
    :target: https://travis-ci.org/dgilland/verify

.. |coveralls| image:: http://img.shields.io/coveralls/dgilland/verify/master.svg?style=flat-square
    :target: https://coveralls.io/r/dgilland/verify

.. |license| image:: http://img.shields.io/pypi/l/verify.svg?style=flat-square
    :target: https://pypi.python.org/pypi/verify/
