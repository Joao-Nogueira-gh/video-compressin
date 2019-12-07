## \class BitStream
# Adaptation of already existing code to: support a single mode of file manipulation at a time,
# write one bit to a file, read one bit from a file, write N bits to a file, read N bits from a
# file, write value M using N bits to a file, read N bits from a file and the value these
# correspond to.<br>
# Every function aborts the program if it requires a different mode. For instance, if the function
# _writebit() is called with Bitstream on READ mode. 
# \author Tiago Melo 89005
# \author João Nogueira 89262 
class BitStream:
    def __init__(self, f, mode):
        ## Initialization function
        # \param[in] file_name Name of the file that is going to be manipulated
        # \param[in] mode Mode of manipulation (write/read)
        self.mode = mode

        if mode == "READ":
            self.input = open(f, "rb")
        elif mode == "WRITE":
            self.out = open(f, "wb")

        self.write_accumulator = 0
        self.write_bcount = 0

        self.read_accumulator = 0
        self.read_bcount = 0
        self.read = 0

    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.mode == "WRITE":
            self.flush()
 
    def __del__(self):
        if self.mode == "WRITE":
            try:
                self.flush()
            except ValueError:   # I/O operation on closed file.
                pass


    ## Write a single bit to self.file_name
    # \param[in] value of the bit to be written to a file
    def _writebit(self, bit):
        if self.write_bcount == 8:
            self.flush()
        if bit > 0:
            self.write_accumulator |= 1 << 7-self.write_bcount
        self.write_bcount += 1


    ## Read a single bit from file
    # \param[out] value of the bit read 
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


    ## Write N bits to file
    # \param[in] bits to be written to a file
    # \param[in] number of bits to be written
    def writebits(self, bits, n):
        while n > 0:
            self._writebit(bits & 1 << n-1)
            n -= 1
 

    ## Read N bits from a file
    # \param[in] number of bits to be read from a file
    # \param[out] values of bits read from file
    def readbits(self, n):
        chars = []
        for i in range(0, 8):
            chars.append(str(self._readbit()))

        return ''.join(chars)


    ## Write a given value using a certain number of bits to a file
    # \param[in] value Value that is being written to a file
    # \param[in] nbits Number of bits being used to write value
    # Throws an error if value cannot be written using only nbits
    def write_n_bits(self, value, nbits):
        if self.mode != "WRITE":
            print("ERROR: Unsupported operation given the current mode (READ)")
            exit(1)
        b = str(bin(value))[2:]
        if nbits < len(b):
            print("Error: Cannot write "+str(value)+" with as little as " + str(nbits) + " bits")
            exit(0)

        for i in range(nbits-1, -1, -1): # -1 -1, tem bue -1s idk achei piada xd
            if i >= len(b):
                self._writebit(0)
            else:
                self._writebit(ord(b[i]))


    ## Read the value corresponding to the next N bits of the file
    # \param[in] nbits Number of bits that are going to be read from file
    def read_n_bits(self, nbits):
        if self.mode != "READ":
            print("ERROR: Unsupported operation given the current mode (WRITE)")
            exit(1)
        v = 0
        while nbits > 0:
            v = (v << 1) | self._readbit()
            nbits -= 1
        return v


    ## Auxiliary function to the write operations
    # Writes the packaged bits to a file
    def flush(self):
        self.out.write(bytearray([self.write_accumulator]))
        self.write_accumulator = 0
        self.write_bcount = 0


    ## Close files
    # Closes the file from where Bitstream is reading if the mode is READ
    # Closes the file to where Bitstream is writing if the mode is WRITE
    # Importantly, it deletes this object which, in turn, flushes any bits left in buffer
    def close(self):
        self.__del__()

        if self.mode == "WRITE":
            self.out.close()
        elif self.mode == "READ":
            self.input.close()
    
    def writeTxt(self,txt):
        txt=bytearray(txt, encoding='utf-8')
        self.out.write(txt)
    def readTxt(self,txt):
        txt=txt.decode('utf-8')
