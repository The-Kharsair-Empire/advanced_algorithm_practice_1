
class Root:
    """
    this is the root node
    it is safe to use dictionary as hash value for A-Z, a-z, 0-9, are unique
    """
    def __init__(self, link=None):
        self.link = link
        self.children = {}

    def addchild(self, key, node):
        self.children[key] = node

    def getchild(self, key):
        return self.children[key] if self.haschild(key) else None

    def haschild(self, key):
        return key in self.children

class Node(Root):
    """
    this is internal node, it shares some attributes and method from root, so here it inherited Root
    """
    def __init__(self, start, end, link=None):
        super().__init__(link)
        self.start = start
        self.end = end
        self.edgelength = end-start

    def getEdgeLength(self):
        return self.end-self.start

class Leaf():
    """
    this is the leaf node, because its end is a global variable, its end is represented using a class End instead of a integer
    """
    def __init__(self, startIndex, start, end):
        self.startIndex = startIndex
        self.start = start
        self.end = end
        self.edgelength = end.getend()-start

    def getEdgeLength(self):
        return self.end.getend()-self.start

class End():
    """
    this is the leaf end, to maintain the consistency of global variable, enclose it in a class
    """
    def __init__(self):
        self.leafend = 0

    def increment(self, by=1):
        self.leafend += by

    def getend(self):
        return self.leafend

def construct(string):
    """
    method heavily inspired by visualization animation of ukkonnen algorithm on: http://brenden.github.io/ukkonen-animation/ , very amazing visual aid, check it out


    for each phase:
        update leaf -> rule 1 done
        while number of extension left to be done > 0: (# of times rule3 applies last phase)
            if there exist a path edge already to walk down to the current char:
                if need skip/count trick, walk down to the next node:
                    'continue next iteration of while loop
                if edge already seen:
                    leave no change -> rule 3 done
                    break
                elif the last char x mismatch in the middle of the edge:
                    create a node in the edge, branch out from that node -> rule 2 case 1 done
                    traverse through suffix link to do this for every internal node that has the same edge, until root node is reached, update the pointer itself instead of traversing suffix link
            else:
                creating a new leaf from the node you are going out -> rule 2 case 2 done

    :param string:
    :return: a constructed suffix tree
    """
    root = Root()
    activeNode = root
    activeEdge = None
    activeLength = 0
    leafEnd = End()
    remainder = 0
    n = len(string)
    for i in range(n):
        leafEnd.increment() # applies rule 1, once leaf always leaf, done in O(1)
        remainder += 1 #because current char at phase i needed to be dealt with plus some that wans't dealt from the previous phase (skipped by rule 3)
        lastNode = None
        while remainder > 0:
            if activeLength == 0: # it means the pointer hasn't pointing any existing edge, it should follow your current char
                activeEdge = i

            if activeNode.haschild(string[activeEdge]): # there exist a path edge to current char,
                child = activeNode.getchild(string[activeEdge])
                edgeLength = child.getEdgeLength()
                if activeLength >= edgeLength: #skip/count tricks is needed
                    activeNode = child
                    activeLength -= edgeLength
                    activeEdge += edgeLength
                    continue
                if string[i] == string[child.start + activeLength]: #rule 3 applies,
                    activeLength += 1
                    if activeNode != root and lastNode is not None: #because rule3 happens after rule 2, the last internal node created in rule 2 hasn't been given a suffix link
                        lastNode.link = activeNode
                        lastNode = None
                    break

                else: #rule 2 case 1 applies, make new internal node
                    newNode = Node(child.start, child.start + activeLength, root) #where they cut the edge making a new branch out
                    activeNode.addchild(string[activeEdge], newNode)
                    suffixstart = child.start
                    child.start = child.start+activeLength
                    newNode.addchild(string[child.start], child)
                    newNode.addchild(string[i], Leaf(suffixstart, i, leafEnd))#new leaf adding to that new node
                    if lastNode is not None: #adding suffix link
                        lastNode.link = newNode
                    lastNode = newNode #remember where it come from for the next node's suffix link
                    remainder -= 1
                    if activeNode != root:
                        activeNode = activeNode.link # traverse through suffix links
                    elif activeNode == root and activeLength > 0:
                        activeLength -= 1
                        activeEdge = i - remainder + 1

            else: #child not added, rule 2 case 2 applies, creating child from existing node (including root node)
                suffixstart = i if activeNode == root else activeNode.start
                activeNode.addchild(string[i], Leaf(suffixstart, i, leafEnd))
                if lastNode is not None:
                    lastNode.link = activeNode
                    lastNode = None
                remainder -= 1
                if activeNode != root:
                    activeNode = activeNode.link  # traverse through suffix links
                elif activeNode == root and activeLength > 0:
                    activeLength -= 1
                    activeEdge = i - remainder + 1

    return root

def similar(a, b):
    """
    if the lcp doesn't end on a node, it ends in the middle of a edge. count how many chars are they the same
    :param a:
    :param b:
    :return:
    """
    count = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            return count
        count += 1
    return count


def search(string, tree, i, j):
    """
    travese using skip/count tricks to find lcp, because lcp share the same edge and internal node in the suffix tree
    :param string:
    :param tree:
    :param i:
    :param j:
    :return:
    """
    first = tree.getchild(string[i])
    second = tree.getchild(string[j])
    length = 0
    while first == second:

        tree = first
        edgeLength = first.getEdgeLength()
        if string[i+edgeLength-1] == string[j+edgeLength-1]:
            length += edgeLength
            i += edgeLength
            j += edgeLength
            if type(tree) == Leaf:
                length -= 1
                break
            first = tree.getchild(string[i])
            second = tree.getchild(string[j])
        else:
            print('here')
            length += similar(string[i:i+edgeLength], string[j:j+edgeLength])
            break

    return length

import sys
string = sys.argv[1]
pairs = sys.argv[2]

with open(string) as sfile:
    string = sfile.read()
with open(pairs) as pfile:
    pfile = pfile.readlines()

string += '$'
tree = construct(string)

output =  open('output_lcps.txt', 'w')
for i in pfile:
    i = i.strip().split()
    output.write(i[0]+'\t'+i[1]+'\t'+str(search(string, tree, int(i[0])-1, int(i[1])-1))+'\n')

output.close()

