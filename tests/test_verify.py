# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal
import operator

import pytest
import pydash

import verify as v
from verify import expect, Not


def make_parametrize_id(argvalue):
    """Return custom parameter id for test reporting."""
    if hasattr(argvalue, '__name__'):
        return '-' + argvalue.__name__
    else:
        return str(argvalue)


def raises_assertion():
    """Expect AssertionError to be raised."""
    return pytest.raises(AssertionError)


@pytest.mark.parametrize('value,assertions', [
    (5, (v.Greater(4), v.Less(6))),
])
def test_expect_multiple_assertions(value, assertions):
    """Test that Expect handles multiple assertions."""
    assert expect(value, *assertions)


@pytest.mark.parametrize('value,predicates', [
    (True, (pydash.is_boolean, pydash.identity)),
])
def test_expect_predicates(value, predicates):
    """Test that Expect handles multiple predicates that returns boolean
    values."""
    assert expect(value, *predicates)


@pytest.mark.parametrize('value,predicates', [
    (True, (pydash.is_boolean, pydash.is_number)),
    (True, (pydash.is_int, pydash.identity)),
])
def test_expect_predicates_raises(value, predicates):
    """Test that Expect handles multiple predicates that returns boolean
    values."""
    with raises_assertion():
        assert expect(value, *predicates)


@pytest.mark.parametrize('meth,value,comparables', [
    (v.Not, False, v.Truthy),
    (v.Not, True, v.Falsy),
    (v.Not, 1, pydash.is_boolean),
    (v.Predicate, True, pydash.is_boolean),
    (v.Predicate, 1, pydash.is_number),
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
    (v.Between, 5, ((4, 5),)),
    (v.Between, 5, ((None, 5),)),
    (v.Between, 5, ((5, None),)),
    (v.Between, 5, ((5, 5),)),
    (v.Between, 5, 6),
    (v.Length, [1, 2, 3, 4], 4),
    (v.Length, (1, 2, 3), 3),
    (v.Is, True, True),
    (v.Is, False, False),
    (v.Is, None, None),
    (v.Is, 1, 1),
    (v.Is, 'a', 'a'),
    (v.IsTrue, True, ()),
    (v.IsFalse, False, ()),
    (v.IsNone, None, ()),
    (v.All, True, ([pydash.is_boolean, pydash.is_nan],)),
    (v.Any, True, ([pydash.is_boolean, pydash.is_number],)),
    (v.In, 1, ([0, 1, 2],)),
    (v.In, 'a', (('a', 'b', 'c'),)),
    (v.In, 'a', 'abc'),
    (v.Contains, [1, 2, 3], 2),
    (v.Contains, {'one': 1, 'two': 2}, 'two'),
    (v.ContainsOnly, [1, 1, 1], ([1],)),
    (v.ContainsOnly, [1, 0, 1], ((1, 0),)),
    (v.Subset, {'b': 2}, ({'a': 1, 'b': 2},)),
    (v.Subset,
     {'a': [{'b': [{'d': 4}]}]},
     ({'a': [{'b': [{'c': 3, 'd': 4}]}]},)),
    (v.Subset, [1, 2], ([1, 2, 3],)),
    (v.Superset, {'a': 1, 'b': 2}, ({'b': 2},)),
    (v.Superset,
     {'a': [{'b': [{'c': 3, 'd': 4}]}]},
     ({'a': [{'b': [{'d': 4}]}]},)),
    (v.Superset, [1, 2, 3], ([1, 2],)),
    (v.Unique, [1, 2, 3, 4], ()),
    (v.Unique, {'one': 1, 'two': 2, 'thr': 3}, ()),
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
    (v.Boolean, True, ()),
    (v.Boolean, False, ()),
    (v.String, '', ()),
    (v.Dict, {}, ()),
    (v.List, [], ()),
    (v.Tuple, (), ()),
    (v.Date, datetime.date.today(), ()),
    (v.Date, datetime.datetime.now(), ()),
    (v.DateString, '2015-01-01', '%Y-%m-%d'),
    (v.DateString, '2015-01-01T01:00:59', '%Y-%m-%dT%H:%M:%S'),
    (v.Int, 1, ()),
    (v.Float, 1.1, ()),
    (v.Number, 1, ()),
    (v.Number, 0, ()),
    (v.Number, -1, ()),
    (v.Number, 1.05, ()),
    (v.Number, Decimal('1.05'), ()),
    (v.NaN, '', ()),
    (v.NaN, True, ()),
    (v.NaN, {}, ()),
    (v.Positive, 1, ()),
    (v.Positive, 100, ()),
    (v.Negative, -1, ()),
    (v.Negative, -100, ()),
    (v.Even, 2, ()),
    (v.Even, -8, ()),
    (v.Odd, 1, ()),
    (v.Odd, -5, ()),
    (v.Monotone, [1, 1, 3, 5], operator.le),
    (v.Monotone, [1, 2, 10, 20], operator.lt),
    (v.Increasing, [1, 1, 3, 5], ()),
    (v.StrictlyIncreasing, [1, 5, 10], ()),
    (v.Decreasing, [5, 3, 1, 1], ()),
    (v.StrictlyDecreasing, [5, 4, 2, 1], ()),
], ids=make_parametrize_id)
def test_assert_method(meth, value, comparables):
    """Test that method passes when evaluated for comparables."""
    if not isinstance(comparables, (list, tuple)):
        comparables = (comparables,)

    assert expect(value, meth(*comparables))
    assert meth(value, *comparables)


