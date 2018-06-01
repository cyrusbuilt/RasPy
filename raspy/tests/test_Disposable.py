"""Tests for Disposable base class."""

from raspy.disposable import Disposable


class Foo(Disposable):
    """Test class for deriving from Disposable."""

    def __init__(self):
        super(Foo, self).__init__()


class TestDisposable(object):
    """Class to test Disposable base class."""

    @classmethod
    def test_disposable(cls):
        """Test class disposal and instantiation."""
        f = Foo()
        f.dispose()

        assert isinstance(f, Disposable)
        assert f.is_disposed
