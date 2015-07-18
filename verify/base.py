"""Base classes and mixins.
"""


class _NotSet(object):
    """Represents an unset value."""
    def __repr__(self):  # pragma: no cover
        return 'NotSet'


#: Singleton to indicate that a keyword argument was not provided.
NotSet = _NotSet()


class Assertion(object):
    """Base class for assertions.

    If `value` **is not** provided, then assertion isn't executed. This style
    of usage is used in conjuction with :class:`.expect`.

    If `value` **is** provided, then assertion is executed immediately. This
    style of usage is used when making assertions using only the class and not
    an assertion runner like :class:`.expect`.

    Keyword Arguments:
        msg (str, optional): Override assert message to use when performing
            assertion.
    """
    #: Default format string used for assert message.
    reason = ''

    #: Operation to perform to determine whether `value` is valid. **This must
    #: be set in subclass**.
    op = None

    def __init__(self, value=NotSet, **opts):
        self.set_options(opts)

        if value is not NotSet:
            self(value, **opts)

    def set_options(self, opts):
        # Optional method that sets options as class instance variables for
        # use when calling operation.
        pass

    def format_msg(self, *args, **kargs):
        """Return formatted assert message. This is used to generate the assert
        message during :meth:`__call__`. If no ``msg`` keyword argument is
        provided, then :attr:`reason` will be used as the format string. By
        default, passed in ``args`` and ``kargs`` along with the classes
        ``__dict__`` dictionary are given to the format string. In all cases,
        ``arg[0]`` will be the `value` that is being validated.
        """
        reason = kargs.pop('msg', None) or self.reason
        kargs.update(self.__dict__)
        return reason.format(*args, **kargs)

    def compare(self, value):  # pragma: no cover
        # pylint: disable=not-callable
        return self.op(value)

    def __repr__(self):  # pragma: no cover
        return '<{0}>'.format(self)

    def __str__(self):  # pragma: no cover
        return '{0}()'.format(self.__class__.__name__)

    def __call__(self, *args, **opts):
        """Execute validation.

        Keyword Arguments:
            msg (str, optional): Override assert message to use when performing
                assertion.

        Returns:
            bool: ``True`` if comparison passes, otherwise, an
                ``AssertionError`` is raised.

        Raises:
            AssertionError: If comparison returns ``False``.
        """
        fmt_kargs = {'msg': opts.pop('msg', None)}
        fmt_kargs.update(opts)

        assert self.compare(*args, **opts), self.format_msg(*args, **fmt_kargs)
        return True


class Comparator(Assertion):
    """Base class for assertions that compare two values."""
    def __init__(self, comparable, value=NotSet, **opts):
        if value is not NotSet:
            # Swap variables since the prescence of both inputs indicates we
            # are immediately executing validation.
            value, comparable = comparable, value

        # Whether we are validating now or later, set comparable on class since
        # self.compare() expects comparable to be an instance variable.
        self.comparable = comparable

        super(Comparator, self).__init__(value, **opts)

    def compare(self, value):
        # pylint: disable=not-callable
        return self.op(value, self.comparable)


class Negate(object):
    """Mixin class that negates the results of :meth:`compare` from the parent
    class.
    """
    def compare(self, *args, **opts):
        try:
            return not super(Negate, self).compare(*args, **opts)
        except AssertionError:  # pragma: no cover
            return True


def is_assertion(obj):
    """Return whether `obj` is either an instance or subclass of
    :class:`Assertion`.
    """
    try:
        return isinstance(obj, Assertion) or issubclass(obj, Assertion)
    except TypeError:
        # Happens if `obj` isn't a class.
        return False
