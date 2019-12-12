from Bitstream import BitStream
from Golomb import *

def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

if __name__ == '__main__':

    header='ENCODED YUV4MPEG2 W1280 H720 F50:1 Ip A1:1 C444 4'
    bts = BitStream("testing", "WRITE")

    l=[]
    n1=n="{0:b}".format(5)
    n2=n="{0:b}".format(-5)
    print(n1,n2)
    l.append(n1)
    l.append(n2)
    l.append('1111111111111111111111111111111101')
    comp=len(header)
    print(comp)
    bts.write_n_bits(comp,8)
    bts.writeTxt(header)

    for i in range(0,len(l)):
        x=l[i]
        bts.writebits(int(x,2), len(x))
        print('ASDHSAJF',len(x))

    bts.close()

    ####################

    bts = BitStream("testing", "READ")

    lenh=bts.read_n_bits(8)
    print(lenh)

    chars=[]
    for i in range(0,lenh*8):
        chars.append(str(bts._readbit()))

    res=''.join(chars)
    #print(res)
    a=decode_binary_string(res)
    print(a)

    g=Golomb(4)

    for x in l:
        chars = []
        for i in range(0, len(x)):
            chars.append(str(bts._readbit()))

        res=''.join(chars)
        print(res)
        print(g.decode(res))
        if res==x:
            print('yoo')
        else:
            print(res,x)

    bts.close()

    r1=g.encode(5)
    r2=g.encode(-5)
    print(r1,r2)
    r3=g.decode(r1)
    r4=g.decode(r2)
    print(r3,r4)

    # bts = BitStream("testing", "WRITE")
    # bts.write_n_bits(,1)
    # bts.close()
    # bts = BitStream("testing", "READ")
    # x=bts.read_n_bits(1)
    # print(x)
    # bts.close()