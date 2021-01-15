
import sys

text = sys.argv[1]
patttern = sys.argv[2]
with open(text) as txt:
    txt = txt.read()
with open(patttern) as pat:
    pat = pat.read()

f = open('output_hammingdist.txt', 'w')

def GusfieldZ_algorithm(txt):
    m = len(txt)
    Z = [0]*m
    l = 0
    r = 0
    for k in range(1, m):
        if k > r:
            r = k
            while r < m and txt[r] == txt[r-k]:
                r += 1
            l = k
            Z[k] = r - l
        else:
            if Z[k - l] < r - k:
                Z[k] = Z[k - l]
            else:
                while r < m and txt[r] == txt[r-k]:
                    r += 1
                l = k
                Z[k] = r - l
    return Z

def searchHammingDist(pat, txt):
    """
        the logics of this algorithm is that you match pat+'$'+txt and match reverse(pat)+'$'+reverse(txt), so you have the Z-algorithm forward and backward, denoted as
    Z_forward and Z_backward.
        if there is a hamming distance of 1 in a hammingdist-1 match, the sum of the two Z-values: Z_forward[i] and Z_backward[i+len(pat)-1] is equal to len(pat) - 1.
        this is how you find the hammingdistance-1 match (match that has hamming distance 1)
    :param pat:
    :param txt:
    :return:
    """
    pat, txt = pat.lower(), txt.lower()
    n = len(txt)
    m = len(pat)
    Z_f = GusfieldZ_algorithm(pat+'$'+txt)[len(pat)+1:]
    Z_b = GusfieldZ_algorithm(pat[::-1]+'$'+txt[::-1])[len(pat)+1:][::-1]
    for i in range(n-m+1):
        if Z_f[i] + Z_b[i+m-1] == m - 1: #hamming dist of 1
            f.write(str(i+1)+'\t'+str(1)+'\n')
        elif Z_f[i] == m: # exact match
            f.write(str(i + 1) + '\t' + str(0) + '\n')

searchHammingDist(pat, txt)

f.close()

# searchHammingDist('abc', 'bbcaefadcabcpqr')
# searchHammingDist('abc', 'abdababcbc')
