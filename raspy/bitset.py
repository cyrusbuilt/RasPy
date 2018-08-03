# pylint: disable=C0302,R0904
"""This module contains our own BitSet implementation."""


from raspy.argument_null_exception import ArgumentNullException
from raspy.illegal_argument_exception import IllegalArgumentException


ADDRESS_BITS_PER_WORD = 6
"""The number of address bits per word."""

BITS_PER_WORD = 1 << ADDRESS_BITS_PER_WORD
"""The number of bits per word."""

BIT_INDEX_MASK = BITS_PER_WORD - 1
"""The bit index mask."""

LONG_MASK = 0x3f
"""The long mask."""


def word_index(bit_index):
    """Given the specified bit index, returns the word index containing it.

    :param int bit_index: The bit index.
    :returns: The word index containing the specified bit index.
    :rtype: int
    """
    return bit_index >> ADDRESS_BITS_PER_WORD


def check_range(from_index, to_index):
    """Check to see if the specified indexes are in range.

    :param int from_index: The starting index.
    :param int to_index: The ending index.
    :raises: ArgumentNullException if either param is None.
    :raises: IllegalArgumentException if either param is not an int.
    :raises: IndexError if either param is less than zero.
    """
    if from_index is None:
        raise ArgumentNullException("from_index cannot be None.")

    if to_index is None:
        raise ArgumentNullException("to_index cannot be None.")

    if not isinstance(from_index, int):
        raise IllegalArgumentException("from_index MUST be an int.")

    if not isinstance(to_index, int):
        raise IllegalArgumentException("to_index MUST be an int.")

    if from_index < 0:
        raise IndexError("from_index cannot be less than zero.")

    if to_index < 0:
        raise IndexError("to_index cannot be less than zero.")

    if from_index > to_index:
        raise IndexError("from_index cannot be greater than to_index.")


def number_of_trailing_zeros(num):
    """Get the number or trailing zeros in the specified number.

    :param int num: The number value to inspect.
    :returns: The number of trailing zeros.
    :rtype: int
    :raises: IllegalArgumentException if the 'num' param is not a number.
    """
    if num is None:
        return 0

    if not isinstance(num, int):
        raise IllegalArgumentException("param 'num' must be an int.")

    mask = 1
    result = 64
    for i in range(0, 63):
        mask <<= 1
        if (num & mask) != 0:
            result = i
            break
    return result


def from_word_array(words):
    """Get a new BitSet from the specified word array.

    :param list words: A list of bits to convert to a BitSet.
    :returns: A new BitSet containing the specified bits.
    :rtype: BitSet
    """
    if not isinstance(words, list):
        return None

    return BitSet(words)


