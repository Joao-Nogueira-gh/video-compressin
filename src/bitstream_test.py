from Bitstream import BitStream

if __name__ == '__main__':


    bts = BitStream("../res/output_bits.dat", "WRITE")
    
    # Writing a few random bits to a file
    chars = '01010101'
    for c in chars:
        bts.writebits(ord(c), 1)

    # Writing 255 using 9 bits (first will be left as 0)
    bts.write_n_bits(255, 9)
    
    # Closing file - mandatory if we wish to perform different operations
    bts.close()


    # # # # # # # # # # # # # # # # # # # # # # # # # # 


    bts = BitStream("../res/output_bits.dat", "READ")

    # Reading 8 chars, that should result in the same random bits as before
    chars = []
    for i in range(0, 8):
        chars.append(str(bts._readbit()))

    print(''.join(chars))

    # Reading the value stored in the NEXT 9 bits (should be the 255 we wrote)
    print(bts.read_n_bits(9))

    # Closing file - not mandatory, but good practice
    bts.close()