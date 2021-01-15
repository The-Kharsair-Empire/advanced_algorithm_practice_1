
import sys

# text = sys.argv[1]
# patttern = sys.argv[2]
# with open(text) as txt:
#     txt = txt.read()
# with open(patttern) as pat:
#     pat = pat.read()
txt = "cabc"
pat= "a"
f = open('output_editdist.txt', 'w')

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


def searchEditDist(pat, txt):
    """
        the logics of this algorithm is that you match pat+'$'+txt and match reverse(pat)+'$'+reverse(txt), so you have the Z-algorithm forward and backward, denoted as
    Z_forward and Z_backward.
        if there is a edit distance of 1 in a editdist-1 match, there are four cases:
            1: exact match, Z_forward[i] = len(pat)
            2: the sum of the two Z-values: Z_forward[i] and Z_backward[i+len(pat)-1] is equal to len(pat) - 1 (hamming distance = 1).
            3: deletion case, one char missing, the sum of the two Z-values: Z_forward[i] and Z_backward[i+len(pat)-2] is equal to len(pat) - 1
            4: insertion case, one char extra, the sum of the two Z-values: Z_forward[i] and Z_backward[i+len(pat)] is equal to len(pat)
        there are few exceptions. if a exact match is found at i, than case 3 at i+1, i, case 4 at i, i-1 should be avoided. for example, a match of pat 'abc' found
    the editdist-1 match of ab, bc, xabc, abcx should be avoided. it can be down using either more if-else cases or using runtime order in if-else block to prevent.
        In my code, repeat matching of ab, and abcx is avoided by the latter, if abc is found,  the loop will terminate to prevent further searching of ab and abcx.
    bc is prevented by the intrisic property of z value, as Z_forward[i] is 3, Z_backward[i+len(pat)-1] is also three, so case 3:
    Z_backward[i+len(pat)-2] is equal to len(pat) so it can't be len(pat)-1 anyway. xabc is prevented by a additional if condition, if Z_forward[i+1] is a exact match,
    then forward[i] would be counted for this case.
        this is how you find the editdistance-1 match (match that has edit distance 1)
    :param pat:
    :param txt:
    :return:
    """
    pat, txt = pat.lower(), txt.lower()
    n = len(txt)
    m = len(pat)
    Z_f = GusfieldZ_algorithm(pat+'$'+txt)[len(pat)+1:]
    Z_b = GusfieldZ_algorithm(pat[::-1]+'$'+txt[::-1])[len(pat)+1:][::-1]
    i = 0
    while i < n-m+1:
        if Z_f[i] == m: #case 1: exact match, Z_forward[i] = len(pat)
            f.write(str(i+1)+'\t'+str(0)+'\n')
        elif Z_f[i] + Z_b[i+m-1] == m - 1: # case 2: the sum of the two Z-values: Z_forward[i] and Z_backward[i+len(pat)-1] is equal to len(pat) - 1 (hamming distance = 1).
            f.write(str(i + 1) + '\t' + str(1)+'\n')
        elif Z_f[i] + Z_b[i+m-2] == m - 1:#case 3: deletion case, one char missing, the sum of the two Z-values: Z_forward[i] and Z_backward[i+len(pat)-2] is equal to len(pat) - 1
            f.write(str(i + 1) + '\t' + str(1)+'\n')
        elif i + m < n and Z_f[i] + Z_b[i+m] == m: #case 4: insertion case, one char extra, the sum of the two Z-values: Z_forward[i] and Z_backward[i+len(pat)] is equal to len(pat)
            if Z_f[i+1] != m: # avoid matching xabc where abc is the exact match
                f.write(str(i + 1) + '\t' + str(1)+'\n')
        i += 1
    # if Z_f[i] + Z_b[i+m-2] == m - 1:  #loop will terminate when there is m char length remain, so there is still one more deletion case at the next position. match it manually
    #     f.write(str(i + 1) + '\t' + str(1))

searchEditDist(pat, txt)

f.close()