@pytest.mark.parametrize('meth,value,comparables', [
    (v.Not, True, v.Truthy),
    (v.Not, False, v.Falsy),
    (v.Not, True, pydash.is_boolean),
    (v.Predicate, 1, pydash.is_boolean),
    (v.Predicate, True, pydash.is_number),
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
    (v.Between, 5, 4),
    (v.Between, 5, ((1, 4),)),
    (v.Length, [1, 2, 3, 4], 3),
    (v.Length, (1, 2, 3), 2),
    (v.Length, 1, 1),
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
    (v.All, True, ([pydash.is_boolean, pydash.is_number],)),
    (v.Any, True, ([pydash.is_none, pydash.is_number],)),
    (v.In, 1, ([0, 0, 2],)),
    (v.In, 'a', (('b', 'b', 'c'),)),
    (v.In, 1, 2),
    (v.Contains, [1, 2, 3], 4),
    (v.Contains, {'one': 1, 'two': 2}, 2),
    (v.Contains, 4, 4),
    (v.ContainsOnly, 1, 1),
    (v.ContainsOnly, [1, 0], ([1],)),
    (v.Subset, {'a': 1, 'b': 2}, ({'b': 2},)),
    (v.Subset,
     {'a': [{'b': [{'c': 3, 'd': 4}]}]},
     ({'a': [{'b': [{'d': 4}]}]},)),
    (v.Subset, [1, 2, 3], ([1, 2],)),
    (v.Superset, {'b': 2}, ({'a': 1, 'b': 2},)),
    (v.Superset,
     {'a': [{'b': [{'d': 4}]}]},
     ({'a': [{'b': [{'c': 3, 'd': 4}]}]},)),
    (v.Superset, [1, 2], ([1, 2, 3],)),
    (v.Unique, [1, 1, 2], ()),
    (v.Unique, {'one': 1, 'uno': 1}, ()),
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
    (v.Boolean, None, ()),
    (v.Boolean, 1, ()),
    (v.Boolean, '', ()),
    (v.Boolean, [], ()),
    (v.String, True, ()),
    (v.String, [], ()),
    (v.Dict, [], ()),
    (v.Dict, (), ()),
    (v.Dict, False, ()),
    (v.List, {}, ()),
    (v.List, (), ()),
    (v.List, False, ()),
    (v.Tuple, {}, ()),
    (v.Tuple, [], ()),
    (v.Tuple, '', ()),
    (v.Date, '', ()),
    (v.Date, '2015-01-01', ()),
    (v.DateString, 2015, '%Y'),
    (v.DateString, '2015-29-01', '%Y-%m-%d'),
    (v.Int, '', ()),
    (v.Int, False, ()),
    (v.Int, 1.1, ()),
    (v.Float, 1, ()),
    (v.Float, '', ()),
    (v.Number, '', ()),
    (v.Number, False, ()),
    (v.Number, None, ()),
    (v.Number, {}, ()),
    (v.Number, [], ()),
    (v.NaN, 1, ()),
    (v.NaN, 0, ()),
    (v.NaN, -1, ()),
    (v.NaN, 1.05, ()),
    (v.NaN, Decimal('1.05'), ()),
    (v.Positive, -1, ()),
    (v.Positive, -100, ()),
    (v.Negative, 1, ()),
    (v.Negative, 100, ()),
    (v.Even, 1, ()),
    (v.Even, -5, ()),
    (v.Odd, 2, ()),
    (v.Odd, -8, ()),
    (v.Monotone, [1, 0, 3, 5], operator.le),
    (v.Monotone, [1, 2, 0, 20], operator.lt),
    (v.Increasing, [1, 0, 3, 5], ()),
    (v.StrictlyIncreasing, [1, 1, 10], ()),
    (v.Decreasing, [5, 3, 0, 1], ()),
    (v.StrictlyDecreasing, [5, 5, 2, 1], ()),
], ids=make_parametrize_id)
def test_assert_raises(meth, value, comparables):
    """Test that method raises an assertion error when evaluated for
    comparables.
    """
    if not isinstance(comparables, (list, tuple)):
        comparables = (comparables,)

    with raises_assertion():
        expect(value, meth(*comparables))

    with raises_assertion():
        meth(value, *comparables)