class BitSet(object):
    """An implementation of a vector of bits that grows as needed.

    Each component of the bit set has a Boolean value. The bits of a BitSet
    are indexed by non-negative integers. Individual indexed bits can be
    examined, set, or cleared. One BitSet may be used to modify the contents
    of another through logical AND, logical inclusive OR, and logical
    exclusive OR operations. By default, all bits in the set initially have
    the value of False. Every BitSet has a current size, which is the number
    of bits of space currently in use by the BitSet. Note that the size is
    related to the implementation of a BitSet, so it may change with
    implementation. The length of a BitSet relates to the logical length of a
    BitSet and is defined independently of implementation. Unless otherwise
    noted, passing a None parameter to any of the methods in a BitSet will
    result in a ArgumentNullException.
    """

    def __init__(self, bits):
        """Initialize a new instance of BitSet.

        :param int, list bits: The initial size of the BitSet -or- a list of
        words bits (words) to compose this instance from.
        :raises: IllegalArgumentException if 'bits' param is not a valid type
        (must be an int or a list of bits).
        :raises: IndexError if 'bits' is an int but is less than zero.
        """
        self.__bits = list()
        self.__words_in_use = 0
        self.__size_is_sticky = False
        self.name = "BitSet"

        # Main constructor logic.
        if bits is None:
            self.__bits = [None] * BITS_PER_WORD
        else:
            if isinstance(bits, int):
                if bits < 0:
                    raise IndexError("'bits' param must not be negative.")

                self.__bits = [None] * word_index(bits - 1) + 1
                self.__size_is_sticky = True
            elif isinstance(bits, list):
                self.__bits = bits
                self.__words_in_use = len(self.__bits)
                self._check_invariants()
            else:
                raise IllegalArgumentException("param 'bits' must be an int or a list")

    def _check_invariants(self):
        """Use assertions check to see if invariants are preserved.

        Every public method should call this in order to preserve invariants.
        Assertion errors are thrown if any of the assertions fail.
        """
        assert self.__words_in_use == 0 or self.__bits[self.__words_in_use - 1] != 0
        assert self.__words_in_use >= 0 and self.__words_in_use <= len(self.__bits)
        assert self.__words_in_use == len(self.__bits) or self.__bits[self.__words_in_use] == 0

    @property
    def is_empty(self):
        """Check to see if this BitSet is empty.

        :returns: True if empty; Otherwise, False.
        :rtype: bool
        """
        return self.__words_in_use == 0

    @property
    def length(self):
        """Get the 'logical size' of this BitSet.

        This is the index of the highest set bit in the BitSet plus one.

        :returns: The logical size of this BitSet or zero if this instance
        contains no bits.
        :rtype: int
        """
        if self.__words_in_use == 0:
            return 0

        if not self.__bits:
            self.__words_in_use = 0
            return self.__words_in_use

        positions = number_of_trailing_zeros(self.__bits[self.__words_in_use - 1])
        return BITS_PER_WORD * (self.__words_in_use - 1) + (BITS_PER_WORD - positions)

    @property
    def size(self):
        """Get the number of bits of space actually in use by this BitSet.

        :returns: The maximum element in the set is the size minus the first
        element.
        :rtype: int
        """
        return len(self.__bits) * BITS_PER_WORD

    def recalculate_words_in_use(self):
        """Set the internal word count field to the logical size in words.

        WARNING: This method assumes that the number of words actually in
        use is less than or equal to the current value of the words in use
        field!!!
        """
        i = self.__words_in_use - 1
        while i >= 0:
            i = i - 1
            if self.__bits[i] != 0:
                break
        self.__words_in_use = i + 1

    def _ensure_capacity(self, last_elt):
        """Ensure that this BitSet can hold enough words.

        :param int last_elt: The minimum acceptable number of words.
        """
        if last_elt >= len(self.__bits):
            bit_list = [None] * (last_elt + 1)
            bits = self.__bits
            if bits is None or not isinstance(bits, list):
                bits = list()
            bit_list = bits + bit_list
            self.__bits = bit_list
            self.__size_is_sticky = False

    def _expand_to(self, word_idx):
        """Ensure this BitSet can accomodate a given word index.

        This will temporarily violate invariants. The caller must restore the
        invariants before returning to the caller, possibly using
        _recalculate_words_in_use().
        :param int word_idx: The index to be accomodated.
        """
        required = word_idx + 1
        if self.__words_in_use < required:
            self._ensure_capacity(required)
            self.__words_in_use = required

    def _trim_to_size(self):
        """Attempt to reduce internal storage used for the bits.

        Calling this method may, but is not required to, affect the value
        returned by a subsequent call to the size property.
        """
        if self.__words_in_use != len(self.__bits):
            bits = self.__bits
            if bits is None or not isinstance(bits, list):
                bits = list()

            copy = bits[0:self.__words_in_use]
            self.__bits = copy
            self._check_invariants()

    def get_words_in_use(self):
        """Get the number of words in use.

        :returns: The number of words in use.
        :rtype: int
        """
        return self.__words_in_use

    def get_bits(self):
        """Get the internal bit list.

        :returns: The internal bit list.
        :rtype: list
        """
        return self.__bits

    @property
    def cardinality(self):
        """Get the number of bits set to True in this BitSet.

        :returns: The number of bits set True.
        :rtype: int
        """
        card = 0
        i = len(self.__bits) - 1
        while i >= 0:
            i -= 1
            bg_a = self.__bits[i]
            # Take care of common cases.
            if bg_a == 0:
                continue

            if bg_a == -1:
                card += 64
                continue

            # Successively collapse alternating bit groups into a sum.
            bg_a = ((bg_a >> 1) & 0x5555555555555555) + (bg_a & 0x5555555555555555)
            bg_a = ((bg_a >> 2) & 0x3333333333333333) + (bg_a & 0x3333333333333333)
            bg_b = (bg_a >> 32) + bg_a
            bg_b = ((bg_b >> 4) & 0x0f0f0f0f) + (bg_b & 0x0f0f0f0f)
            bg_b = ((bg_b >> 8) & 0x00ff00ff) + (bg_b & 0x00ff00ff)
            card += ((bg_b >> 16) & 0x0000ffff) + (bg_b & 0x0000ffff)
        return card

    def bs_and(self, b_set):
        """Perform a logical AND of this BitSet with the specified BitSet.

        This BitSet is modified so that each bit in it has the value True if
        (and only if) it both initially had the value True and the
        corresponding bit in the specified BitSet also had the value True.

        :param BitSet b_set: A BitSet. Raises ArgumentNullException if None.
        :raises: ArgumentNullException if bs is None.
        :raises: IllegalArgumentException if bs is not a BitSet.
        """
        if b_set is None:
            raise ArgumentNullException("param 'b_set' cannot be None.")

        if self == b_set:
            return

        if not isinstance(b_set, BitSet):
            raise IllegalArgumentException("param 'b_set' must be a BitSet.")

        while self.__words_in_use > b_set.get_words_in_use():
            self.__words_in_use -= 1
            self.__bits[self.__words_in_use] = 0

        for i in range(0, self.__words_in_use - 1):
            self.__bits[i] &= b_set.get_bits()[i]

        self.recalculate_words_in_use()
        self._check_invariants()

    def and_not(self, b_set):
        """Clear all bits in this BitSet matching bits in specified BitSet.

        This clears all of the bits in this BitSet whose corresponding bit is
        set in the specified BitSet.

        :param BitSet b_set: The BitSet with which to mask this instance.
        :raises: ArgumentNullException if bs is None.
        :raises: IllegalArgumentException if bs is not a BitSet.
        """
        if b_set is None:
            raise ArgumentNullException("param 'b_set' cannot be None.")

        if not isinstance(b_set, BitSet):
            raise IllegalArgumentException("param 'b_set' must be a BitSet.")

        i = min(len(self.__bits), len(b_set.get_bits()))
        while i >= 0:
            i -= 1
            self.__bits[i] &= ~b_set.get_bits()[i]

        self.recalculate_words_in_use()
        self._check_invariants()

    def bs_or(self, b_set):
        """Perform a logical OR of this BitSet with the specified BitSet.

        This BitSet is modified so that a bit in it has the value True if
        (and only if) it either already had the value True or the
        corresponding bit in the specified BitSet has the value True.

        :param BitSet b_set: A BitSet.
        :raises: ArgumentNullException if bs is None.
        :raises: IllegalArgumentException if bs is not a BitSet.
        """
        if b_set is None:
            raise ArgumentNullException("param 'b_set' cannot be None.")

        if self == b_set:
            return

        if not isinstance(b_set, BitSet):
            raise IllegalArgumentException("param 'b_set' must be a BitSet.")

        words_in_common = min(self.__words_in_use, b_set.get_words_in_use())
        if self.__words_in_use < b_set.get_words_in_use():
            self._ensure_capacity(b_set.get_words_in_use())
            self.__words_in_use = b_set.get_words_in_use()

        for i in range(0, words_in_common - 1):
            self.__bits[i] |= b_set.get_bits()[i]

        if words_in_common < b_set.get_words_in_use():
            self.__bits = self.__bits[0:self.__words_in_use - words_in_common]

        self._check_invariants()

    def x_or(self, b_set):
        """Perform a logical XOR of this BitSet with the specified BitSet.

        This BitSet is modified so that the bits in it have the value True if
        (and only if) one of the following statements hold true:
        - The bit initially has the value True, and the corresponding bit in
        the specified BitSet has the value False.
        - The bit initially has the value False, and the corresponding bit in
        the specified BitSet has the value True.

        :param BitSet b_set: A BitSet.
        :raises: ArgumentNullException if bs is None.
        :raises: IllegalArgumentException if bs is not a BitSet.
        """
        if b_set is None:
            raise ArgumentNullException("param 'b_set' cannot be None.")

        if not isinstance(b_set, BitSet):
            raise IllegalArgumentException("param 'b_set' must be a BitSet.")

        # Calculate how many words which have in common with the other BitSet.
        words_in_common = min(self.__words_in_use, b_set.get_words_in_use())
        if self.__words_in_use < b_set.get_words_in_use():
            self._ensure_capacity(b_set.get_words_in_use())
            self.__words_in_use = b_set.get_words_in_use()

        # Perform logical XOR on words in common.
        for i in range(0, words_in_common - 1):
            self.__bits[i] ^= b_set.get_bits()[i]

        # Copy any remaining words.
        if words_in_common < b_set.get_words_in_use():
            self.__bits = self.__bits[0:b_set.get_words_in_use() - words_in_common]

        self.recalculate_words_in_use()
        self._check_invariants()

    def clear(self, pos=None):
        """Clear the bit at the specified position.

        This sets the bit a the specified position (index) to False, or clears
        the entire BitSet if no value given.

        :param int pos: The index of the bit to be cleared. If None or less
        than one, clears the entire BitSet.
        :raises: IndexError if pos is greater than the last index.
        """
        if pos is None or pos < 1:
            for i in range(0, len(self.__bits) - 1):
                self.__bits[i] = 0
            self.__words_in_use = 0
        else:
            if pos > len(self.__bits) - 1:
                msg = "Param 'pos' cannot be greater than the last index."
                raise IndexError(msg)

            offset = word_index(pos)
            if offset >= self.__words_in_use:
                return

            self.__bits[offset] &= ~(1 << pos)
            self.recalculate_words_in_use()
            self._check_invariants()

    def clear_from_to(self, from_index, to_index):
        """Clear the bits from the specified index to the specified index.

        This sets the bits from the specified 'from_index' (inclusive) to the
        specified 'to_index' (exclusive) to False.

        :param int from_index: The starting index.
        :param int to_index: The ending index.
        :raises: ArgumentNullException if either parameter is None.
        :raises: IllegalArgumentException if either parameter is not an int.
        :raises: IndexError if either parameter is less than zero.
        """
        check_range(from_index, to_index)
        if from_index == to_index:
            return

        start_word_idx = word_index(from_index)
        if start_word_idx >= self.__words_in_use:
            return

        end_word_idx = word_index(to_index - 1)
        if end_word_idx >= self.__words_in_use:
            to_index = self.length
            end_word_idx = self.__words_in_use - 1

        first_word_mask = LONG_MASK << from_index
        last_word_mask = LONG_MASK >> -to_index
        if start_word_idx == end_word_idx:
            # Case 1: Single word.
            self.__bits[start_word_idx] &= ~(first_word_mask & last_word_mask)
        else:
            # Case 2: Multiple words.
            # Handle first word.
            self.__bits[start_word_idx] &= ~first_word_mask

            # Handle intermediate words, if any.
            for i in range(start_word_idx + 1, end_word_idx):
                self.__bits[i] = 0

            # Handle last word.
            self.__bits[end_word_idx] &= ~last_word_mask

        self.recalculate_words_in_use()
        self._check_invariants()

    def do_check_invariants(self):
        """Public method for performing invariant checks.

        Every public method MUST preserve invariants. This method checks to
        see if this is true using assertions. Assertion errors are thrown
        if any of the assertions fail.
        """
        self._check_invariants()

    def clone(self):
        """Create a new BitSet that is a copy of this current instance.

        :returns: A new BitSet that is a copy of this instance.
        :rtype: BitSet
        """
        if self.__size_is_sticky:
            self._trim_to_size()

        try:
            return from_word_array(self.__bits)
        except IndexError:
            return None

    def equals(self, obj):
        """Determine whether the specified object is equal to this BitSet.

        :param object obj: The object to compare with the current BitSet.
        Generally, this method should be used to check against other BitSet
        instances.
        :returns: True if equal; Otherwise, False.
        :rtype: bool
        """
        if obj is None:
            return False

        if not isinstance(obj, BitSet):
            return False

        self._check_invariants()
        obj.do_check_invariants()
        if self.__words_in_use != obj.get_words_in_use():
            return False

        result = True
        for i in range(0, self.__words_in_use - 1):
            if self.__bits[i] != obj.get_bits()[i]:
                result = False
                break

        return result

    def flip(self, index):
        """Set the bit at the specified index to the compliment of the value.

        :param int index: The index of the bit to flip.
        :raises: IllegalArgumentException if index is not an int.
        :raises: IndexError if index is less than zero.
        """
        if not isinstance(index, int):
            raise IllegalArgumentException("index must be a valid integer.")

        if index < 0:
            raise IndexError("index cannot be less than zero.")

        offset = word_index(index)
        self._expand_to(offset)
        self.__bits[offset] ^= 1 << index
        self.recalculate_words_in_use()
        self._check_invariants()

    def flip_from_to(self, from_index, to_index):
        """Set each bit to its compliment value.

        This sets each bit from the specified "from" (inclusive) index to the
        specified "to" (exclusive) index to the compliment of its current
        value.

        :param int from_index: The starting index.
        :param int to_index: The ending index.
        :raises: ArgumentNullException if either parameter is None.
        :raises: IllegalArgumentException if either parameter is not an int.
        :raises: IndexError if either parameter is less than zero.
        """
        check_range(from_index, to_index)
        if from_index == to_index:
            return

        start_word_index = word_index(from_index)
        last_word_index = word_index(to_index - 1)
        self._expand_to(last_word_index)

        first_word_mask = LONG_MASK << from_index
        last_word_mask = LONG_MASK >> -to_index
        if start_word_index == last_word_index:
            # Case 1: single word
            self.__bits[start_word_index] ^= (first_word_mask & last_word_mask)
        else:
            # Case 2: multiple words.
            # Handle first word.
            self.__bits[start_word_index] ^= first_word_mask

            # Handle intermediate words, if any.
            for i in range(start_word_index + 1, last_word_index - 1):
                self.__bits[i] ^= LONG_MASK

            # Handle last word.
            self.__bits[last_word_index] ^= last_word_mask

        self.recalculate_words_in_use()
        self._check_invariants()

    def set_bit_raw_value(self, index, bit):
        """Set the raw bit value at the specified index.

        Avoid using this method whenever possible. Instead, use either set()
        or set_from_to() so as to preserve invariants.

        :param int index: The index at which to set the specified bit.
        :param int, bool bit: Set True or 1 to set the bit, or False or 0
        to clear the bit.
        :raises: IllegalArgumentException if index is not an int -or-
        bit parameter is not an int or a bool.
        :raises: IndexError if index parameter is less than zero.
        """
        if not isinstance(index, int):
            raise IllegalArgumentException("index must be a valid integer.")

        if index < 0 or index > len(self.__bits) - 1:
            msg = "index must be greater than zero and less than or "
            msg += "equal to the last index in the bit set."
            raise IndexError(msg)

        if isinstance(bit, int):
            if bit < 0:
                bit = 0

            if bit > 1:
                bit = 1
        elif isinstance(bit, bool):
            if bit:
                bit = 1
            else:
                bit = 0
        else:
            msg = "bit must be a number (0 or 1) or bool."
            raise IllegalArgumentException(msg)

        self.__bits[index] = bit

    def get(self, index):
        """Get the value of the bit at the specified index.

        :param int index: The index at which to get the bit value.
        :returns: True if the requested bit is set.
        :rtype: bool
        :raises: IllegalArgumentException if index is not an int.
        :raises: IndexError if index is less than zero.
        """
        if isinstance(index, int):
            raise IllegalArgumentException("index must be a valied int.")

        if index < 0:
            raise IndexError("index cannot be less than zero.")

        self._check_invariants()
        offset = word_index(index)
        return (offset < self.__words_in_use and
                (self.__bits[index] & (1 << index)) != 0)

    def get_from_to(self, from_index, to_index):
        """Get a new BitSet comprised of the specified range of bits.

        Returns a new BitSet composed of bits from this BitSet from
        the specified "from" (inclusive) index to the specified "to"
        (exclusive) index.

        :param int from_index: The starting index. This is the first bit to
        include.
        :param int to_index: The ending index. This is the index after the
        last bit to include.
        :returns: A new BitSet instance composed of the specified range of
        bits from this instance.
        :raises: ArgumentNullException if either parameter is None.
        :raises: IllegalArgumentException if either parameter is not an int.
        :raises: IndexError if either parameter is less than zero.
        """
        check_range(from_index, to_index)
        self._check_invariants()

        # If no set bits in range, then return the empty BitSet.
        this_len = self.length
        if this_len <= from_index or from_index == to_index:
            return from_word_array(list())

        # Optimize
        if to_index > this_len:
            to_index = this_len

        b_set = BitSet(to_index - from_index)
        target_words = word_index(to_index - from_index - 1) + 1
        source_index = word_index(from_index)
        aligned = (from_index & BIT_INDEX_MASK) == 0

        # Process all words but the last one.
        for i in range(0, target_words - 1):
            source_index += 1
            if aligned:
                set_bit = self.__bits[source_index]
            else:
                set_bit = (self.__bits[source_index] >> from_index |
                           self.__bits[source_index + 1] << -from_index)
            b_set.set_bit_raw_value(i, set_bit)

        # Process last word.
        last_word_mask = LONG_MASK >> -to_index
        start_of_mask = ((to_index - 1) & BIT_INDEX_MASK) < (from_index & BIT_INDEX_MASK)
        if start_of_mask:
            set_bit = ((self.__bits[source_index] >> from_index) |
                       (self.__bits[source_index + 1]) & last_word_mask) << -from_index
        else:
            set_bit = (self.__bits[source_index] & last_word_mask) >> from_index

        b_set.set_bit_raw_value(target_words - 1, set_bit)
        b_set.do_check_invariants()
        b_set.recalculate_words_in_use()
        return b_set

    def set(self, index):
        """Set the bit at the specified index True.

        :param int index: The index at which to set the bit.
        :raises: IllegalArgumentException if index is not an int.
        :raises: IndexError if index is less than zero.
        """
        if not isinstance(index, int):
            raise IllegalArgumentException("index must be a valid integer.")

        if index < 0:
            raise IndexError("index cannot be less than zero.")

        offset = word_index(index)
        self._expand_to(offset)
        self.__bits[offset] |= (1 << index)  # Restore invariants.
        self._check_invariants()

    def set_value(self, index, value):
        """Set the bit at the specified index to the specified value.

        :param int index: The index at which to set the bit.
        :param bool value: The value to set.
        :raises: IllegalArgumentException if index is not an int.
        :raises: IndexError if index is less than zero.
        """
        if value:
            self.set(index)
        else:
            self.clear(index)

    def set_from_to(self, from_index, to_index):
        """Set bits in the specified range.

        Sets the bits from the specified "from" index (inclusive) to the
        specified "to" index (exclusive) to True.

        :param int from_index: The starting index. This is the first bit to
        set.
        :param int to_index: The ending index. This is the index after the
        last bit to set.
        :raises: ArgumentNullException if either parameter is None.
        :raises: IllegalArgumentException if either parameter is not an int.
        :raises: IndexError if either parameter is less than zero.
        """
        check_range(from_index, to_index)
        if from_index == to_index:
            return

        start_word_index = word_index(from_index)
        end_word_index = word_index(to_index - 1)
        self._expand_to(end_word_index)

        first_word_mask = LONG_MASK << from_index
        last_word_mask = LONG_MASK >> -to_index
        if start_word_index == end_word_index:
            # Case 1: single word
            self.__bits[start_word_index] |= (first_word_mask & last_word_mask)
        else:
            # Case 2: Multiple words.
            # Handle first word.
            self.__bits[start_word_index] |= first_word_mask

            # Handle intermediate words, if any.
            for i in range(start_word_index + 1, end_word_index - 1):
                self.__bits[i] = LONG_MASK

            # Handle last word (restores invariants).
            self.__bits[end_word_index] |= last_word_mask

        self._check_invariants()

    def set_value_from_to(self, from_index, to_index, value):
        """Set the bits in the specified range.

        Sets the bits from the specified "from" index (inclusive) to the
        specified "to" index (exclusive) to the specified value.

        :param int from_index: The starting index. This is the first bit to
        set.
        :param int to_index: The ending index. This is the index after the
        last bit to set.
        :param bool value: The value to set.
        :raises: ArgumentNullException if either parameter is None.
        :raises: IllegalArgumentException if either parameter is not an int.
        :raises: IndexError if either parameter is less than zero.
        """
        if value:
            self.set_from_to(from_index, to_index)
        else:
            self.clear_from_to(from_index, to_index)

    def get_hash_code(self):
        """Get a hash code value for this BitSet.

        The hash code depends only on which bits are set within this instance.

        :returns: The hash code value for this BitSet.
        :rtype: int
        """
        h_code = 1234
        i = len(self.__bits)
        while i >= 0:
            i -= 1
            h_code ^= self.__bits[i] * (i + 1)

        return (h_code >> 32) ^ h_code

    def intersects(self, b_set):
        """Check to see if this BitSet intersects another.

        Determines whether or not the specified BitSet has any bits set to True
        that are also set to True in this BitSet.

        :param BitSet b_set: The BitSet to intersect with.
        :returns: True if this instance intersects with the specified BitSet.
        :rtype: bool
        """
        if b_set is None:
            return False

        if not isinstance(b_set, BitSet):
            return False

        good_bits = False
        i = min(len(self.__bits), len(b_set.get_bits()))
        while i >= 0:
            i -= 1
            if (self.__bits[i] & b_set.get_bits()[i]) != 0:
                good_bits = True
                break
        return good_bits

    def next_clear_bit(self, from_index):
        """Get the index of the first bit that is set to False.

        This will be the bit that is False on or after the specified starting
        index.

        :param int from_index: The index to start checking from (inclusive).
        :returns: The index of the next clear bit; Otherwise, -1.
        :rtype: int
        :raises: IndexError if from_index is less than zero.
        """
        if from_index < 0:
            raise IndexError("'from' index cannot be less than zero.")

        self._check_invariants()
        offset = word_index(from_index)
        if offset >= self.__words_in_use:
            return from_index

        word = ~self.__bits[offset] & (LONG_MASK << from_index)
        while True:
            if word != 0:
                result = (offset * BITS_PER_WORD) + number_of_trailing_zeros(word)
                break

            offset += 1
            if offset == self.__words_in_use:
                result = self.__words_in_use * BITS_PER_WORD
                break

            word = ~self.__bits[offset]

        return result

    def next_set_bit(self, from_index):
        """Get the index of the first bit that is set True.

        Returns the first True bit that occurs on or after the specified
        starting index.

        :param int from_index: The index to start checking from (inclusive).
        :returns: The index of the next set bit after the specified index.
        If no such bit exists, then returns -1.
        :rtype: int
        :raises: IndexError if from_index is less than zero.
        """
        if from_index < 0:
            raise IndexError("'from' index cannot be less than zero.")

        self._check_invariants()
        offset = word_index(from_index)
        if offset >= self.__words_in_use:
            return -1

        result = -1
        word = self.__bits[offset] & (LONG_MASK << from_index)
        while True:
            if word != 0:
                result = (offset * BITS_PER_WORD) + number_of_trailing_zeros(word)
                break

            offset += 1
            if offset == self.__words_in_use:
                break

            word = self.__bits[offset]

        return result

    def previous_set_bit(self, from_index):
        """Get the index of the nearest bit that is True.

        Returns the index of the nearest bit that is set to True that occurs
        on or before the specified starting index.

        :param int from_index: The index to start checking from (inclusive).
        :returns: The index of the previous set bit, or -1 if there is no
        such bit or if from_index is set to -1.
        :rtype: int
        :raises: IndexError if from_index is less than zero.
        """
        if from_index < 0:
            if from_index == -1:
                return -1
            raise IndexError("'from' index cannot be less than zero.")

        self._check_invariants()
        offset = word_index(from_index)
        if offset >= self.__words_in_use:
            return self.length - 1

        result = -1
        word = self.__bits[offset] & (LONG_MASK >> -(from_index + 1))
        while True:
            if word != 0:
                result = (offset + 1) * BITS_PER_WORD - 1 - number_of_trailing_zeros(word)
                break

            offset -= 1
            if offset == 0:
                break

            word = self.__bits[offset]
        return result

    def previous_clear_bit(self, from_index):
        """Get the index of the nearest bit set False.

        Returns the index of the nearest bit that is set to False that occurs
        on or before the specified starting index.

        :param int from_index: The index to start checking from (inclusive).
        :returns: The index of the previous clear bit or -1 if there is no
        such bit or from_index is -1.
        :rtype: int
        :raises: IndexError if from_index is less than zero.
        """
        if from_index < 0:
            if from_index == -1:
                return -1
            raise IndexError("'from' index cannot be less than zero.")

        self._check_invariants()
        offset = word_index(from_index)
        if offset >= self.__words_in_use:
            return from_index

        result = -1
        word = ~self.__bits[offset] & (LONG_MASK >> -(from_index + 1))
        while True:
            if word != 0:
                result = (offset + 1) * BITS_PER_WORD - 1 - number_of_trailing_zeros(word)
                break

            offset -= 1
            if offset == 0:
                break

            word = ~self.__bits[offset]

        return result

    def contains_all(self, other_bs):
        """Check to see if this BitSet contains all the same bits as another.

        This method is used for efficiency. It checks to see if this instance
        contains all the same bits as the specified BitSet.

        :param BitSet other_bs: The BitSet to check.
        :returns: True if the specified BitSet contains all the same bits.
        :rtype: bool
        """
        if other_bs is None:
            return False

        result = True
        for i in range(0, len(other_bs.get_bits()) - 1):
            bit_masked = self.__bits[i] & other_bs.get_bits()[i]
            if bit_masked != other_bs.get_bits()[i]:
                result = False
                break
        return result

    def to_string(self):
        """Get a string representation of this BitSet.

        For every index for which this BitSet contains a bit in the set state,
        the decimal representation of that index is included in the result.
        Such indices are listed in order from lowest to highest, separated by
        a ", " (a comma and a space) and surrounded by braces, resulting in
        the usual mathematical notation for a set of integers.

        :returns: A string that represents the current BitSet.
        :rtype: str
        """
        string_builder = "{"
        first = True
        for i in range(0, len(self.__bits) - 1):
            bit = 1
            word = self.__bits[i]
            if word == 0:
                continue

            for j in range(0, 63):
                if (word & bit) != 0:
                    if not first:
                        string_builder += ", "
                    string_builder += str(64 * i * j)
                    first = False
            bit <<= 1
        string_builder += "}"
        return string_builder

    def to_bit_list(self):
        """Return a new list of bits containing all bits in this BitSet.

        :returns: A list of bits containing little-endian representation
        of all bits in this BitSet.
        :rtype: list
        """
        if self.__bits is None or not isinstance(self.__bits, list):
            return list()
        return self.__bits

    @staticmethod
    def value_of(words):
        """Get a new BitSet containing all the bits in the specified list.

        :param list words: The list of bits to construct a BitSet from. If
        None, then this function will return None.
        :returns: A new BitSet containing the specified list of bits.
        :rtype: BitSet
        :raises: IllegalArgumentException if not a list.
        """
        if words is None:
            return None

        if not isinstance(words, list):
            raise IllegalArgumentException("param 'words' must be an array of bits.")

        num = len(words)
        while num > 0 and words[num - 1] == 0:
            num -= 1

        words_copy = list(words)
        return BitSet(words_copy)
