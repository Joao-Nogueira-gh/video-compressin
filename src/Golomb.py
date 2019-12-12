import math

#external library that implements truncated binary encoding
from truncated_binary_encoding import truncated_binary_encoding

#TODO: how to calculate optimal M?
#TODO:cant revert truncated binary encoding...

## \class Golomb 
# Basic implementation of an encoder/decoder using Golomb Codes
# \author Tiago Melo 89005
# \author João Nogueira 89262

class Golomb:

    def __init__(self, factor):
        ## Initialization function
        # \param[in] factor The value of "M" to be assigned to the Golomb Coder
        # setting up useful flags for decoding and checking if M==2^x
        self.factor=factor
        self.sequenceFlag=False
        self.standardM=False
        if math.log(factor,2).is_integer():
            self.standardM=True


    ## Encoding function
    # \param[in] number The number to be encoded
    # \param[out] code Returns the encoded number (string)
    # Computing quotient and remainder, and putting them together to form the code
    # Quotient converted to Unary code
    # Remainder converted to Binary code 
    def encode(self,number):
        #print('encoding',number)
        number=int(number) #in case it's not a number it also works with strings
        (q,r)=divmod(number,self.factor)
        #print(q,r)
        un=self.convertToUnary(q)
        bn=self.convertToBinary(r)
        #print('q',un,'-r',bn)
        code=un+bn
        #print('encoded to',code, type(code))
        return code

    ## Decoding function
    # \param[in] sequence The sequence of 0's and 1's (the code)
    # \param[out] number Returns decoded number
    # Iterating sequence:
    # Quotient is the sum of 1's until a 0 appears
    # Remainder is the direct conversion of binary code to integer
    # Number = factor*quotient + remainder
    def decode(self,sequence):
        self.sequenceFlag=False
        sequence=str(sequence) #making sure it is a string
        q=0
        r='' 
        for i in range(0,len(sequence)):
            if sequence[i]=='0' and self.sequenceFlag==False:
                self.sequenceFlag=True
                continue
            if self.sequenceFlag:
                r+=sequence[i]
            else:
                q+=1
        r=int(r,2)
        #print(q,r)
        number=self.factor*q+r
        #print('decoded->',number, type(number))
        return number

    ## Convertion to Unary Code
    # \param[in] number The number to be encoded to Unary
    # \param[out] sequence The Unary code sequence
    # In this implementation we add X 1's where X=number, followed by a 0
    def convertToUnary(self,number):
        # x 1's and one 0
        sequence=''
        for i in range(0,number):
            sequence+='1'
        sequence+='0'
        #print(sequence)
        return sequence
    ## Convertion to Binary Code
    # \param[in] number The number to be encoded to Binary
    # \param[out] sequence The Binary code sequence
    # If our factor=2^x then it's normal binary encoding
    # Else it's truncated binary encoding (WIP)
    def convertToBinary(self,number):
        if self.standardM:
            sequence="{0:b}".format(number) #alternative para retirar 0b
            #print(sequence)
            nb=int(math.log(self.factor,2))
            dif=nb-len(sequence)
            #print(dif)
            if dif!=0:
                for i in range(0,dif):
                    sequence='0'+sequence
            return sequence
        else:
            sequence=truncated_binary_encoding(number,self.factor)
            # b=math.log(self.factor,2)
            # b=math.ceil(b)
            # if number<b:
            #     #less bits
            #     pass
            # else:
            #     #more bits
            #     pass
            #print("truncated",sequence)
            return sequence
