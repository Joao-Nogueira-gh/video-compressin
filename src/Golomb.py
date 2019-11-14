import math

from truncated_binary_encoding import truncated_binary_encoding

#todo: how to calculate optimal M?
#cant revert truncated binary encoding...

class Golomb:
    def __init__(self, factor):
        self.factor=factor
        self.sequenceFlag=False
        self.standardM=False
        if math.log(factor,2).is_integer():
            self.standardM=True

    def encode(self,string):
        print('encoding',string)
        number=int(string)
        (q,r)=divmod(number,self.factor)
        print(q,r)
        un=self.convertToUnary(q)
        bn=self.convertToBinary(r)
        r=un+bn
        print('encoded to',r)
        return r

    def decode(self,sequence):
        self.sequenceFlag=False
        q=0
        r=''
        #sequence is the encoded string
        for i in range(0,len(sequence)):
            if sequence[i]=='0' and self.sequenceFlag==False:
                self.sequenceFlag=True
                continue
            if self.sequenceFlag:
                r+=sequence[i]
            else:
                q+=1
        r=int(r,2)
        print(q,r)
        number=self.factor*q+r
        print('decoded->',number)
        return number


    def convertToUnary(self,number):
        # x 1's and one 0
        s=''
        for i in range(0,number):
            s+='1'
        s+='0'
        print(s)
        return s
    
    def convertToBinary(self,number):
        if self.standardM:
            conv="{0:b}".format(number) #alternative para retirar 0b
            print(conv,type(conv))
            return conv
        else:
            x=truncated_binary_encoding(number,self.factor)
            # b=math.log(self.factor,2)
            # b=math.ceil(b)
            # if number<b:
            #     #less bits
            #     pass
            # else:
            #     #more bits
            #     pass
            print("truncated",x,type(x))
            return x
