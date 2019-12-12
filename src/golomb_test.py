from Golomb import *

def main():
    g=Golomb(4)
    x=g.encode(9)
    #print(x)
    exit(0)
    f=open("../res/testFile.txt","r")
    o=open("../res/encodedTestFile.txt","w")
    a=open("../res/decodedTestFile.txt","w")
    c=0
    for line in f:
        campos=line.rstrip().split(";")
        for x in campos:
            r=g.encode(x)
            o.write(r+";")
        o.write("\n")
    f.close()
    o.close()
    o=open("../res/encodedTestFile.txt","r")
    for line in o:
        campos=line.rstrip().split(";")
        for x in campos:
            if x=='':
                continue
            r=g.decode(x)
            a.write(str(r)+";")
        a.write("\n")
    a.close()
    o.close()
    print('success')

if __name__ == "__main__":
    main()