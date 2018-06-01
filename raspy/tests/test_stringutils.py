"""Test all StringUtils methods."""

from raspy import string_utils


def test_create():
    """Test create method."""
    created = string_utils.create('c', 3)
    assert created == 'ccc'


def test_pad_left():
    """Test pad_left method."""
    testString = "Hello World!"
    padded = string_utils.pad_left(testString, 'a', 3)
    assert padded == "aaaHello World!"


def test_pad_right():
    """Test pad_right method."""
    testString = "Hello World!"
    padded = string_utils.pad_right(testString, 'f', 5)
    assert padded == "Hello World!fffff"


def test_pad():
    """Test pad method."""
    testString = "FooBar"
    padded = string_utils.pad(testString, '-', 3)
    assert padded == "---FooBar---"


def test_pad_center():
    """Test pad_center method."""
    testString = "FooBar"
    char = string_utils.DEFAULT_PAD_CHAR
    padded = string_utils.pad_center(testString, char, 1)
    assert padded == "Foo Bar"


def test_ends_with():
    """Test ends_with method."""
    assert string_utils.ends_with("foo.bar", "bar")


def test_starts_with():
    """Test starts_with method."""
    assert string_utils.starts_with("foo.bar", "foo")


def test_is_null_or_empty():
    """Test is_null_or_empty method."""
    assert string_utils.is_null_or_empty(None)
    assert string_utils.is_null_or_empty(string_utils.EMPTY)


def test_trim():
    """Test trim method."""
    assert string_utils.trim("   test   ") == "test"


def test_contains():
    """Test contains method."""
    assert string_utils.contains("foo bar", "bar")


def test_convert_string_to_byte():
    """Test convert_string_to_byte method."""
    actual = string_utils.convert_string_to_byte("1")
    expected = [49]
    assert sorted(actual) == sorted(expected)
