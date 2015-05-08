
import pytest

import verify
from verify import Expect, Not


truisms = [True, 1, 'verify']
falsisms = [False, None, 0,  '']


def raises_assertion():
    return pytest.raises(AssertionError)


@pytest.mark.parametrize('value,assertables', [
    (5, [verify.Greater(4), verify.Less(6)]),
])
def test_multiple_assertables(value, assertables):
    Expect(value, *assertables)


@pytest.mark.parametrize('value,assertion', [
    (False, verify.Truthy),
    (True, verify.Falsy)
])
def test_not(value, assertion):
    Expect(value,
           Not(assertion))

    assert Not(assertion)


@pytest.mark.parametrize('value,assertable', [
    (True, verify.Truthy),
    (False, verify.Falsy)
])
def test_not_raises(value, assertable):
    with raises_assertion():
        Expect(value,
               Not(assertable))

    with raises_assertion():
        Not(value, assertable)


@pytest.mark.parametrize('value,comparable', [
    (1, 1),
    (True, True),
    (1, True),
    (0, False),
    ('abc', 'abc'),
])
def test_equal(value, comparable):
    Expect(value,
           verify.Equal(comparable))

    verify.Equal(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (1, 2),
    (True, False),
    ('abc', 'cba'),
])
def test_equal_raises(value, comparable):
    with raises_assertion():
        Expect(value,
               verify.Equal(comparable))

    with raises_assertion():
        verify.Equal(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (5, 4),
    (10, -10),
    ('b', 'a'),
    (True, False),
])
def test_greater(value, comparable):
    Expect(value,
           verify.Greater(comparable))

    verify.Greater(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (5, 5),
    (4, 5),
    ('a', 'b'),
])
def test_greater_raises(value, comparable):
    with raises_assertion():
        Expect(value,
               verify.Greater(comparable))

    with raises_assertion():
        verify.Greater(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (5, 5),
    (5, 4),
    (10, -10),
    ('b', 'a'),
    (True, False),
])
def test_greater_equal(value, comparable):
    Expect(value,
           verify.GreaterEqual(comparable))

    verify.GreaterEqual(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (4, 5),
    ('a', 'b'),
    (False, True),
])
def test_greater_equal_raises(value, comparable):
    with raises_assertion():
        Expect(value,
               verify.GreaterEqual(comparable))

    with raises_assertion():
        verify.GreaterEqual(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (-10, 10),
    (4, 5),
    ('a', 'b'),
])
def test_less(value, comparable):
    Expect(value,
           verify.Less(comparable))

    verify.Less(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (5, 4),
    (10, -10),
    ('b', 'a'),
    (True, False),
])
def test_less_raises(value, comparable):
    with raises_assertion():
        Expect(value,
               verify.Less(comparable))

    with raises_assertion():
        verify.Less(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (5, 5),
    (4, 5),
    ('a', 'b'),
])
def test_less_equal(value, comparable):
    Expect(value,
           verify.LessEqual(comparable))

    verify.LessEqual(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (5, 4),
    (10, -10),
    ('b', 'a'),
    (True, False),
])
def test_less_equal_raises(value, comparable):
    with raises_assertion():
        Expect(value,
               verify.LessEqual(comparable))

    with raises_assertion():
        verify.LessEqual(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (True, True),
    (False, False),
    (None, None),
    (1, 1),
    ('a', 'a')
])
def test_is(value, comparable):
    Expect(value,
           verify.Is(comparable))

    verify.Is(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (1, 2),
    (1, True),
    (0, False),
    ('a', 'b')
])
def test_is_raises(value, comparable):
    with raises_assertion():
        Expect(value,
               verify.Is(comparable))

    with raises_assertion():
        verify.Is(value, comparable)


@pytest.mark.parametrize('value', [
    True
])
def test_is_true(value):
    Expect(value,
           verify.IsTrue())

    verify.IsTrue(value)


@pytest.mark.parametrize('value', falsisms)
def test_is_true_raises(value):
    with raises_assertion():
        Expect(value,
               verify.IsTrue())

    with raises_assertion():
        verify.IsTrue(value)


@pytest.mark.parametrize('value', [
    False
])
def test_is_false(value):
    Expect(value,
           verify.IsFalse())

    verify.IsFalse(value)


@pytest.mark.parametrize('value', truisms)
def test_is_false_raises(value):
    with raises_assertion():
        Expect(value,
               verify.IsFalse())

    with raises_assertion():
        verify.IsFalse(value)


@pytest.mark.parametrize('value', [
    None
])
def test_is_none(value):
    Expect(value,
           verify.IsNone())

    verify.IsNone(value)


@pytest.mark.parametrize('value', truisms)
def test_is_none_raises(value):
    with raises_assertion():
        Expect(value,
               verify.IsNone())

    with raises_assertion():
        verify.IsNone(value)


@pytest.mark.parametrize('value,comparable', [
    (1, [0, 1, 2]),
    ('a', ('a', 'b', 'c')),
    ('a', 'abc'),
])
def test_in(value, comparable):
    Expect(value,
           verify.In(comparable))

    verify.In(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (1, [0, 0, 2]),
    ('a', ('b', 'b', 'c')),
    (1, 2),
])
def test_in_raises(value, comparable):
    with raises_assertion():
        Expect(value,
               verify.In(comparable))

    with raises_assertion():
        verify.In(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (True, bool),
    ('abc', str),
    (1, int)
])
def test_instance_of(value, comparable):
    Expect(value,
           verify.InstanceOf(comparable))

    verify.InstanceOf(value, comparable)


@pytest.mark.parametrize('value,comparable', [
    (True, str),
    ('abc', int),
    (1, str)
])
def test_instance_of_raises(value, comparable):
    with raises_assertion():
        Expect(value,
               verify.InstanceOf(comparable))

    with raises_assertion():
        verify.InstanceOf(value, comparable)


@pytest.mark.parametrize('value', truisms)
def test_truthy(value):
    Expect(value,
           verify.Truthy())

    verify.Truthy(value)


@pytest.mark.parametrize('value', falsisms)
def test_true_raises(value):
    with raises_assertion():
        Expect(value,
               verify.Truthy())

    with raises_assertion():
        verify.Truthy(value)


@pytest.mark.parametrize('value', falsisms)
def test_falsy(value):
    Expect(value,
           verify.Falsy())

    verify.Falsy(value)


@pytest.mark.parametrize('value', truisms)
def test_falsy_raises(value):
    with raises_assertion():
        Expect(value,
               verify.Falsy())

    with raises_assertion():
        verify.Falsy(value)
