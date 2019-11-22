from Bitstream import BitStream

if __name__ == '__main__':
    bts = BitStream("input_bits.dat", "WRITE")
    chars = '01000000'
    for c in chars:
        bts.writebits(ord(c), 1)

    bts.write_n_bits(128, 8)
    
    bts.close()

    bts = BitStream("input_bits.dat", "READ")

    chars = []
    for i in range(0, 8):
        chars.append(str(bts._readbit()))

    print(''.join(chars))


    # bts.write_n_bits(value, n_bits) -> write value using n_bits
    # bts.read_n_bits(n_bits) -> read value corresponding to n_bits

    print(bts._readbit(),bts._readbit(),bts._readbit(),bts._readbit()
    ,bts._readbit(),bts._readbit(),bts._readbit(),bts._readbit())

