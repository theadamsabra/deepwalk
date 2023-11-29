# Taken and repurposed from:
# https://github.com/loginaway/DeepWalk/blob/master/deepwalk/BinaryTree.py

import torch
import numpy as np

class Node(object):
    '''
    Tree node.
    '''
    def __init__(self, embedding_size, phi=None):
        self.left=None
        self.child={'0':None, '1':None} # direc['0']: left child, else right child
        self.Phi = torch.randn(embedding_size, 1)

class Tree(object):
    def __init__(self, whole_size, embedding_size):
        BinarySeq=bin(whole_size).lstrip('0b')
        self.layer_size=len(BinarySeq)
        self.whole_size=whole_size
        self.embedding_size=embedding_size
        self.root=Node(self.embedding_size)

    def index2Bin(self, index):
        '''
        Turn index of vi(word vector) to Binary Sequence 
        with layer_size length.
        '''
        return bin(index).lstrip('0b').rjust(self.layer_size, '0')

    def growTree_from_single(self, BinarySeq):
        '''
        Grow Tree from one Sequence.
        '''
        prev=self.root
        for i in BinarySeq[:-1]:
            if prev.child[i]: # Child Not Null
                prev=prev.child[i]
            else:   # child[i] is Null
                N=Node(self.embedding_size)
                prev.child[i]=N
                prev=N

    def growTree_from_multiple(self, BinarySeqs):
        '''
        Grow Tree from a list of Sequences.
        '''
        for seq in BinarySeqs:
            self.growTree_from_single(seq)

    def growTree(self, indexList=None):
        '''
        If indexList is input, then grow the tree using indexes from indexList.
        Otherwise, use indexes: 0 to whole_size as the input to grow the tree.
        '''
        if indexList:
            seqs=[self.index2Bin(i) for i in indexList]
        else:
            seqs=[self.index2Bin(i) for i in range(self.whole_size)]
        self.growTree_from_multiple(seqs)

    def getNodeList(self, index):
        '''
        index: index of vi(word vector)
        Retrieve nodes on the route from root to vi.
        '''
        seq=self.index2Bin(index)
        prev=self.root
        nodeList=np.empty(self.layer_size, dtype=object)
        nodeList[0]=prev
        for i in range(len(seq[:-1])):
            prev=prev.child[seq[i]]
            nodeList[i+1]=prev
        return nodeList
