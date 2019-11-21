from Bitstream import BitStream

if __name__ == '__main__':
    bts = BitStream(open("output_bits.dat", "rb"), open("input_bits.dat", "wb"))
    chars = '01000000'
    for c in chars:
        bts.writebits(ord(c), 1)

    chars = []
    while True:
        x = bts.readbits(8)
        if not bts.read:  # End-of-file?
            break
        chars.append(chr(x))

    print(''.join(chars))

    print(bts._readbit(),bts._readbit(),bts._readbit(),bts._readbit()
    ,bts._readbit(),bts._readbit(),bts._readbit(),bts._readbit())

