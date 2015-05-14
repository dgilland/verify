# -*- coding: utf-8 -*-

import pytest
import pydash

import verify as v
from verify import expect

from .fixtures import (
    METHOD_CALL_CASES,
    METHOD_RAISE_CASES,
    raises_assertion,
    assert_truthy,
    make_parametrize_id
)


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


@pytest.mark.parametrize('meth,value,arg',
                         METHOD_CALL_CASES,
                         ids=make_parametrize_id)
def test_assert_method(meth, value, arg):
    """Test that method passes when evaluated for comparables."""
    assert expect(value, meth(*arg.args, **arg.kargs))
    assert meth(value, *arg.args, **arg.kargs)


@pytest.mark.parametrize('meth,value,arg',
                         METHOD_RAISE_CASES,
                         ids=make_parametrize_id)
def test_assert_raises(meth, value, arg):
    """Test that method raises an assertion error when evaluated for
    comparables.
    """
    with raises_assertion() as exc:
        expect(value, meth(*arg.args, **arg.kargs))

    with raises_assertion() as exc:
        meth(value, *arg.args, **arg.kargs)

