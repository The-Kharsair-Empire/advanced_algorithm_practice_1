
class Node:
    """
    this is each node in binomial heap
    """
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.child = self.sibling = self.parent = None

class BinomialHeap:
    def __init__(self, node):
        """
        this function is call only when inserting a tree to a heap so it's safe to assume the min node is the root as there is only one tree.
        :param node:
        """
        self.heap = [node]
        self.min = node # min node is always the top node for a binomial heap that contain only one tree

    def mergeTree(self, tree1, tree2):
        """
        merging tree is quite simple, just compare two tree root in terms of key and make one the child of the other, and update the sibling
        :param tree1:
        :param tree2:
        :return:
        """
        if tree1.key > tree2.key:
            tree1, tree2 = tree2, tree1
        tree2.parent = tree1
        tree2.sibling = tree1.child
        tree1.child = tree2
        tree1.degree += 1
        return tree1

    def extractMin(self):
        """
        same as remove the current min root and merge its children into the main heap
        :return:
        """
        retVal = self.min
        self.heap.remove(self.min)

        if retVal.child is not None:
            newHeap = BinomialHeap(retVal.child)
            curNode = retVal.child.sibling
            retVal.child.sibling = None
            while curNode is not None:
                newHeap.mergeHeap(BinomialHeap(curNode))
                temp = curNode
                curNode = curNode.sibling
                temp.sibling = None
            self.mergeHeap(newHeap)
        temp = list(map(lambda x: x.key, self.heap))
        self.min = self.heap[temp.index(min(temp))] if temp != [] else self.min

        return retVal

    def insert(self, node):
        """
        merge a heap that contains only one element into the heap
        :param node:
        :return:
        """
        self.mergeHeap(BinomialHeap(node))

    def mergeHeap(self, anotherHeap):
        """

        the merging of binomial heap utilize the idea of binary addition.
        for i, j each tree in heap 1 and heap2
            if degree(root of heap1[i]) == degree(root of heap2[j]):
                merge them, push into the newheap
            else if one is greater than the other in degree:
                take the lesser
                see if its degree equals to the tree with the largest degree:
                if degree(root of lesser) == degree(root of newheap[-1])
                    merge them
                else:
                    just push lesser into the newheap
        if there is any tree left either heap 1 or heap 2, (can't be both because one has to run out to exit the loop)
            push them to the newheap, merge from newheap[-1] if necessary
        :param self, anotherHeap:
        :return: a merged heap
        """
        heap1 = self.heap
        heap2 = anotherHeap.heap
        # print(self.visualizeHeap(self))
        # print(self.visualizeHeap(anotherHeap))
        newHeap = []
        i = j = 0
        while i < len(heap1) and j < len(heap2):
            if heap1[i].degree < heap2[j].degree:
                if len(newHeap) > 0 and newHeap[-1].degree == heap1[i].degree:
                    newHeap[-1] = self.mergeTree(newHeap[-1], heap1[i])
                else:
                    newHeap.append(heap1[i])
                i += 1
            elif heap1[i].degree > heap2[j].degree:
                if len(newHeap) > 0 and newHeap[-1].degree == heap2[j].degree:
                    newHeap[-1] = self.mergeTree(newHeap[-1], heap2[j])
                else:
                    newHeap.append(heap2[j])
                j += 1
            else:
                newHeap.append(self.mergeTree(heap1[i], heap2[j]))
                i += 1
                j += 1

        while j < len(heap2):
            if len(newHeap) > 0 and heap2[j].degree == newHeap[-1].degree:
                newHeap[-1] = self.mergeTree(heap2[j], newHeap[-1])
            else:
                newHeap += heap2[j:]
                break
            j += 1

        while i < len(heap1):
            if len(newHeap) > 0 and heap1[i].degree == newHeap[-1].degree:
                newHeap[-1] = self.mergeTree(heap1[i], newHeap[-1])
            else:
                newHeap += heap1[i:]
                break
            i += 1

        self.heap = newHeap
        self.min = self.min if self.min.key <= anotherHeap.min.key else anotherHeap.min

    # def visualizeHeap(self, heap):
    #     vis = ''
    #     li = []
    #     for i in heap.heap:
    #         vis += str(i.degree) + ' <---- '
    #         li.append(i.degree)
    #
    #     for i in range(1,len(li)):
    #         if li[i] <= li[i-1]:
    #             return vis, 'wrong'
    #     return vis, 'correctus!'




import sys
file = sys.argv[1]
with open(file) as f:
    f = f.readlines()
data = [int(i.strip()) for i in f]

head = BinomialHeap(Node(data[0]))
for i in data[1:]:
    head.insert(Node(i))

output = open('output_bhsort.txt', 'w')
while head.heap != []:
    output.write(str(head.extractMin().key)+'\n')

output.close()
