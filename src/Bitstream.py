
WRITE = 0
READ = 1

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


    def __init__(self, file_name, mode):
        ## Initialization function
        # \param[in] file_name Name of the file that is going to be manipulated
        # \param[in] mode Mode of manipulation (write/read)
        if mode == "WRITE":
            self.mode = WRITE
            self.out = open(file_name, "wb")
    
        elif mode == "READ":
            self.mode = READ
            self.input = open(file_name, "rb")
            self.read = 0

        else:
            print("ERROR: Unsupported mode")
            exit(1)
    
        self.accumulator = 0
        self.bcount = 0


    ## Write a single bit to self.file_name
    # \param[in] value of the bit to be written to a file
    def _writebit(self, bit):
        if self.mode != WRITE:
            print("ERROR: Unsupported operation given the current mode (READ)")
            exit(1)

        if self.bcount == 8:
            self.flush()
        if bit > 0:
            self.accumulator |= 1 << 7-self.bcount
        self.bcount += 1
 

    ## Read a single bit from file
    # \param[out] value of the bit read
    def _readbit(self):
        if self.mode != READ:
            print("ERROR: Unsupported operation given the current mode (WRITE)")
            exit(1)

        if not self.bcount:
            a = self.input.read(1)
            if a:
                self.accumulator = ord(a)
            self.bcount = 8
            self.read = len(a)
        rv = (self.accumulator & (1 << self.bcount-1)) >> self.bcount-1
        self.bcount -= 1
        return rv


    ## Write N bits to file
    # \param[in] bits to be written to a file
    # \param[in] number of bits to be written
    def writebits(self, bits, n):
        if self.mode != WRITE:
            print("ERROR: Unsupported operation given the current mode (READ)")
            exit(1)

        while n > 0:
            self._writebit(bits & 1 << n-1)
            n -= 1


    ## Read N bits from a file
    # \param[in] number of bits to be read from a file
    # \param[out] values of bits read from file
    def readbits(self, n):
        if self.mode != READ:
            print("ERROR: Unsupported operation given the current mode (WRITE)")
            exit(1)
        v = 0
        while n > 0:
            v = (v << 1) | self._readbit()
            n -= 1
        return v


    ## Write a given value using a certain number of bits to a file
    # \param[in] value Value that is being written to a file
    # \param[in] nbits Number of bits being used to write value
    # Throws an error if value cannot be written using only nbits
    def write_n_bits(self, value, nbits):
        if self.mode != WRITE:
            print("ERROR: Unsupported operation given the current mode (READ)")
            exit(1)
        b = str(bin(value))[2:]
        if nbits < len(b):
            print("Error: Cannot write "+str(value)+" with as little as " + str(nbits) + " bits")
            exit(0)

        for i in range(nbits-1, -1, -1): # -1 -1, tem bue -1s idk achei piada xd
            self._writebit(ord(b[i]))


    ## Read the value corresponding to the next N bits of the file
    # \param[in] nbits Number of bits that are going to be read from file
    def read_n_bits(self, nbits):
        if self.mode != READ:
            print("ERROR: Unsupported operation given the current mode (WRITE)")
            exit(1)
        bits = self.readbits(nbits)
        num = int(bits, 2)
        return num


    ## Auxiliary function to the write operations
    # Writes the packaged bits to a file
    def flush(self):
        if self.mode != WRITE:
            print("ERROR: Unsupported operation given the current mode")
            exit(1)

        self.out.write(bytearray([self.accumulator]))
        self.accumulator = 0
        self.bcount = 0


    ## Close files
    # Closes the file from where Bitstream is reading if the mode is READ
    # Closes the file to where Bitstream is writing if the mode is WRITE
    def close(self):
        if self.mode == "WRITE":
            self.out.close()
        elif self.mode == "READ":
            self.input.close()