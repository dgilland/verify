# -*- coding: utf-8 -*-
"""The verify module.
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


__all__ = tuple(name for name in globals().keys() if not name.startswith('__'))
