# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal
import operator
import re

import pytest
import pydash

import verify as v
from verify import expect, Not


class Argv(object):
    def __init__(self, *args, **kargs):
        self.args = args
        self.kargs = kargs

    def __repr__(self):
        return '{0}-{1}'.format(self.args, self.kargs)
    __str__ = __repr__


def make_parametrize_id(argvalue):
    """Return custom parameter id for test reporting."""
    if isinstance(argvalue, Argv):
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


@pytest.mark.parametrize('meth,value,argv', [
    (v.Not, False, Argv(v.Truthy)),
    (v.Not, True, Argv(v.Falsy)),
    (v.Not, 1, Argv(pydash.is_boolean)),
    (v.Predicate, True, Argv(pydash.is_boolean)),
    (v.Predicate, 1, Argv(pydash.is_number)),
    (v.Equal, 1, Argv(1)),
    (v.Equal, True, Argv(True)),
    (v.Equal, 1, Argv(True)),
    (v.Equal, 0, Argv(False)),
    (v.Equal, 'abc', Argv('abc')),
    (v.Match, 'abc', Argv(r'\w+')),
    (v.Match, 'abc', Argv(re.compile(r'\w+'))),
    (v.Greater, 5, Argv(4)),
    (v.Greater, 10, Argv(-10)),
    (v.Greater, 'b', Argv('a')),
    (v.Greater, True, Argv(False)),
    (v.GreaterEqual, 5, Argv(5)),
    (v.GreaterEqual, 5, Argv(4)),
    (v.GreaterEqual, 10, Argv(-10)),
    (v.GreaterEqual, 'b', Argv('a')),
    (v.GreaterEqual, True, Argv(False)),
    (v.Less, -10, Argv(10)),
    (v.Less, 4, Argv(5)),
    (v.Less, 'a', Argv('b')),
    (v.LessEqual, 5, Argv(5)),
    (v.LessEqual, 4, Argv(5)),
    (v.LessEqual, 'a', Argv('b')),
    (v.Between, 5, Argv((4, 5))),
    (v.Between, 5, Argv((None, 5))),
    (v.Between, 5, Argv((5, None))),
    (v.Between, 5, Argv((5, 5))),
    (v.Between, 5, Argv(6)),
    (v.Between, 5, Argv(min=4, max=6)),
    (v.Between, 5, Argv(min=4)),
    (v.Between, 5, Argv(max=6)),
    (v.Length, [1, 2, 3, 4], Argv(4)),
    (v.Length, (1, 2, 3), Argv(3)),
    (v.Length, [1, 2, 3, 4], Argv((3, 5))),
    (v.Length, [1, 2, 3, 4], Argv(min=3, max=5)),
    (v.Length, [1, 2, 3, 4], Argv(min=3)),
    (v.Length, [1, 2, 3, 4], Argv(max=5)),
    (v.Is, True, Argv(True)),
    (v.Is, False, Argv(False)),
    (v.Is, None, Argv(None)),
    (v.Is, 1, Argv(1)),
    (v.Is, 'a', Argv('a')),
    (v.IsTrue, True, Argv()),
    (v.IsFalse, False, Argv()),
    (v.IsNone, None, Argv()),
    (v.All, True, Argv([pydash.is_boolean, pydash.is_nan])),
    (v.Any, True, Argv([pydash.is_boolean, pydash.is_number])),
    (v.In, 1, Argv([0, 1, 2])),
    (v.In, 'a', Argv(('a', 'b', 'c'))),
    (v.In, 'a', Argv('abc')),
    (v.Contains, [1, 2, 3], Argv(2)),
    (v.Contains, {'one': 1, 'two': 2}, Argv('two')),
    (v.ContainsOnly, [1, 1, 1], Argv([1])),
    (v.ContainsOnly, [1, 0, 1], Argv((1, 0))),
    (v.Subset, {'b': 2}, Argv({'a': 1, 'b': 2})),
    (v.Subset,
     {'a': [{'b': [{'d': 4}]}]},
     Argv({'a': [{'b': [{'c': 3, 'd': 4}]}]})),
    (v.Subset, [1, 2], Argv([1, 2, 3])),
    (v.Superset, {'a': 1, 'b': 2}, Argv({'b': 2})),
    (v.Superset,
     {'a': [{'b': [{'c': 3, 'd': 4}]}]},
     Argv({'a': [{'b': [{'d': 4}]}]})),
    (v.Superset, [1, 2, 3], Argv([1, 2])),
    (v.Unique, [1, 2, 3, 4], Argv()),
    (v.Unique, {'one': 1, 'two': 2, 'thr': 3}, Argv()),
    (v.InstanceOf, True, Argv(bool)),
    (v.InstanceOf, 'abc', Argv(str)),
    (v.InstanceOf, 1, Argv(int)),
    (v.Truthy, True, Argv()),
    (v.Truthy, 1, Argv()),
    (v.Truthy, 'verify', Argv()),
    (v.Falsy, False, Argv()),
    (v.Falsy, None, Argv()),
    (v.Falsy, 0, Argv()),
    (v.Falsy, '', Argv()),
    (v.Boolean, True, Argv()),
    (v.Boolean, False, Argv()),
    (v.String, '', Argv()),
    (v.Dict, {}, Argv()),
    (v.List, [], Argv()),
    (v.Tuple, (), Argv()),
    (v.Date, datetime.date.today(), Argv()),
    (v.Date, datetime.datetime.now(), Argv()),
    (v.DateString, '2015-01-01', Argv('%Y-%m-%d')),
    (v.DateString, '2015-01-01T01:00:59', Argv('%Y-%m-%dT%H:%M:%S')),
    (v.Int, 1, Argv()),
    (v.Float, 1.1, Argv()),
    (v.Number, 1, Argv()),
    (v.Number, 0, Argv()),
    (v.Number, -1, Argv()),
    (v.Number, 1.05, Argv()),
    (v.Number, Decimal('1.05'), Argv()),
    (v.NotNumber, '', Argv()),
    (v.NotNumber, True, Argv()),
    (v.NotNumber, {}, Argv()),
    (v.Positive, 1, Argv()),
    (v.Positive, 100, Argv()),
    (v.Negative, -1, Argv()),
    (v.Negative, -100, Argv()),
    (v.Even, 2, Argv()),
    (v.Even, -8, Argv()),
    (v.Odd, 1, Argv()),
    (v.Odd, -5, Argv()),
    (v.Monotone, [1, 1, 3, 5], Argv(operator.le)),
    (v.Monotone, [1, 2, 10, 20], Argv(operator.lt)),
    (v.Increasing, [1, 1, 3, 5], Argv()),
    (v.StrictlyIncreasing, [1, 5, 10], Argv()),
    (v.Decreasing, [5, 3, 1, 1], Argv()),
    (v.StrictlyDecreasing, [5, 4, 2, 1], Argv()),
], ids=make_parametrize_id)
def test_assert_method(meth, value, argv):
    """Test that method passes when evaluated for comparables."""
    assert expect(value, meth(*argv.args, **argv.kargs))
    assert meth(value, *argv.args, **argv.kargs)


