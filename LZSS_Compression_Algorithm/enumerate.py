
def enumerateTraversal(N, internalNode, previousCombo):
    """
    the logics behind this agorithm is that for any tree that has a internal Node of N, it has N-1 internal Node distributed between left/right children of its root Node
    since we already found the traversal of any N-k where 0 < k < N -internalNode tree, the pre-order traversal of tree with Internal Node = N is : '0' + traversal(left child) + traversal(right child)
    :param N:
    :param internalNode:
    :param previousCombo:
    :return:
    """
    if internalNode > N:
        return previousCombo
    thisCombo = []
    for i in range(internalNode):
        left = internalNode-1-i
        right = i
        for j in previousCombo[left]:
            for k in previousCombo[right]:
                traversal = '0' + j + k
                thisCombo.append(traversal)
    previousCombo.append(sorted(thisCombo))
    return enumerateTraversal(N, internalNode + 1, previousCombo)

import sys

N = int(sys.argv[1])

enumerateResult = enumerateTraversal(N, 1, [['1']])
formattedResult = []
outputFile =  open('output_enumerate.txt', 'w')
i = 1
for eachN in enumerateResult:
    for j in eachN:
        outputFile.write('{}\t{}\n'.format(i, j))
        i += 1

outputFile.close()


