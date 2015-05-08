
from decimal import Decimal

import pytest

import verify
import verify as v
from verify import Expect, Not


def make_parametrize_id(argvalue):
    """Return custom parameter id for test reporting."""
    if hasattr(argvalue, '__name__'):
        return argvalue.__name__
    else:
        return str(argvalue)


def raises_assertion():
    """Expect AssertionError to be raised."""
    return pytest.raises(AssertionError)


@pytest.mark.parametrize('value,assertables', [
    (5, [v.Greater(4), v.Less(6)]),
])
def test_multiple_assertables(value, assertables):
    assert Expect(value, *assertables)


@pytest.mark.parametrize('meth,value,comparables', [
    (v.Not, False, v.Truthy),
    (v.Not, True, v.Falsy),
    (v.Equal, 1, 1),
    (v.Equal, True, True),
    (v.Equal, 1, True),
    (v.Equal, 0, False),
    (v.Equal, 'abc', 'abc'),
    (v.Greater, 5, 4),
    (v.Greater, 10, -10),
    (v.Greater, 'b', 'a'),
    (v.Greater, True, False),
    (v.GreaterEqual, 5, 5),
    (v.GreaterEqual, 5, 4),
    (v.GreaterEqual, 10, -10),
    (v.GreaterEqual, 'b', 'a'),
    (v.GreaterEqual, True, False),
    (v.Less, -10, 10),
    (v.Less, 4, 5),
    (v.Less, 'a', 'b'),
    (v.LessEqual, 5, 5),
    (v.LessEqual, 4, 5),
    (v.LessEqual, 'a', 'b'),
    (v.Is, True, True),
    (v.Is, False, False),
    (v.Is, None, None),
    (v.Is, 1, 1),
    (v.Is, 'a', 'a'),
    (v.IsTrue, True, ()),
    (v.IsFalse, False, ()),
    (v.IsNone, None, ()),
    (v.In, 1, ([0, 1, 2],)),
    (v.In, 'a', (('a', 'b', 'c'),)),
    (v.In, 'a', 'abc'),
    (v.InstanceOf, True, bool),
    (v.InstanceOf, 'abc', str),
    (v.InstanceOf, 1, int),
    (v.Truthy, True, ()),
    (v.Truthy, 1, ()),
    (v.Truthy, 'verify', ()),
    (v.Falsy, False, ()),
    (v.Falsy, None, ()),
    (v.Falsy, 0, ()),
    (v.Falsy, '', ()),
    (v.Number, 1, ()),
    (v.Number, 0, ()),
    (v.Number, -1, ()),
    (v.Number, 1.05, ()),
    (v.Number, Decimal(1.05), ()),
], ids=make_parametrize_id)
def test_assert_method(meth, value, comparables):
    if not isinstance(comparables, (list, tuple)):
        comparables = (comparables,)

    assert Expect(value, meth(*comparables))
    assert meth(value, *comparables)


@pytest.mark.parametrize('meth,value,comparables', [
    (v.Not, True, v.Truthy),
    (v.Not, False, v.Falsy),
    (v.Equal, 1, 2),
    (v.Equal, True, False),
    (v.Equal, 'abc', 'cba'),
    (v.Greater, 5, 5),
    (v.Greater, 4, 5),
    (v.Greater, 'a', 'b'),
    (v.GreaterEqual, 4, 5),
    (v.GreaterEqual, 'a', 'b'),
    (v.GreaterEqual, False, True),
    (v.Less, 5, 4),
    (v.Less, 10, -10),
    (v.Less, 'b', 'a'),
    (v.Less, True, False),
    (v.LessEqual, 5, 4),
    (v.LessEqual, 10, -10),
    (v.LessEqual, 'b', 'a'),
    (v.LessEqual, True, False),
    (v.Is, 1, 2),
    (v.Is, 1, True),
    (v.Is, 0, False),
    (v.Is, 'a', 'b'),
    (v.IsTrue, False, ()),
    (v.IsTrue, None, ()),
    (v.IsTrue, 0, ()),
    (v.IsTrue, '', ()),
    (v.IsFalse, True, ()),
    (v.IsFalse, 1, ()),
    (v.IsFalse, 'verify', ()),
    (v.IsNone, True, ()),
    (v.IsNone, 1, ()),
    (v.IsNone, 'verify', ()),
    (v.In, 1, ([0, 0, 2],)),
    (v.In, 'a', (('b', 'b', 'c'),)),
    (v.In, 1, 2),
    (v.InstanceOf, True, str),
    (v.InstanceOf, 'abc', int),
    (v.InstanceOf, 1, str),
    (v.Truthy, False, ()),
    (v.Truthy, None, ()),
    (v.Truthy, 0, ()),
    (v.Truthy, '', ()),
    (v.Falsy, True, ()),
    (v.Falsy, 1, ()),
    (v.Falsy, 'verify', ()),
    (v.Number, '', ()),
    (v.Number, False, ()),
    (v.Number, None, ()),
    (v.Number, {}, ()),
    (v.Number, [], ()),
], ids=make_parametrize_id)
def test_assert_raises(meth, value, comparables):
    if not isinstance(comparables, (list, tuple)):
        comparables = (comparables,)

    with raises_assertion():
        Expect(value, meth(*comparables))

    with raises_assertion():
        meth(value, *comparables)
