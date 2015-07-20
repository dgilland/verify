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


from .runners import (
    expect,
    ensure,
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
    NotLength,
    to_be_in,
    is_in,
    to_not_be_in,
    is_not_in,
    to_contain,
    contains,
    to_not_contain,
    does_not_contain,
    to_contain_only,
    contains_only,
    to_not_contain_only,
    does_not_contain_only,
    to_be_subset,
    is_subset,
    to_not_be_subset,
    is_not_subset,
    to_be_superset,
    is_superset,
    to_not_be_superset,
    is_not_superset,
    to_be_unique,
    is_unique,
    to_not_be_unique,
    is_not_unique,
    to_have_length,
    has_length,
    to_not_have_length,
    does_not_have_length,
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
    IsNone,
    IsNotNone,
    to_be_equal,
    is_equal,
    to_not_be_equal,
    is_not_equal,
    to_match,
    is_match,
    matches,
    to_not_match,
    is_not_match,
    does_not_match,
    to_be,
    is_,
    to_not_be,
    is_not,
    to_not_be,
    is_not,
    to_be_true,
    is_true,
    to_not_be_true,
    is_not_true,
    to_be_false,
    is_false,
    to_not_be_false,
    is_not_false,
    to_be_none,
    is_none,
    to_not_be_none,
    is_not_none,
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
    to_be_truthy,
    is_truthy,
    to_be_falsy,
    is_falsy,
    not_,
    does_not,
    to_fail,
    fails,
    does,
    to_pass,
    passes,
    all_,
    does_all,
    passes_all,
    not_all,
    does_not_all,
    fails_all,
    any_,
    does_any,
    passes_any,
    not_any,
    does_not_any,
    fails_any,
)

from .numbers import (
    Greater,
    GreaterThan,
    GreaterEqual,
    GreaterOrEqual,
    Less,
    LessThan,
    LessEqual,
    LessOrEqual,
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
    to_be_greater,
    to_be_greater_than,
    is_greater,
    is_greater_than,
    to_be_greater_equal,
    to_be_greater_or_equal,
    is_greqter_equal,
    is_greater_or_equal,
    to_be_less,
    to_be_less_than,
    is_less,
    is_less_than,
    to_be_less_equal,
    to_be_less_or_equal,
    is_less_equal,
    is_less_or_equal,
    to_be_between,
    is_between,
    to_not_be_between,
    is_not_between,
    to_be_positive,
    is_positive,
    to_be_negative,
    is_negative,
    to_be_even,
    is_even,
    to_be_odd,
    is_odd,
    to_be_monotone,
    is_monotone,
    to_be_increasing,
    is_increasing,
    to_be_strictly_increasing,
    is_strictly_increasing,
    to_be_decreasing,
    is_decreasing,
    to_be_strictly_decreasing,
    is_strictly_decreasing,
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
    to_be_type,
    is_type,
    to_not_be_type,
    is_not_type,
    to_be_boolean,
    is_boolean,
    to_not_be_boolean,
    is_not_boolean,
    to_be_string,
    is_string,
    to_not_be_string,
    is_not_string,
    to_be_dict,
    is_dict,
    to_not_be_dict,
    is_not_dict,
    to_be_list,
    is_list,
    to_not_be_list,
    is_not_list,
    to_be_tuple,
    is_tuple,
    to_not_be_tuple,
    is_not_tuple,
    to_be_date,
    is_date,
    to_not_be_date,
    is_not_date,
    to_be_date_string,
    is_date_string,
    to_not_be_date_string,
    is_not_date_string,
    to_be_int,
    is_int,
    to_not_be_int,
    is_not_int,
    to_be_float,
    is_float,
    to_not_be_float,
    is_not_float,
    to_be_number,
    is_number,
    to_not_be_number,
    is_not_number,
)
