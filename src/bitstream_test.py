## @brief
# Module for testing of the Bitstream class
#

from Bitstream import BitStream
import sys

if __name__ == '__main__':
    if len(sys.argv)==4:
        chars=sys.argv[1]
        number=int(sys.argv[2])
        nbits=int(sys.argv[3])
    else:
        chars = '0010101'
        number=49
        nbits=6

    bts = BitStream("../res/output_bits.dat", "WRITE")

    # Writing a few random bits to a file

    charlength=len(chars)

    print('Writing',chars,'to file')
    
    bts.writebits(int(chars,2), charlength)

    # Writing a number with x bits

    print('Writing',number,'with',nbits,'bits')

    bts.write_n_bits(number, nbits)
    
    # Closing file - mandatory if we wish to perform different operations
    bts.close()


    # # # # # # # # # # # # # # # # # # # # # # # # # # 


    bts = BitStream("../res/output_bits.dat", "READ")

    # Reading x=len(chars) characters, that should result in the same bits as before
    chars = []
    for i in range(0, charlength):
        chars.append(str(bts._readbit()))

    print('Read from file: ',''.join(chars))

    # Reading the value stored in the NEXT x bits (should be the value we wrote)
    print('Read from file: ',bts.read_n_bits(nbits))

    # Closing file
    bts.close()

    #Showing binary content written on file
    f=open("../res/output_bits.dat", "rb")
    print('Actual file content-> ',f.read())