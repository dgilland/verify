******
verify
******

|version| |travis| |coveralls| |license|

Verify is a painless assertion library for Python.


Links
=====

- Project: https://github.com/dgilland/verify
- Documentation: http://verify.readthedocs.org
- PyPi: https://pypi.python.org/pypi/verify/
- TravisCI: https://travis-ci.org/dgilland/verify


Quickstart
==========

Install using pip:


::

    pip install verify


Verify some value using verify's assertions:


.. code-block:: python

    from verify import Expect, Not, Truthy, Falsy, Less, Greater

    Expect(5 * 5,
           Truthy(),
           Not(Falsy),
           Greater(15),
           Less(30))


Verify using your own functions:


.. code-block:: python

    def is_just_right(value):
        assert 20 <= value <= 30, "it's just not right"

    # Passes
    Expect(25, is_just_right)

    # Fails
    try:
        Expect(31, is_just_right)
    except AssertionError:
        raise


Under the hood the value that's passed to ``Expect`` will be piped through all of the assertion callables that are passed to it.

You can also use the verify assertions on their own:


.. code-block:: python

    # These will pass.
    verify.Truthy(1)
    verify.Equal(2, 2)
    verify.Greater(3, 2)

    # These will fail with an AssertionError
    verify.Truthy(0)
    verify.Equal(2, 3)
    verify.Greater(2, 3)


Validators
==========

All of the validators in ``verify`` are callables that can be used in two contexts:

1. By themselves as in ``Equal(a, b)`` which will raise an ``AssertionError`` if false.
2. In combination with ``Except`` as in ``Expect(a, Equal(b))`` could also raise an ``AssertionError``.

The available validators are:

================   ===========
Validator          Description
================   ===========
``Not``            Assert that a callable doesn't raise an ``AssertionError``
``Equal``          Assert that ``a == b``
``Greater``        Assert that ``a > b``
``GreaterEqual``   Assert that ``a >= b``
``Less``           Assert that ``a < b``
``LessEqual``      Assert that ``a <= b``
``Is``             Assert that ``a is b``
``In``             Assert that ``a in b``
``InstanceOf``     Assert that ``isinstance(a, b)``
``Truthy``         Assert that ``bool(a)``
``Falsy``          Assert that ``not bool(a)``
``IsTrue``         Assert that ``a is True``
``IsFalse``        Assert that ``a is False``
``IsNone``         Assert that ``a is None``
``IsBoolean``      TODO
``IsString``       TODO
``IsDict``         TODO
``IsList``         TODO
``IsTuple``        TODO
``IsNumber``       TODO
``IsInt``          TODO
``IsFloat``        TODO
``IsNaN``          TODO
``IsDate``         TODO
``IsDatetime``     TODO
``Negative``       TODO
``Positive``       TODO
``Odd``            TODO
``Even``           TODO
``Monotone``       TODO
``Increasing``     TODO
``Decreasing``     TODO
``Contains``       TODO
``ContainsOnly``   TODO
``Any``            TODO
``All``            TODO
``Match``          TODO
``Range``          TODO
``Length``         TODO
``Datetime``       TODO
``Unique``         TODO
``ExactSequence``  TODO
``Predicate``      TODO
``Subset``         TODO
``Superset``       TODO
================   ===========


For more details, please see the full documentation at http://verify.readthedocs.org.


.. |version| image:: http://img.shields.io/pypi/v/verify.svg?style=flat-square
    :target: https://pypi.python.org/pypi/verify/

.. |travis| image:: http://img.shields.io/travis/dgilland/verify/master.svg?style=flat-square
    :target: https://travis-ci.org/dgilland/verify

.. |coveralls| image:: http://img.shields.io/coveralls/dgilland/verify/master.svg?style=flat-square
    :target: https://coveralls.io/r/dgilland/verify

.. |license| image:: http://img.shields.io/pypi/l/verify.svg?style=flat-square
    :target: https://pypi.python.org/pypi/verify/
