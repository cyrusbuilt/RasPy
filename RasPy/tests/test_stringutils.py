"""Test all StringUtils methods."""

from RasPy import StringUtils


def test_create():
    """Test create method."""
    created = StringUtils.create('c', 3)
    assert created == 'ccc'


def test_pad_left():
    """Test pad_left method."""
    testString = "Hello World!"
    padded = StringUtils.pad_left(testString, 'a', 3)
    assert padded == "aaaHello World!"


def test_pad_right():
    """Test pad_right method."""
    testString = "Hello World!"
    padded = StringUtils.pad_right(testString, 'f', 5)
    assert padded == "Hello World!fffff"


def test_pad():
    """Test pad method."""
    testString = "FooBar"
    padded = StringUtils.pad(testString, '-', 3)
    assert padded == "---FooBar---"


def test_pad_center():
    """Test pad_center method."""
    testString = "FooBar"
    char = StringUtils.DEFAULT_PAD_CHAR
    padded = StringUtils.pad_center(testString, char, 1)
    assert padded == "Foo Bar"


def test_ends_with():
    """Test ends_with method."""
    assert StringUtils.ends_with("foo.bar", "bar")


def test_starts_with():
    """Test starts_with method."""
    assert StringUtils.starts_with("foo.bar", "foo")


def test_is_null_or_empty():
    """Test is_null_or_empty method."""
    assert StringUtils.is_null_or_empty(None)
    assert StringUtils.is_null_or_empty(StringUtils.EMPTY)


def test_trim():
    """Test trim method."""
    assert StringUtils.trim("   test   ") == "test"


def test_contains():
    """Test contains method."""
    assert StringUtils.contains("foo bar", "bar")


def test_convert_string_to_byte():
    """Test convert_string_to_byte method."""
    actual = StringUtils.convert_string_to_byte("1")
    expected = [49]
    assert sorted(actual) == sorted(expected)
