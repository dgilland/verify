.. _changelog:

Changelog
=========


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
