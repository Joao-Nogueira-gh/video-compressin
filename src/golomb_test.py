## @brief
# Module for testing of the Golomb class
#

from Golomb import *
import sys

if __name__ == "__main__":
    if len(sys.argv)==2:
        m=int(sys.argv[1])
    else:
        m=32

    #Initializing Golomb with parameter m
    g=Golomb(m)

    #Original file, contains a few numbers, throughout 3 lines, separated by ';' 
    f=open("../res/testFile.txt","r")

    print('\nOriginal file contents:')

    #File in which we encode the original file contents
    #Writing encoded contents
    o=open("../res/encodedTestFile.txt","w")
    c=0
    for line in f:
        print(line)
        campos=line.rstrip().split(";")
        for x in campos:
            #encoding each number and adding a separator
            r=g.encode(x)
            o.write(r+";")
        o.write("\n")
    f.close()
    o.close()

    #Open encoded file
    o=open("../res/encodedTestFile.txt","r")

    #File in which we write back the decoded file contents, should be equal to original files
    a=open("../res/decodedTestFile.txt","w")

    print('\nEncoded file contents:')

    #Decode content and write back in file

    for line in o:
        print(line)
        campos=line.rstrip().split(";")
        for x in campos:
            if x=='':
                continue
            r=g.decode(x)
            a.write(str(r)+";")
        a.write("\n")
    a.close()
    o.close()

    #Show final file contents (should be similar to the first one's)
    print('\nDecoded file contents:')
    b=open("../res/decodedTestFile.txt",'r')
    print(b.read())