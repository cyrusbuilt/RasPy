"""Tests for raspy.Size class."""

from raspy import size


class TestSize(object):
    """Class to test Size structure."""

    def test_size(self):
        """Test out the size class.

        Testing the various class methods.
        """
        s = size.Size(5, 3)
        assert s.width == 5
        assert s.height == 3

        s.width = 4
        assert s.width == 4

        s.height = 4
        assert s.height == 4

        s = size.Size(0, 0)
        e = size.EMPTY
        assert s.width == e.width
        assert s.height == e.height
