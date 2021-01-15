
import sys

text = sys.argv[1]
patttern = sys.argv[2]
with open(text) as txt:
    txt = txt.read()
with open(patttern) as pat:
    pat = pat.read()

f = open('output_kmp.txt', 'w')

def GusfieldZ_algorithm(txt):
    """
    the logic is identical to the one in lecture with case 1, case 2a, and case 2b
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

def Calculate_SPx(pat):
    """
        what is different from the original sp list is that it SPx is a 2-D array, with size len(pat) x 26.
        SP[i] is a list of size 26, SP[i][j] stands for the the length of the longest proper suffix of pat[1..i] that matches the prefix
    of pat with j corresponding to the 'index' (a is 0, b is 1 and so on) of the one letter before the matched suffix of pat[1..i]
    :param pat:
    :return SPx:
    """
    Z = GusfieldZ_algorithm(pat)
    m = len(pat)
    SPx = [[0]*26 for _ in range(m)]
    for j in range(m-1, 0, -1):
        i = j + Z[j] - 1
        SPx[i][ord(pat[Z[j]])-ord('a')] = Z[j]

    return SPx

def KMP_algorithm(pat, txt):
    """
        this is the modified kmp algorithm using SPx value, basically when you find a mismatch, at corresponding index i of pat, and j+i of txt, you update by the SPx[i][ord(i-1)],
    where stores the shift value that indicates the longest suffix of pat[1..i] that matches the prefix and right after the certain char(used for indexing) that the corresponding mismatch happened in the txt
    :param pat:
    :param txt:
    :return:
    """
    txt, pat = txt.lower(), pat.lower()
    SPx = Calculate_SPx(pat)
    end, m = len(txt), len(pat)
    cur = 0
    while cur + m < end:
        mismatch = False
        for i in range(m):
            if pat[i] != txt[cur+i]:
                mismatch = True
                cur += max(1, i-SPx[i-1][ord(txt[cur+i])-ord('a')])
                break

        if not mismatch: #loop finished without mismatch
            f.write(str(cur+1)+'\n')
            cur += m-SPx[m-1][ord(txt[cur+m])-ord('a')]

    if pat == txt[end - m:]:
        f.write(str(cur + 1))


KMP_algorithm(pat, txt)

f.close()