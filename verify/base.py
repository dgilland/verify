"""Base classes and mixins.
"""


class _NotSet(object):
    """Represents an unset value."""
    def __repr__(self):  # pragma: no cover
        return 'NotSet'


NotSet = _NotSet()


class Assertion(object):
    """Base class for assertions."""
    reason = ''
    op = None

    def __init__(self, value=NotSet):
        if value is not NotSet:
            self(value)

    def message(self, *args, **kargs):
        kargs.update(self.__dict__)
        return self.reason.format(*args, **kargs)

    def compare(self, value):  # pragma: no cover
        # pylint: disable=not-callable
        return self.op(value)

    def __repr__(self):  # pragma: no cover
        return '<{0}>'.format(self)

    def __str__(self):  # pragma: no cover
        return '{0}()'.format(self.__class__.__name__)

    def __call__(self, *args, **kargs):
        """Our main entry point for executing validation.

        Returns:
            bool: ``True`` if comparison passes, otherwise, an
                ``AssertionError`` is raised.

        Raises:
            AssertionError: If comparison returns ``False``.
        """
        assert self.compare(*args, **kargs), self.message(*args, **kargs)
        return True


class Comparator(Assertion):
    """Base class for assertions that compare two values."""
    def __init__(self, comparable, value=NotSet):
        if value is not NotSet:
            # Swap variables since the prescence of both inputs indicates we
            # are immediately executing validation.
            value, comparable = comparable, value

        # Whether we are validation now or later, set comparable on class since
        # self.compare() expects comparable to be an instance variable.
        self.comparable = comparable

        if value is not NotSet:
            # Immediately execute validation.
            self(value)

    def compare(self, value):
        # pylint: disable=not-callable
        return self.op(value, self.comparable)


class Negate(object):
    """Mixin class that negates the results of :meth:`compare` from the parent
    class.
    """
    def compare(self, *args, **kargs):
        try:
            return not super(Negate, self).compare(*args, **kargs)
        except AssertionError:  # pragma: no cover
            return True


def is_assertion(obj):
    """Return whether `obj` is either an instance or subclass of
    :class:`Assertion`.
    """
    is_instance = isinstance(obj, Assertion)

    try:
        is_subclass = issubclass(obj, Assertion)
    except TypeError:
        # Happens if `obj` isn't a class.
        is_subclass = False

    return is_instance or is_subclass
