
import sys
from bitarray import bitarray
class Node:
    def __init__(self, char=None, left=None, right=None):
        self.char = char
        self.left = left
        self.right = right

def decode_elias(eliascode):
    l = 1
    codelength = 1
    n = len(eliascode)
    while eliascode[0] == '0' and n > 1:
        eliascode = '1' + eliascode[1:]
        nextl = int(eliascode[:l],2) + 1
        codelength += nextl
        eliascode = eliascode[l:]
        l = nextl
    return int(eliascode[:l], 2), codelength

def decode(codeword):
    if codeword == '':
        return ''
    text = ''
    huffmanTree = Node()
    charNum, nextchunk = decode_elias(codeword)
    for _ in range(charNum): #reconstruct the huffman tree for the huff man codes, used later
        char = chr(int(codeword[nextchunk:nextchunk+8],2))
        huffmanlength, eliaslength = decode_elias(codeword[nextchunk + 8:])
        startOfHuffmanCode = nextchunk+8+eliaslength
        curNode = huffmanTree
        if charNum > 1:
            for j in range(huffmanlength):
                if codeword[startOfHuffmanCode+j] == '0':
                    if curNode.left is None:
                        curNode.left = Node()
                    curNode = curNode.left
                elif codeword[startOfHuffmanCode+j] == '1':
                    if curNode.right is None:
                        curNode.right = Node()
                    curNode = curNode.right
        curNode.char = char

        nextchunk += huffmanlength + eliaslength + 8

    fieldNum, eliaslength = decode_elias(codeword[nextchunk:])
    nextchunk += eliaslength

    for _ in range(fieldNum): #decoding lzss code
        if codeword[nextchunk] == '0':
            nextchunk += 1
            offset, eliaslength = decode_elias(codeword[nextchunk:])
            nextchunk += eliaslength
            matchSize, eliaslength = decode_elias(codeword[nextchunk:])
            nextchunk += eliaslength
            for i in range(matchSize):
                text += text[len(text) - offset]

        elif codeword[nextchunk] == '1':
            if charNum > 1:
                i = 1
            else: # when there is only one unique character in the text, e.g "aaaaaaaaa" the char itself will be stored in the root of the huffman tree and coded as '0'
                i = 2
            curNode = huffmanTree
            while curNode.left is not None: #go down the huffman tree to see which char the 0/1 code represents.
                if codeword[nextchunk+i] == '1':
                    curNode = curNode.right
                elif codeword[nextchunk+i] == '0':
                    curNode = curNode.left
                i += 1
            text += curNode.char
            nextchunk += i

    return text

if __name__ == '__main__':
    bitfile = sys.argv[1]

    stringfile = bitarray()
    with open(bitfile, 'rb') as binfile:
        stringfile.fromfile(binfile)

    # print(stringfile.to01())

    string = decode(stringfile.to01())

    with open('output_lzss_decoder.txt', 'w') as textfile:
        textfile.write(string)
