# -*- coding: utf-8 -*-
"""The verify module is composed of various assertion callables (in this case,
callable classes) that can be called in two contexts:

1. By themselves as in ``Equal(a, b)`` which will raise an ``AssertionError``
   if ``a`` does not equal ``b``.
2. In combination with :func:`.expect` as in ``expect(a, Equal(b))`` which
   could also raise an ``AssertionError``.

Thus, for all assertion classes below, the `value` argument defaults to
``NotSet`` which is a custom singleton to indicate that nothing was passed in
for `value`. Whether `value` is set or ``NotSet`` is used to indicate which
context the assertion class is being used. Whenever `value` is set, the
`comparable` is swapped with `value` (internally inside the class' ``__init__``
method). This allows the assertion to be used in the two contexts above.

This module's main focus is on testing, which is why all assertions raise an
``AssertionError`` on failure. Therefore, all assertion classes function
similarly:

- If the evaluation of `value` with `comparable` returns ``False``, then an
  ``AssertionError`` is raised with a custom message.
- If the evaluation of `value` with `comparable` returns ``True`` and the class
  was only created (e.g. ``Equal(a, b)``), then nothing is raised or returned
  (obviously, since all we did was create a class instance).
- If the evaluation of `value` with `comparable` returns ``True`` and the class
  was called (e.g. ``expect(a, Equal(b))`` or ``Equal(b)(a)``), then ``True``
  is returned from the class call.

There are two general types of assertions within this module:

1. Assertions that evaulate a single object: `value`. Referred to here as a
   plain assertion.
2. Assertions that evaulate two objects: `value` and `comparable`. Referred to
   here as a comparator assertion.

When using plain assertions with :func:`.expect`, you can pass the bare
assertion or initialize it.

::

    >>> expect(True, Truthy)
    <expect(True)>
    >>> expect(True, Truthy())
    <expect(True)>

When using any of the assertions, inserting ``assert`` in front is optional as
each assertion will raise if the evaluation is false. However, having that
``assert`` in front may be aesthetically appealing to you, but keep in mind
that any assert message included will not be shown since the assertion error
will occur within the class itself and raised with it's own custom error
message.

::

    >>> Truthy(True)
    <Truthy()>
    >>> assert Truthy(True)

::

    # Both of these would raise an assertion error.
    >>> Falsy(True)
    Traceback (most recent call last):
    ...
    AssertionError: True is not falsy

    >>> assert Falsy(True)
    Traceback (most recent call last):
    ...
    AssertionError: True is not falsy

    # But assert messages will not make it to the traceback.
    >>> assert Falsy(True), 'this message will not be shown'
    Traceback (most recent call last):
    ...
    AssertionError: True is not falsy
"""

from .__meta__ import (
    __title__,
    __summary__,
    __url__,
    __version__,
    __author__,
    __email__,
    __license__
)


from .logic import (
    Truthy,
    Falsy,
    Not,
    Predicate,
    All,
    NotAll,
    Any,
    NotAny,
)

from .equality import (
    Equal,
    NotEqual,
    Match,
    NotMatch,
    Is,
    IsNot,
    IsTrue,
    IsNotTrue,
    IsFalse,
    IsNotFalse,
    IsNotNone,
    IsNone,
)

from .types import (
    Type,
    NotType,
    Boolean,
    NotBoolean,
    String,
    NotString,
    Dict,
    NotDict,
    List,
    NotList,
    Tuple,
    NotTuple,
    Date,
    NotDate,
    DateString,
    NotDateString,
    Int,
    NotInt,
    NotFloat,
    Float,
    Number,
    NotNumber,
)

from .containers import (
    In,
    NotIn,
    Contains,
    NotContains,
    ContainsOnly,
    NotContainsOnly,
    Subset,
    NotSubset,
    Superset,
    NotSuperset,
    Unique,
    NotUnique,
    Length,
)

from .numbers import (
    Greater,
    GreaterEqual,
    Less,
    LessEqual,
    Between,
    NotBetween,
    Positive,
    Negative,
    Even,
    Odd,
    Monotone,
    Increasing,
    StrictlyIncreasing,
    Decreasing,
    StrictlyDecreasing,
)

from .runners import (
    expect,
)


__all__ = (
    'Truthy',
    'Falsy',
    'Not',
    'Predicate',
    'All',
    'NotAll',
    'Any',
    'NotAny',
    'Equal',
    'NotEqual',
    'Match',
    'NotMatch',
    'Is',
    'IsNot',
    'IsTrue',
    'IsNotTrue',
    'IsFalse',
    'IsNotFalse',
    'IsNotNone',
    'IsNone',
    'Type',
    'NotType',
    'Boolean',
    'NotBoolean',
    'String',
    'NotString',
    'Dict',
    'NotDict',
    'List',
    'NotList',
    'Tuple',
    'NotTuple',
    'Date',
    'NotDate',
    'DateString',
    'NotDateString',
    'Int',
    'NotInt',
    'NotFloat',
    'Float',
    'Number',
    'NotNumber',
    'In',
    'NotIn',
    'Contains',
    'NotContains',
    'ContainsOnly',
    'NotContainsOnly',
    'Subset',
    'NotSubset',
    'Superset',
    'NotSuperset',
    'Unique',
    'NotUnique',
    'Length',
    'Greater',
    'GreaterEqual',
    'Less',
    'LessEqual',
    'Between',
    'NotBetween',
    'Positive',
    'Negative',
    'Even',
    'Odd',
    'Monotone',
    'Increasing',
    'StrictlyIncreasing',
    'Decreasing',
    'StrictlyDecreasing',
    'expect',
)
