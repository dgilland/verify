.. _changelog:

Changelog
=========


v0.5.0 (2015-05-12)
-------------------

- Add ``NotEqual``.
- Add ``NotMatch``.
- Add ``NotBetween``.
- Add ``IsNot``.
- Add ``IsNotTrue``.
- Add ``IsNotFalse``.
- Add ``IsNotNone``.
- Add ``NotAll``.
- Add ``NotAny``.
- Add ``NotIn``.
- Add ``NotContains``.
- Add ``NotContainsOnly``.
- Add ``NotSubset``.
- Add ``NotSuperset``.
- Add ``NotUnique``.
- Add ``NotInstanceOf``.
- Add ``NotBoolean``.
- Add ``NotString``.
- Add ``NotDict``.
- Add ``NotList``.
- Add ``NotTuple``.
- Add ``NotDate``.
- Add ``NotDateString``.
- Add ``NotInt``.
- Add ``NotFloat``.
- Rename ``NaN`` to ``NotNumber``. (**breaking change**)


v0.4.0 (2015-05-12)
-------------------

- Make ``Between`` accept keyword arguments for ``min`` and ``max``.
- Make ``Length`` function like ``Between`` and allow comparison over range of lengths. If a single comparable value is passed in, then comparison uses the value as a max length. Previously, a single comparable value performed an equality check for length. (**breaking change**)
- Make ``Match`` accept keyword argument ``flags`` for use with string based regular expression.


v0.3.0 (2015-05-11)
-------------------

- Add ``Match``.
- Add ``Subset``.
- Add ``Superset``.
- Add ``Unique``.
- Add ``Date``.
- Add ``DateString``.
- Add ``Positive``.
- Add ``Negative``.
- Add ``Even``.
- Add ``Odd``.
- Add ``Monotone``.
- Add ``Increasing``.
- Add ``StrictlyIncreasing``.
- Add ``Decreasing``.
- Add ``StrictlyDecreasing``.


v0.2.0 (2015-05-11)
-------------------

- Add ``All``.
- Add ``Any``.
- Add ``Between``.
- Add ``Contains``.
- Add ``ContainsOnly``.
- Add ``Length``.
- Make ``Not`` compatible with bare predicate functions by return the evaluation of the `comparable`.


v0.1.1 (2015-05-08)
-------------------

- Make ``expect`` include an assertion message on failure. Without it, a cryptic ``NameError`` is thrown when a plain predicate function fails due to a generator being used in the ``all()`` call.


v0.1.0 (2015-05-08)
-------------------

- Add ``Boolean``.
- Add ``Dict``.
- Add ``Float``.
- Add ``Int``.
- Add ``IsTrue``.
- Add ``IsFalse``.
- Add ``List``.
- Add ``NaN``.
- Add ``Number``.
- Add ``Predicate``.
- Add ``String``.
- Add ``Tuple``.
- Rename ``Except`` to ``except``. (**breaking change**)
- Make ``except`` **not** call `value` if it's callable. (**breaking change**)
- Make ``except`` return ``True`` if all assertions pass.


v0.0.1 (2015-05-07)
-------------------

- First release.
