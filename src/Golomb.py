## @class Golomb 
# Basic implementation of an encoder/decoder using Golomb Codes
# @author Tiago Melo 89005
# @author João Nogueira 89262

import math

class Golomb:

    def __init__(self, factor):
        ## Initialization function
        # @param[in] factor The value of "M" to be assigned to the Golomb Coder
        # setting up useful flags for decoding and checking if M==2^x
        self.factor=factor #M

        self.sequenceFlag=False
        self.standardM=False

        if math.log(factor,2).is_integer():
            self.standardM=True


    ## Encoding function
    # @param[in] number The number to be encoded
    # @param[out] code Returns the encoded number (string)
    # Computing quotient and remainder, and putting them together to form the code
    # Quotient converted to Unary code
    # Remainder converted to Binary code 
    def encode(self,number):

        number=int(number) #in case it's not a number it also works with strings
        (q,r)=divmod(number,self.factor)

        un=self.convertToUnary(q)
        bn=self.convertToBinary(r)

        code=un+bn

        return code


    ## Decoding function
    # @param[in] sequence The sequence of 0's and 1's (the code)
    # @param[out] number Returns decoded number
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

        number=self.factor*q+r

        return number


    ## Convertion to Unary Code
    # @param[in] number The number to be encoded to Unary
    # @param[out] sequence The Unary code sequence
    # In this implementation we add X 1's where X=number, followed by a 0
    def convertToUnary(self,number):
        sequence=''

        for i in range(0,number):
            sequence+='1'

        sequence+='0'

        return sequence


    ## Convertion to Binary Code
    # @param[in] number The number to be encoded to Binary
    # @param[out] sequence The Binary code sequence
    # If our factor=2^x then it's normal binary encoding, keeping in mind the number of bits should be equal to log(factor,2)
    # If it isn't then truncated binary encoding is not implemented
    def convertToBinary(self,number):
        if self.standardM:
            sequence="{0:b}".format(number) #alternative para retirar 0b
            nb=int(math.log(self.factor,2))
            dif=nb-len(sequence)

            if dif!=0: #adding 0's so that the number of bits of the Remainder = log(factor,2)
                for i in range(0,dif):
                    sequence='0'+sequence

            return sequence
        else:
            print('not implemented for m!=2^x')
            exit(0)