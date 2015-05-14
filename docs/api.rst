.. _api:

API Reference
=============

.. testsetup::

    from verify import *


.. automodule:: verify


Assertion Runner
----------------

The :class:`.expect` class is basically an assertion runner that takes an input `value` and passes it through any number of assertions or predicate functions. If all assertions pass **and** return truthy, then all is well and ``True`` is returned. Otherwise, either one of the assertion functions will raise an ``AssertionError`` or no exceptiosn were raised but at least one of the functions returned a non-truthy value which means that :func:`.expect` will return ``False``.

.. autoclass:: verify.runners.expect
    :members:


Assertions
----------

For all assertion classes, the `value` argument is optional, but when provided the assertion will be evaluated immediately. When passing both the `value` and `comparable` arguments, be sure that `value` comes first even though `comparable` is listed as the first argument. Internally, when both variables are passed in, `value` and `comparable` are swapped in order to support late evaulation, i.e., all of the following are equivalent ways to assert validity:


.. doctest::

    >>> Less(5, 10)
    <Less()>
    >>> Less(10)(5)
    True
    >>> expect(5, Less(10))
    <expect(5)>
    >>> Truthy(5)
    <Truthy()>
    >>> Truthy()(5)
    True
    >>> expect(5, Truthy())
    <expect(5)>

Below are the various assertion classes that can be used for validation.


Logic
+++++

.. automodule:: verify.logic
    :members:
    :exclude-members: op


Equality
++++++++

.. automodule:: verify.equality
    :members:
    :exclude-members: op


Types
+++++

.. automodule:: verify.types
    :members:
    :exclude-members: op


Containers
++++++++++

.. automodule:: verify.containers
    :members:
    :exclude-members: op

Numbers
+++++++

.. automodule:: verify.numbers
    :members:
    :exclude-members: op