@pytest.mark.parametrize('meth,value,argv', [
    (v.Not, True, Argv(v.Truthy)),
    (v.Not, False, Argv(v.Falsy)),
    (v.Not, True, Argv(pydash.is_boolean)),
    (v.Predicate, 1, Argv(pydash.is_boolean)),
    (v.Predicate, True, Argv(pydash.is_number)),
    (v.Equal, 1, Argv(2)),
    (v.Equal, True, Argv(False)),
    (v.Equal, 'abc', Argv('cba')),
    (v.Match, '###', Argv(r'\w+')),
    (v.Match, '###', Argv(re.compile(r'\w+'))),
    (v.Match, 1, Argv(r'\w+')),
    (v.Greater, 5, Argv(5)),
    (v.Greater, 4, Argv(5)),
    (v.Greater, 'a', Argv('b')),
    (v.GreaterEqual, 4, Argv(5)),
    (v.GreaterEqual, 'a', Argv('b')),
    (v.GreaterEqual, False, Argv(True)),
    (v.Less, 5, Argv(4)),
    (v.Less, 10, Argv(-10)),
    (v.Less, 'b', Argv('a')),
    (v.Less, True, Argv(False)),
    (v.LessEqual, 5, Argv(4)),
    (v.LessEqual, 10, Argv(-10)),
    (v.LessEqual, 'b', Argv('a')),
    (v.LessEqual, True, Argv(False)),
    (v.Between, 5, Argv(4)),
    (v.Between, 5, Argv((1, 4))),
    (v.Between, 5, Argv(min=1, max=4)),
    (v.Length, [1, 2, 3, 4], Argv((3, 3))),
    (v.Length, (1, 2, 3), Argv((2, 2))),
    (v.Length, 1, Argv((1, 1))),
    (v.Length, [1, 2, 3, 4], Argv(max=3)),
    (v.Is, 1, Argv(2)),
    (v.Is, 1, Argv(True)),
    (v.Is, 0, Argv(False)),
    (v.Is, 'a', Argv('b')),
    (v.IsTrue, False, Argv()),
    (v.IsTrue, None, Argv()),
    (v.IsTrue, 0, Argv()),
    (v.IsTrue, '', Argv()),
    (v.IsFalse, True, Argv()),
    (v.IsFalse, 1, Argv()),
    (v.IsFalse, 'verify', Argv()),
    (v.IsNone, True, Argv()),
    (v.IsNone, 1, Argv()),
    (v.IsNone, 'verify', Argv()),
    (v.All, True, Argv([pydash.is_boolean, pydash.is_number])),
    (v.Any, True, Argv([pydash.is_none, pydash.is_number])),
    (v.In, 1, Argv([0, 0, 2])),
    (v.In, 'a', Argv(('b', 'b', 'c'))),
    (v.In, 1, Argv(2)),
    (v.Contains, [1, 2, 3], Argv(4)),
    (v.Contains, {'one': 1, 'two': 2}, Argv(2)),
    (v.Contains, 4, Argv(4)),
    (v.ContainsOnly, 1, Argv(1)),
    (v.ContainsOnly, [1, 0], Argv([1])),
    (v.Subset, {'a': 1, 'b': 2}, Argv({'b': 2})),
    (v.Subset,
     {'a': [{'b': [{'c': 3, 'd': 4}]}]},
     Argv({'a': [{'b': [{'d': 4}]}]})),
    (v.Subset, [1, 2, 3], Argv([1, 2])),
    (v.Superset, {'b': 2}, Argv({'a': 1, 'b': 2})),
    (v.Superset,
     {'a': [{'b': [{'d': 4}]}]},
     Argv({'a': [{'b': [{'c': 3, 'd': 4}]}]})),
    (v.Superset, [1, 2], Argv([1, 2, 3])),
    (v.Unique, [1, 1, 2], Argv()),
    (v.Unique, {'one': 1, 'uno': 1}, Argv()),
    (v.InstanceOf, True, Argv(str)),
    (v.InstanceOf, 'abc', Argv(int)),
    (v.InstanceOf, 1, Argv(str)),
    (v.Truthy, False, Argv()),
    (v.Truthy, None, Argv()),
    (v.Truthy, 0, Argv()),
    (v.Truthy, '', Argv()),
    (v.Falsy, True, Argv()),
    (v.Falsy, 1, Argv()),
    (v.Falsy, 'verify', Argv()),
    (v.Boolean, None, Argv()),
    (v.Boolean, 1, Argv()),
    (v.Boolean, '', Argv()),
    (v.Boolean, [], Argv()),
    (v.String, True, Argv()),
    (v.String, [], Argv()),
    (v.Dict, [], Argv()),
    (v.Dict, (), Argv()),
    (v.Dict, False, Argv()),
    (v.List, {}, Argv()),
    (v.List, (), Argv()),
    (v.List, False, Argv()),
    (v.Tuple, {}, Argv()),
    (v.Tuple, [], Argv()),
    (v.Tuple, '', Argv()),
    (v.Date, '', Argv()),
    (v.Date, '2015-01-01', Argv()),
    (v.DateString, 2015, Argv('%Y')),
    (v.DateString, '2015-29-01', Argv('%Y-%m-%d')),
    (v.Int, '', Argv()),
    (v.Int, False, Argv()),
    (v.Int, 1.1, Argv()),
    (v.Float, 1, Argv()),
    (v.Float, '', Argv()),
    (v.Number, '', Argv()),
    (v.Number, False, Argv()),
    (v.Number, None, Argv()),
    (v.Number, {}, Argv()),
    (v.Number, [], Argv()),
    (v.NotNumber, 1, Argv()),
    (v.NotNumber, 0, Argv()),
    (v.NotNumber, -1, Argv()),
    (v.NotNumber, 1.05, Argv()),
    (v.NotNumber, Decimal('1.05'), Argv()),
    (v.Positive, -1, Argv()),
    (v.Positive, -100, Argv()),
    (v.Negative, 1, Argv()),
    (v.Negative, 100, Argv()),
    (v.Even, 1, Argv()),
    (v.Even, -5, Argv()),
    (v.Odd, 2, Argv()),
    (v.Odd, -8, Argv()),
    (v.Monotone, [1, 0, 3, 5], Argv(operator.le)),
    (v.Monotone, [1, 2, 0, 20], Argv(operator.lt)),
    (v.Increasing, [1, 0, 3, 5], Argv()),
    (v.StrictlyIncreasing, [1, 1, 10], Argv()),
    (v.Decreasing, [5, 3, 0, 1], Argv()),
    (v.StrictlyDecreasing, [5, 5, 2, 1], Argv()),
], ids=make_parametrize_id)
def test_assert_raises(meth, value, argv):
    """Test that method raises an assertion error when evaluated for
    comparables.
    """
    with raises_assertion() as exc:
        expect(value, meth(*argv.args, **argv.kargs))

    with raises_assertion() as exc:
        meth(value, *argv.args, **argv.kargs)
