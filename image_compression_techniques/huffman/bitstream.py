class OutputBitStream(object):
    """
    A class to write the encoded file

    """

    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename, 'wb')
        self.bytes_written = 0
        self.buffer = []

    def write_bit(self, value):
        self.write_bits([value])

    def write_bits(self, values):
        self.buffer += values
        while len(self.buffer) >= 8:
            self._save_byte()

    def flush_buffer(self):

        if len(self.buffer) > 0:
            self.buffer += [0] * (8 - len(self.buffer))
            self._save_byte()
        assert(len(self.buffer) == 0)

    def _save_byte(self):
        bits = self.buffer[:8]
        self.buffer[:] = self.buffer[8:]

        byte_value = from_binary_list(bits)
        self.file.write(bytes([byte_value]))
        self.bytes_written += 1

    def close(self):
        self.flush_buffer()
        self.file.close()


class InputBitStream(object):
    """
    A class that reads the encoded file for decoding
    """

    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename, 'rb')
        self.bytes_read = 0
        self.buffer = []

    def read_bit(self):
        return self.read_bits(1)[0]

    def read_bits(self, count):
        while len(self.buffer) < count:
            self._load_byte()
        result = self.buffer[:count]
        self.buffer[:] = self.buffer[count:]
        return result

    def flush_buffer(self):
        assert(not any(self.buffer))
        self.buffer[:] = []

    def _load_byte(self):
        value = ord(self.file.read(1))
        self.buffer += pad_bits(to_binary_list(value), 8)
        self.bytes_read += 1

    def close(self):
        self.file.close()


def to_binary_list(n):
    """ Convert an integer to a list of bits """
    if n <= 1:
        return [n]
    else:
        return to_binary_list(n >> 1) + [n & 1]


def from_binary_list(bits):
    """ Convert a list of bits to an integer """
    result = 0
    for bit in bits:
        result = (result << 1) | bit
    return result


def pad_bits(bits, digit_length):
    """ Pad list of bits with zeros to reach digit length """
    assert(digit_length >= len(bits))
    return ([0] * (digit_length - len(bits)) + bits)
