from testing import BitReader, BitWriter

## BitStream class
# Supported methods:
#   Writing one bit
#   Reading one bit
#   Writing n bits
#   Reading n bits


class BitStream:
    def __init__(self, infile, outfile):
        self.reader = BitReader(infile)
        self.writer = BitWriter(outfile)


    def write_bit(self, bit):
        self.writer._writebit(bit)


    def read_bit(self):
        bit = self.reader._readbit()
        return bit
         

    def write_bits(self, bits, count):
        self.writer.writebits(bits, count)


    def read_bits(self, count):
        bits = self.reader.readbits(count)
        return bits


if __name__ == '__main__':
    bts = BitStream(open("bitio_test.dat", 'rb'), open("output_bits.dat", 'wb'))
    chars = '01000000'
    for c in chars:
        bts.write_bits(ord(c), 1)

    chars = []
    while True:
        x = bts.read_bits(7)
        if not bts.reader.read:  # End-of-file?
            break
        chars.append(chr(x))
    print(''.join(chars))