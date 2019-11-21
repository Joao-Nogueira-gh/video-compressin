## BitStream class
# Supported methods:
#   Writing one bit
#   Reading one bit
#   Writing n bits
#   Reading n bits
## It is assumed that a user can never pass the same file as input and output

class BitStream:
    def __init__(self, fin, fout):
        self.write_accumulator = 0
        self.write_bcount = 0
        self.out = fout
 
        self.input = fin
        self.read_accumulator = 0
        self.read_bcount = 0
        self.read = 0

    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()
 
    def __del__(self):
        try:
            self.flush()
        except ValueError:   # I/O operation on closed file.
            pass
 
    def _writebit(self, bit):
        if self.write_bcount == 8:
            self.flush()
        if bit > 0:
            self.write_accumulator |= 1 << 7-self.write_bcount
        self.write_bcount += 1
 
    def writebits(self, bits, n):
        while n > 0:
            self._writebit(bits & 1 << n-1)
            n -= 1

    def _readbit(self):
        if not self.read_bcount:
            a = self.input.read(1)
            if a:
                self.read_accumulator = ord(a)
            self.read_bcount = 8
            self.read = len(a)
        rv = (self.read_accumulator & (1 << self.read_bcount-1)) >> self.read_bcount-1
        self.read_bcount -= 1
        return rv
 
    def readbits(self, n):
        v = 0
        while n > 0:
            v = (v << 1) | self._readbit()
            n -= 1
        return v

    def flush(self):
        self.out.write(bytearray([self.write_accumulator]))
        self.write_accumulator = 0
        self.write_bcount = 0

    def set_infile(self, fin):
        self.input.close()
        self.input = fin
        self.read_accumulator = 0
        self.read_bcount = 0
        self.read = 0

    def set_outfile(self, fout):
        self.out.close()
        self.write_accumulator = 0
        self.write_bcount = 0
        self.out = fout