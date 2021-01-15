
from heapq import *
from bitarray import bitarray
import sys
class Node:#this node is used to construct huffman code, i defined lt because this is the thing that goes into a minheap
    def __init__(self, frequency, char=None, left=None, right=None):
        self.frequency = frequency
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency

def Z_algorithm(txt):
    """
    the logic is identical to the one in lecture with case 1, case 2a, and case 2b
    used in lzss encoding to find match
    :param txt:
    :return:
    """
    m = len(txt)
    Z = [0]*m
    l = 0
    r = 0
    for k in range(1, m):
        if k > r: # case 1
            r = k
            while r < m:
                if txt[r] != txt[r-k]:
                    break
                r += 1
            l = k
            Z[k] = r - l
        else:
            if Z[k - l] < r - k: # case 2a
                Z[k] = Z[k - l]
            else: # case 2b
                while r < m:
                    if txt[r] != txt[r-k]:
                        break
                    r += 1

                l = k
                Z[k] = r - l
    return Z

def buildHuffmanTree(text):
    countDic = {}
    for eachChar in text: #counting number of occurance of each unique char
        if eachChar in countDic.keys():
            countDic[eachChar] += 1
        else:
            countDic[eachChar] = 1

    minHeap = []
    for (i, j) in countDic.items():
        newNode = Node(j, i)
        heappush(minHeap, (j, newNode))

    while len(minHeap) > 1: #bilding huffman tree by choose the two least frequent Node (can be a char or a combined internal node) each iteration and combine them and put back to the heap, until only one node left.
        right = heappop(minHeap)
        left = heappop(minHeap)
        internalFrequency = left[0] + right[0]
        internalLabel = left[1].char + right[1].char
        newNode = Node(internalFrequency, internalLabel, left[1], right[1])
        heappush(minHeap, (internalFrequency, newNode))
    return minHeap[0][1]

def getHuffmanCode(node, code):
    """
    traverse huffman Tree to get the huffman code for each char
    :param node:
    :param code:
    :return:
    """
    if node.left is None:
        return [(node.char, code)]
    return getHuffmanCode(node.left, code+'0') + getHuffmanCode(node.right, code+'1')

def elias(number):
    code = str(bin(number))[2:]
    l = len(code) # l is the length for next length component
    while l > 1:
        l -= 1
        Lcomponent = str(bin(l))[2:]
        l = len(Lcomponent)
        code = '0' + Lcomponent[1:] + code
    return code

def findMatch(Z, window, buffer):
    """
    determine the offset and the matchsize using Z-algorithm
    :param Z:
    :param window:
    :param buffer:
    :return:
    """
    Z = Z[buffer+1:]
    Z = Z[:len(Z)-buffer]
    matchSize, matchStart = 0, 0
    for k in range(len(Z)):
        if Z[k] > matchSize:
            matchSize = Z[k]
            matchStart = k
    return matchSize, window - matchStart

def lzss(text, W, L, huffmanCode):
    """
    this is the algorithm off the slides, self-explanatory. count is the total number of Format-0/1 fields, used later for the encoding.
    :param text:
    :param W:
    :param L:
    :param huffmanCode:
    :return:
    """
    huffmanCode = {each[0]:each[1] for each in huffmanCode}
    code = ''
    n,i = len(text), 0
    count = 0
    while i < n:
        window = min(W, i)
        buffer = min(L, n-i)
        matcheSize, offset = findMatch(Z_algorithm(text[i:i+buffer] + '$' + text[i-window: i+buffer]), window, buffer)
        if min(matcheSize, offset) >= 3:
            code += '0' + elias(offset) + elias(matcheSize)
            i += matcheSize
        elif min(matcheSize, offset) < 3:
            code += '1' + huffmanCode[text[i]]
            i += 1
        count += 1
    return code, count

def encode(text, W, L):
    if text == '':
        return ''
    huffmanCode = getHuffmanCode(buildHuffmanTree(text), '')
    uniqueChar = len(huffmanCode)
    codeword = elias(uniqueChar)
    if uniqueChar == 1:
        huffmanCode[0] = (huffmanCode[0][0], '0') #if there is only one unique character in the text, assign it code 0

    for i in range(uniqueChar): #this is the header part
        codeword += '{:08b}'.format(ord(huffmanCode[i][0]))
        codeword += elias(len(huffmanCode[i][1]))
        codeword += huffmanCode[i][1]

    lzsscode, lzssfield = lzss(text, W, L, huffmanCode) #this is the body part
    codeword += elias(lzssfield) + lzsscode
    return codeword

if __name__ == '__main__':
    text = open(sys.argv[1]).read()
    W = int(sys.argv[2])
    L = int(sys.argv[3])


    codeword = encode(text, W, L)
    if codeword != '':
        codeword += '0'*(8 - (len(codeword) % 8))
    with open('output_lzss_encoder.bin', 'wb') as binfile:
        bitarray(codeword).tofile(binfile)

    # with open('output_lzss_encoder.text', 'w') as binfile:
    #     binfile.write(codeword)

# text = 'aaaaaaaaaaaa, this is bullshit: blazeblazeblazsebzseb, superlisto__joke is not fun, will burger get people choked-up on death?, 1+1 != 2.'
# W = 6
# L = 4

# binstring = bitarray('110101010')
# with open('test.bin', 'wb') as f:
#     f.write(binstring)
#
# with open('test.txt', 'w') as f:
#     f.write('110101010')