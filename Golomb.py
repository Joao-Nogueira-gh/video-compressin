class Golomb:
    def __init__(self, factor):
        self.factor=factor
        self.sequenceFlag=False

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
        conv="{0:b}".format(number) #alternative para retirar 0b
        print(conv,type(conv))
        return conv
