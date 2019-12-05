class BitInput {
    istream& in;  // the istream to delegate to
    char buf;     // the buffer of bits
    int nbits; public:

BitInputStream(istream& s) : in(s), buf(0), bufi(8) { }


/** Read the next bit from the bit buffer.
 *  Return the bit read as the least significant bit of an int.
 */
int readBit(){
    int i;
    if(nbits == 8){
        buf = in.get();
        nbits = 0;
    }
    i = (1 & buf>>(7-nbits)); //This could be the problem, I'm not getting the writing bit
    nbits++;
    return i;
}

/** Read a char from the ostream (which is a byte)*/
int readChar(){
    int sum = 0;
    for(int i = 7; i>=0; i--) 
        sum = (sum*2) + readBit();
    return sum;
}
class BitOutput {
     ostream& out;  // the istream to delegate to
    char buf;     // the buffer of bits
    int nbits;     // the bit buffer index

public:

    BitOutput(istream& s) : in(s), buf(0), bufi(8) { }

    /* Write the least significant bit of the argument */
    void writeBit(int i){
        //Flush the buffer
        if(nbits == 8){
            out.put(buf);
            out.flush();
            bufi = 0;
            buf = 0;
        }
        buf = buf | (i<<(7-nbits)); //Did it write the right bit to ostream ?
        nbits++;
    }

    /** Write a char to the ostream (a byte) */
    void writeChar(int ch){
        for(int i = 7; i >= 0; i--) 
            writeBit((ch >> i) & 1);
    }