#imports
import pickle
import os

#https://code.activestate.com/recipes/498121-python-octree-implementation/
MAX_OBJECTS_PER_CUBE = 10
same_branch_counter=0
last_branch=0

class octNode:
    def __init__(self, position, size, data):
        self.position=position
        self.data=data
        self.size=size
        self.blacklist=False

        #every octNode starts as a leafNode with no branches
        self.isLeafNode=True
        self.branches=[None, None, None, None, None, None, None, None]

class octTree:
    def __init__(self, worldSize):
        #worldsize is 255 because rgb values range from 0 to 255
        self.root=self.addNode((0,0,0), worldSize, [])
        self.worldsize=worldSize
    
    def findBranch(self, root, position):
        #position of the current root and the current object
        vec1 = root.position
        vec2 = position
        result = 0

        #constants
        DIRLOOKUP = {"FalseFalseFalse":0, "FalseFalseTrue":1, "TrueFalseTrue":2, "TrueFalseFalse":3, "FalseTrueFalse":4, "FalseTrueTrue":5, "TrueTrueTrue":6, "TrueTrueFalse":7}

        #returns the index of the node to travel to
        strdir=str(vec2[0]>=vec1[0])+str(vec2[1]>=vec1[1])+str(vec2[2]>=vec1[2])
        result = DIRLOOKUP[strdir]
        return result

    def findPosition(self, root, position):
        # Basic collision lookup that finds the leaf node containing the specified position
        # Returns the child objects of the leaf, or None if the leaf is empty or none
        if root == None:
            return None
        elif root.isLeafNode:
            return root.data
        else:
            branch = self.findBranch(root, position)
            return self.findPosition(root.branches[branch], position)

class TestObject:
        def __init__(self, name, position):
            self.name = name
            self.position = position

def find_color(arr):
    return loadedOctTree.findPosition(loadedOctTree.root,arr)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
loadedOctTree=pickle.load(open(os.path.join(__location__, 'emojiTree'),'rb'))