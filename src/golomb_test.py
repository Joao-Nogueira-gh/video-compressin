from Golomb import *

def main():
    g=Golomb(5)
    a=g.encode(15)
    g.decode(a)
    b=g.encode(20)
    g.decode(b)
    c=g.encode(38)
    g.decode(c)

if __name__ == "__main__":
    main()