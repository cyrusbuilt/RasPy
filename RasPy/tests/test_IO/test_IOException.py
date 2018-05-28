"""Tests for IOException."""


from RasPy.IO.IOException import IOException


class TestIOException(object):
    """Test methods for IOException."""

    def test_io_exception(self):
        """Test the exception."""
        caught = None
        try:
            raise IOException("This is a test.")
        except Exception as ex:
            caught = ex

        assert isinstance(caught, IOException)
