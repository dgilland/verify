# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal
import operator
import re

import pytest
import pydash

import verify as v
from verify import expect, Not


class Arg(object):
    def __init__(self, *args, **kargs):
        self.args = args
        self.kargs = kargs

    def __repr__(self):
        return '{0}-{1}'.format(self.args, self.kargs)
    __str__ = __repr__


def assert_truthy(value):
    assert value


def make_parametrize_id(argvalue):
    """Return custom parameter id for test reporting."""
    if isinstance(argvalue, Arg):
        return str(argvalue)
    elif hasattr(argvalue, '__name__'):
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
    values.
    """
    assert expect(value, *predicates)


@pytest.mark.parametrize('value,predicates', [
    (True, (pydash.is_boolean, pydash.is_number)),
    (True, (pydash.is_int, pydash.identity)),
])
def test_expect_predicates_raises(value, predicates):
    """Test that Expect handles multiple predicates that returns boolean
    values.
    """
    with raises_assertion():
        assert expect(value, *predicates)


def test_expect_predicates_return_none():
    assert expect(True, assert_truthy)


def test_expect_chaining():
    assert expect(True).Boolean()(assert_truthy)
    assert expect(True, v.Boolean(), assert_truthy).Truthy()


def test_expect_chain_method_proxy():
    for method in [method for method in v.__all__ if method[0].isupper()]:
        assert getattr(v, method) is getattr(expect(None), method).assertion


def test_expect_chain_invalid_method():
    with pytest.raises(AttributeError):
        expect(None).nosuchmethod


@pytest.mark.parametrize('meth,value,arg', [
    (v.Not, False, Arg(v.Truthy)),
    (v.Not, True, Arg(v.Falsy)),
    (v.Not, 1, Arg(pydash.is_boolean)),
    (v.Predicate, True, Arg(pydash.is_boolean)),
    (v.Predicate, 1, Arg(pydash.is_number)),
    (v.Equal, 1, Arg(1)),
    (v.Equal, True, Arg(True)),
    (v.Equal, 1, Arg(True)),
    (v.Equal, 0, Arg(False)),
    (v.Equal, 'abc', Arg('abc')),
    (v.Match, 'abc', Arg(r'\w+')),
    (v.Match, 'abc', Arg(re.compile(r'\w+'))),
    (v.Greater, 5, Arg(4)),
    (v.Greater, 10, Arg(-10)),
    (v.Greater, 'b', Arg('a')),
    (v.Greater, True, Arg(False)),
    (v.GreaterEqual, 5, Arg(5)),
    (v.GreaterEqual, 5, Arg(4)),
    (v.GreaterEqual, 10, Arg(-10)),
    (v.GreaterEqual, 'b', Arg('a')),
    (v.GreaterEqual, True, Arg(False)),
    (v.Less, -10, Arg(10)),
    (v.Less, 4, Arg(5)),
    (v.Less, 'a', Arg('b')),
    (v.LessEqual, 5, Arg(5)),
    (v.LessEqual, 4, Arg(5)),
    (v.LessEqual, 'a', Arg('b')),
    (v.Between, 5, Arg((4, 5))),
    (v.Between, 5, Arg((None, 5))),
    (v.Between, 5, Arg((5, None))),
    (v.Between, 5, Arg((5, 5))),
    (v.Between, 5, Arg(6)),
    (v.Between, 5, Arg(min=4, max=6)),
    (v.Between, 5, Arg(min=4)),
    (v.Between, 5, Arg(max=6)),
    (v.Length, [1, 2, 3, 4], Arg(4)),
    (v.Length, (1, 2, 3), Arg(3)),
    (v.Length, [1, 2, 3, 4], Arg((3, 5))),
    (v.Length, [1, 2, 3, 4], Arg(min=3, max=5)),
    (v.Length, [1, 2, 3, 4], Arg(min=3)),
    (v.Length, [1, 2, 3, 4], Arg(max=5)),
    (v.Is, True, Arg(True)),
    (v.Is, False, Arg(False)),
    (v.Is, None, Arg(None)),
    (v.Is, 1, Arg(1)),
    (v.Is, 'a', Arg('a')),
    (v.IsTrue, True, Arg()),
    (v.IsFalse, False, Arg()),
    (v.IsNone, None, Arg()),
    (v.All, True, Arg([pydash.is_boolean, pydash.is_nan])),
    (v.Any, True, Arg([pydash.is_boolean, pydash.is_number])),
    (v.In, 1, Arg([0, 1, 2])),
    (v.In, 'a', Arg(('a', 'b', 'c'))),
    (v.In, 'a', Arg('abc')),
    (v.Contains, [1, 2, 3], Arg(2)),
    (v.Contains, {'one': 1, 'two': 2}, Arg('two')),
    (v.ContainsOnly, [1, 1, 1], Arg([1])),
    (v.ContainsOnly, [1, 0, 1], Arg((1, 0))),
    (v.Subset, {'b': 2}, Arg({'a': 1, 'b': 2})),
    (v.Subset,
     {'a': [{'b': [{'d': 4}]}]},
     Arg({'a': [{'b': [{'c': 3, 'd': 4}]}]})),
    (v.Subset, [1, 2], Arg([1, 2, 3])),
    (v.Superset, {'a': 1, 'b': 2}, Arg({'b': 2})),
    (v.Superset,
     {'a': [{'b': [{'c': 3, 'd': 4}]}]},
     Arg({'a': [{'b': [{'d': 4}]}]})),
    (v.Superset, [1, 2, 3], Arg([1, 2])),
    (v.Unique, [1, 2, 3, 4], Arg()),
    (v.Unique, {'one': 1, 'two': 2, 'thr': 3}, Arg()),
    (v.Type, True, Arg(bool)),
    (v.Type, 'abc', Arg(str)),
    (v.Type, 1, Arg(int)),
    (v.Truthy, True, Arg()),
    (v.Truthy, 1, Arg()),
    (v.Truthy, 'verify', Arg()),
    (v.Falsy, False, Arg()),
    (v.Falsy, None, Arg()),
    (v.Falsy, 0, Arg()),
    (v.Falsy, '', Arg()),
    (v.Boolean, True, Arg()),
    (v.Boolean, False, Arg()),
    (v.String, '', Arg()),
    (v.Dict, {}, Arg()),
    (v.List, [], Arg()),
    (v.Tuple, (), Arg()),
    (v.Date, datetime.date.today(), Arg()),
    (v.Date, datetime.datetime.now(), Arg()),
    (v.DateString, '2015-01-01', Arg('%Y-%m-%d')),
    (v.DateString, '2015-01-01T01:00:59', Arg('%Y-%m-%dT%H:%M:%S')),
    (v.Int, 1, Arg()),
    (v.Float, 1.1, Arg()),
    (v.Number, 1, Arg()),
    (v.Number, 0, Arg()),
    (v.Number, -1, Arg()),
    (v.Number, 1.05, Arg()),
    (v.Number, Decimal('1.05'), Arg()),
    (v.Positive, 1, Arg()),
    (v.Positive, 100, Arg()),
    (v.Negative, -1, Arg()),
    (v.Negative, -100, Arg()),
    (v.Even, 2, Arg()),
    (v.Even, -8, Arg()),
    (v.Odd, 1, Arg()),
    (v.Odd, -5, Arg()),
    (v.Monotone, [1, 1, 3, 5], Arg(operator.le)),
    (v.Monotone, [1, 2, 10, 20], Arg(operator.lt)),
    (v.Increasing, [1, 1, 3, 5], Arg()),
    (v.StrictlyIncreasing, [1, 5, 10], Arg()),
    (v.Decreasing, [5, 3, 1, 1], Arg()),
    (v.StrictlyDecreasing, [5, 4, 2, 1], Arg()),
    (v.NotEqual, 1, Arg(2)),
    (v.NotEqual, True, Arg(False)),
    (v.NotEqual, 'abc', Arg('cba')),
    (v.NotMatch, '###', Arg(r'\w+')),
    (v.NotMatch, '###', Arg(re.compile(r'\w+'))),
    (v.NotMatch, 1, Arg(r'\w+')),
    (v.NotBetween, 5, Arg(4)),
    (v.NotBetween, 5, Arg((1, 4))),
    (v.NotBetween, 5, Arg(min=1, max=4)),
    (v.IsNot, 1, Arg(2)),
    (v.IsNot, 1, Arg(True)),
    (v.IsNot, 0, Arg(False)),
    (v.IsNot, 'a', Arg('b')),
    (v.IsNotTrue, False, Arg()),
    (v.IsNotTrue, None, Arg()),
    (v.IsNotTrue, 0, Arg()),
    (v.IsNotTrue, '', Arg()),
    (v.IsNotFalse, True, Arg()),
    (v.IsNotFalse, 1, Arg()),
    (v.IsNotFalse, 'verify', Arg()),
    (v.IsNotNone, True, Arg()),
    (v.IsNotNone, 1, Arg()),
    (v.IsNotNone, 'verify', Arg()),
    (v.NotAll, True, Arg([pydash.is_boolean, pydash.is_number])),
    (v.NotAny, True, Arg([pydash.is_none, pydash.is_number])),
    (v.NotIn, 1, Arg([0, 0, 2])),
    (v.NotIn, 'a', Arg(('b', 'b', 'c'))),
    (v.NotIn, 1, Arg(2)),
    (v.NotContains, [1, 2, 3], Arg(4)),
    (v.NotContains, {'one': 1, 'two': 2}, Arg(2)),
    (v.NotContains, 4, Arg(4)),
    (v.NotContainsOnly, 1, Arg(1)),
    (v.NotContainsOnly, [1, 0], Arg([1])),
    (v.NotSubset, {'a': 1, 'b': 2}, Arg({'b': 2})),
    (v.NotSubset,
     {'a': [{'b': [{'c': 3, 'd': 4}]}]},
     Arg({'a': [{'b': [{'d': 4}]}]})),
    (v.NotSubset, [1, 2, 3], Arg([1, 2])),
    (v.NotSuperset, {'b': 2}, Arg({'a': 1, 'b': 2})),
    (v.NotSuperset,
     {'a': [{'b': [{'d': 4}]}]},
     Arg({'a': [{'b': [{'c': 3, 'd': 4}]}]})),
    (v.NotSuperset, [1, 2], Arg([1, 2, 3])),
    (v.NotUnique, [1, 1, 2], Arg()),
    (v.NotUnique, {'one': 1, 'uno': 1}, Arg()),
    (v.NotType, True, Arg(str)),
    (v.NotType, 'abc', Arg(int)),
    (v.NotType, 1, Arg(str)),
    (v.NotBoolean, None, Arg()),
    (v.NotBoolean, 1, Arg()),
    (v.NotBoolean, '', Arg()),
    (v.NotBoolean, [], Arg()),
    (v.NotString, True, Arg()),
    (v.NotString, [], Arg()),
    (v.NotDict, [], Arg()),
    (v.NotDict, (), Arg()),
    (v.NotDict, False, Arg()),
    (v.NotList, {}, Arg()),
    (v.NotList, (), Arg()),
    (v.NotList, False, Arg()),
    (v.NotTuple, {}, Arg()),
    (v.NotTuple, [], Arg()),
    (v.NotTuple, '', Arg()),
    (v.NotDate, '', Arg()),
    (v.NotDate, '2015-01-01', Arg()),
    (v.NotDateString, 2015, Arg('%Y')),
    (v.NotDateString, '2015-29-01', Arg('%Y-%m-%d')),
    (v.NotInt, '', Arg()),
    (v.NotInt, False, Arg()),
    (v.NotInt, 1.1, Arg()),
    (v.NotFloat, 1, Arg()),
    (v.NotFloat, '', Arg()),
    (v.NotNumber, '', Arg()),
    (v.NotNumber, True, Arg()),
    (v.NotNumber, {}, Arg()),
], ids=make_parametrize_id)
def test_assert_method(meth, value, arg):
    """Test that method passes when evaluated for comparables."""
    assert expect(value, meth(*arg.args, **arg.kargs))
    assert meth(value, *arg.args, **arg.kargs)


@pytest.mark.parametrize('meth,value,arg', [
    (v.Not, True, Arg(v.Truthy)),
    (v.Not, False, Arg(v.Falsy)),
    (v.Not, True, Arg(pydash.is_boolean)),
    (v.Predicate, 1, Arg(pydash.is_boolean)),
    (v.Predicate, True, Arg(pydash.is_number)),
    (v.Predicate, False, Arg(assert_truthy)),
    (v.Equal, 1, Arg(2)),
    (v.Equal, True, Arg(False)),
    (v.Equal, 'abc', Arg('cba')),
    (v.Match, '###', Arg(r'\w+')),
    (v.Match, '###', Arg(re.compile(r'\w+'))),
    (v.Match, 1, Arg(r'\w+')),
    (v.Greater, 5, Arg(5)),
    (v.Greater, 4, Arg(5)),
    (v.Greater, 'a', Arg('b')),
    (v.GreaterEqual, 4, Arg(5)),
    (v.GreaterEqual, 'a', Arg('b')),
    (v.GreaterEqual, False, Arg(True)),
    (v.Less, 5, Arg(4)),
    (v.Less, 10, Arg(-10)),
    (v.Less, 'b', Arg('a')),
    (v.Less, True, Arg(False)),
    (v.LessEqual, 5, Arg(4)),
    (v.LessEqual, 10, Arg(-10)),
    (v.LessEqual, 'b', Arg('a')),
    (v.LessEqual, True, Arg(False)),
    (v.Between, 5, Arg(4)),
    (v.Between, 5, Arg((1, 4))),
    (v.Between, 5, Arg(min=1, max=4)),
    (v.Length, [1, 2, 3, 4], Arg((3, 3))),
    (v.Length, (1, 2, 3), Arg((2, 2))),
    (v.Length, 1, Arg((1, 1))),
    (v.Length, [1, 2, 3, 4], Arg(max=3)),
    (v.Is, 1, Arg(2)),
    (v.Is, 1, Arg(True)),
    (v.Is, 0, Arg(False)),
    (v.Is, 'a', Arg('b')),
    (v.IsTrue, False, Arg()),
    (v.IsTrue, None, Arg()),
    (v.IsTrue, 0, Arg()),
    (v.IsTrue, '', Arg()),
    (v.IsFalse, True, Arg()),
    (v.IsFalse, 1, Arg()),
    (v.IsFalse, 'verify', Arg()),
    (v.IsNone, True, Arg()),
    (v.IsNone, 1, Arg()),
    (v.IsNone, 'verify', Arg()),
    (v.All, True, Arg([pydash.is_boolean, pydash.is_number])),
    (v.Any, True, Arg([pydash.is_none, pydash.is_number])),
    (v.In, 1, Arg([0, 0, 2])),
    (v.In, 'a', Arg(('b', 'b', 'c'))),
    (v.In, 1, Arg(2)),
    (v.Contains, [1, 2, 3], Arg(4)),
    (v.Contains, {'one': 1, 'two': 2}, Arg(2)),
    (v.Contains, 4, Arg(4)),
    (v.ContainsOnly, 1, Arg(1)),
    (v.ContainsOnly, [1, 0], Arg([1])),
    (v.Subset, {'a': 1, 'b': 2}, Arg({'b': 2})),
    (v.Subset,
     {'a': [{'b': [{'c': 3, 'd': 4}]}]},
     Arg({'a': [{'b': [{'d': 4}]}]})),
    (v.Subset, [1, 2, 3], Arg([1, 2])),
    (v.Superset, {'b': 2}, Arg({'a': 1, 'b': 2})),
    (v.Superset,
     {'a': [{'b': [{'d': 4}]}]},
     Arg({'a': [{'b': [{'c': 3, 'd': 4}]}]})),
    (v.Superset, [1, 2], Arg([1, 2, 3])),
    (v.Unique, [1, 1, 2], Arg()),
    (v.Unique, {'one': 1, 'uno': 1}, Arg()),
    (v.Type, True, Arg(str)),
    (v.Type, 'abc', Arg(int)),
    (v.Type, 1, Arg(str)),
    (v.Truthy, False, Arg()),
    (v.Truthy, None, Arg()),
    (v.Truthy, 0, Arg()),
    (v.Truthy, '', Arg()),
    (v.Falsy, True, Arg()),
    (v.Falsy, 1, Arg()),
    (v.Falsy, 'verify', Arg()),
    (v.Boolean, None, Arg()),
    (v.Boolean, 1, Arg()),
    (v.Boolean, '', Arg()),
    (v.Boolean, [], Arg()),
    (v.String, True, Arg()),
    (v.String, [], Arg()),
    (v.Dict, [], Arg()),
    (v.Dict, (), Arg()),
    (v.Dict, False, Arg()),
    (v.List, {}, Arg()),
    (v.List, (), Arg()),
    (v.List, False, Arg()),
    (v.Tuple, {}, Arg()),
    (v.Tuple, [], Arg()),
    (v.Tuple, '', Arg()),
    (v.Date, '', Arg()),
    (v.Date, '2015-01-01', Arg()),
    (v.DateString, 2015, Arg('%Y')),
    (v.DateString, '2015-29-01', Arg('%Y-%m-%d')),
    (v.Int, '', Arg()),
    (v.Int, False, Arg()),
    (v.Int, 1.1, Arg()),
    (v.Float, 1, Arg()),
    (v.Float, '', Arg()),
    (v.Number, '', Arg()),
    (v.Number, False, Arg()),
    (v.Number, None, Arg()),
    (v.Number, {}, Arg()),
    (v.Number, [], Arg()),
    (v.Positive, -1, Arg()),
    (v.Positive, -100, Arg()),
    (v.Negative, 1, Arg()),
    (v.Negative, 100, Arg()),
    (v.Even, 1, Arg()),
    (v.Even, -5, Arg()),
    (v.Odd, 2, Arg()),
    (v.Odd, -8, Arg()),
    (v.Monotone, [1, 0, 3, 5], Arg(operator.le)),
    (v.Monotone, [1, 2, 0, 20], Arg(operator.lt)),
    (v.Increasing, [1, 0, 3, 5], Arg()),
    (v.StrictlyIncreasing, [1, 1, 10], Arg()),
    (v.Decreasing, [5, 3, 0, 1], Arg()),
    (v.StrictlyDecreasing, [5, 5, 2, 1], Arg()),
    (v.NotEqual, 1, Arg(1)),
    (v.NotEqual, True, Arg(True)),
    (v.NotEqual, 1, Arg(True)),
    (v.NotEqual, 0, Arg(False)),
    (v.NotEqual, 'abc', Arg('abc')),
    (v.NotMatch, 'abc', Arg(r'\w+')),
    (v.NotMatch, 'abc', Arg(re.compile(r'\w+'))),
    (v.NotBetween, 5, Arg((4, 5))),
    (v.NotBetween, 5, Arg((None, 5))),
    (v.NotBetween, 5, Arg((5, None))),
    (v.NotBetween, 5, Arg((5, 5))),
    (v.NotBetween, 5, Arg(6)),
    (v.NotBetween, 5, Arg(min=4, max=6)),
    (v.NotBetween, 5, Arg(min=4)),
    (v.NotBetween, 5, Arg(max=6)),
    (v.IsNot, True, Arg(True)),
    (v.IsNot, False, Arg(False)),
    (v.IsNot, None, Arg(None)),
    (v.IsNot, 1, Arg(1)),
    (v.IsNot, 'a', Arg('a')),
    (v.IsNotTrue, True, Arg()),
    (v.IsNotFalse, False, Arg()),
    (v.IsNotNone, None, Arg()),
    (v.NotAll, True, Arg([pydash.is_boolean, pydash.is_nan])),
    (v.NotAny, True, Arg([pydash.is_boolean, pydash.is_number])),
    (v.NotIn, 1, Arg([0, 1, 2])),
    (v.NotIn, 'a', Arg(('a', 'b', 'c'))),
    (v.NotIn, 'a', Arg('abc')),
    (v.NotContains, [1, 2, 3], Arg(2)),
    (v.NotContains, {'one': 1, 'two': 2}, Arg('two')),
    (v.NotContainsOnly, [1, 1, 1], Arg([1])),
    (v.NotContainsOnly, [1, 0, 1], Arg((1, 0))),
    (v.NotSubset, {'b': 2}, Arg({'a': 1, 'b': 2})),
    (v.NotSubset,
     {'a': [{'b': [{'d': 4}]}]},
     Arg({'a': [{'b': [{'c': 3, 'd': 4}]}]})),
    (v.NotSubset, [1, 2], Arg([1, 2, 3])),
    (v.NotSuperset, {'a': 1, 'b': 2}, Arg({'b': 2})),
    (v.NotSuperset,
     {'a': [{'b': [{'c': 3, 'd': 4}]}]},
     Arg({'a': [{'b': [{'d': 4}]}]})),
    (v.NotSuperset, [1, 2, 3], Arg([1, 2])),
    (v.NotUnique, [1, 2, 3, 4], Arg()),
    (v.NotUnique, {'one': 1, 'two': 2, 'thr': 3}, Arg()),
    (v.NotType, True, Arg(bool)),
    (v.NotType, 'abc', Arg(str)),
    (v.NotType, 1, Arg(int)),
    (v.NotBoolean, True, Arg()),
    (v.NotBoolean, False, Arg()),
    (v.NotString, '', Arg()),
    (v.NotDict, {}, Arg()),
    (v.NotList, [], Arg()),
    (v.NotTuple, (), Arg()),
    (v.NotDate, datetime.date.today(), Arg()),
    (v.NotDate, datetime.datetime.now(), Arg()),
    (v.NotDateString, '2015-01-01', Arg('%Y-%m-%d')),
    (v.NotDateString, '2015-01-01T01:00:59', Arg('%Y-%m-%dT%H:%M:%S')),
    (v.NotInt, 1, Arg()),
    (v.NotFloat, 1.1, Arg()),
    (v.NotNumber, 1, Arg()),
    (v.NotNumber, 0, Arg()),
    (v.NotNumber, -1, Arg()),
    (v.NotNumber, 1.05, Arg()),
    (v.NotNumber, Decimal('1.05'), Arg()),
], ids=make_parametrize_id)
def test_assert_raises(meth, value, arg):
    """Test that method raises an assertion error when evaluated for
    comparables.
    """
    with raises_assertion() as exc:
        expect(value, meth(*arg.args, **arg.kargs))

    with raises_assertion() as exc:
        meth(value, *arg.args, **arg.kargs)
