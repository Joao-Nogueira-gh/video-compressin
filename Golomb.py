class Golomb:
    def __init__(self, factor):
        self.factor=factor

    def encode(self,number):
        (q,r)=divmod(number,self.factor)
        print(q,r)
        self.convertToUnary(q)
        self.convertToBinary(r)

    def convertToUnary(self,number): #todo, turn into string, not list
        l=[1 for e in range(0,number)]+[0]
        print(l)
        return l
    
    def convertToBinary(self,number):
        conv="{0:b}".format(number) #alternative para retirar 0b
        print(conv,type(conv))
        return conv
