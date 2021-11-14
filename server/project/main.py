#standard library
import base64
import io
import os
import pickle
import random
import math
#packages
from PIL import Image
import numpy as np
from numpy.core.numeric import full_like
from numpy.core.records import find_duplicate
import flask
from flask import Flask, request, jsonify

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
app=Flask(__name__)

#octTree#######################################################################################
MAX_OBJECTS_PER_CUBE = 20
same_branch_counter=0
last_branch=0
tree=None

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

    def addNode(self, position, size, data):
        return octNode(position, size, data)

    def insertNode(self, root, size, parent, objData):
        global same_branch_counter, last_branch
        #this function will recursively travel from the root (0,0,0) to the correct leaf node
        #and either add the object to the leaf node if it is not full or take the list of objects
        #and the object to be added and add them to new leaf nodes within the old leaf node, which
        #at that point becomes a branch
        if root == None:
            # this means we're in the process of breaking up a full branch into 8 leaf nodes
            # we basically position the new node in the correct corner of the parent branch node and adding the object to it
            # where the correct corner is the one closest to the object position
            pos = parent.position
            offset = size / 2
            # find out which direction we're heading in
            branch = self.findBranch(parent, objData.position)
            # new center = parent position + (branch direction * offset)
            newCenter = (0,0,0)
            if branch == 0:
                # left down back
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] - offset )
                
            elif branch == 1:
                # left down forwards
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] + offset )
                
            elif branch == 2:
                # right down forwards
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] + offset )
                
            elif branch == 3:
                # right down back
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] - offset )

            elif branch == 4:
                # left up back
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] - offset )

            elif branch == 5:
                # left up forward
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] + offset )
                
            elif branch == 6:
                # right up forward
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] + offset )

            elif branch == 7:
                # right up back
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] - offset )
            # Now we know the centre point of the new node
            # we already know the size as supplied by the parent node
            # So create a new node at this position in the tree
            return self.addNode(newCenter, size, [objData])

        elif root.position != objData.position and root.isLeafNode == False:
            # we're in an octNode still, we need to traverse further
            branch = self.findBranch(root, objData.position)
            # Find the new scale we working with
            newSize = root.size / 2
            # attempt to insert the object into the next branch recursively until that branch is actually a leaf node
            #at which point this block of the if else won't be triggered
            root.branches[branch] = self.insertNode(root.branches[branch], newSize, root, objData)

        elif root.isLeafNode:
            # We've reached a leaf node. This has no branches yet, but does hold
            # some objects. We can add the object to the leaf directly if it doesn't
            # exceed the object limit, or if it does we can take all the objects and
            # create new sub leaf nodes 
            if len(root.data) < MAX_OBJECTS_PER_CUBE:
                root.data.append(objData)
            elif len(root.data) == MAX_OBJECTS_PER_CUBE and root.blacklist==False:
                # Adding this object to this leaf takes us over the limit
                # So we have to subdivide the leaf and redistribute the objects
                # on the new children. 
                # Add the new object to pre-existing list
                root.data.append(objData)
                # copy the list
                objList = root.data
                # Clear this node's data
                root.data = None
                # turn the current node into a branch node
                root.isLeafNode = False
                # Calculate the size of the new child leaf nodes
                newSize = root.size / 2
                # distribute the objects on the new tree
                # print "Subdividing Node sized at: " + str(root.size) + " at " + str(root.position)
                for ob in objList:
                    branch = self.findBranch(root, ob.position)
                    if branch==last_branch:
                        same_branch_counter+=1
                        if same_branch_counter>500:
                            root.blacklist=True
                    else:
                        same_branch_counter=0
                    last_branch=branch
                    if not root.blacklist:
                        root.branches[branch] = self.insertNode(root.branches[branch], newSize, root, ob)
                    
        return root
    
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
            return [TestObject("0001.png",0)]
        elif root.isLeafNode:
            return root.data
        else:
            branch = self.findBranch(root, position)
            return self.findPosition(root.branches[branch], position)

class TestObject:
        def __init__(self, name, position):
            self.name = name
            self.position = position

#dump tree
emojidict=pickle.load(open(os.path.join(__location__, 'emojidict'),'rb'))
myTree = octTree(255.0000)
i=0
keylist=list(emojidict.keys())
random.shuffle(keylist)
for i in keylist:
    emojidict[i]=tuple([x-127.5 for x in emojidict[i]])
    obj=TestObject(i,emojidict[i])
    myTree.insertNode(myTree.root,255.0000,myTree.root,obj)
print("Tree loaded...")
#GOOD CODE###########################################################################################################################################################
filter_size=150
step_size=15
valid_sizes=[int(i*step_size+filter_size) for i in range(100)]

def find_color(arr):
    return myTree.findPosition(myTree.root,arr)

@app.route('/',methods=['POST'])
def img_proc():
    global filter_size, step_size, valid_sizes
    b64string=jsonify.loads(request.data).image
    image_arr=np.array(Image.open(io.BytesIO(base64.b64decode(b64string))))
    #image_arr=np.array(Image.open("C:\\Users\\owenb\\OneDrive\\Pictures\\Saved Pictures\\big_ass_image.png"))
    smallest=min(image_arr.shape[0:1])

    #resize image to a processible size
    chosen=0
    for i in range(len(valid_sizes)):
        if valid_sizes[i]>smallest:
            chosen=valid_sizes[i-1]
            break
    image_arr=image_arr[:chosen,:chosen,:]
    o=image_arr.copy()
    canvas=np.full_like(image_arr,0)
    canvas_img=Image.new('RGBA',Image.fromarray(canvas).size,(0,0,0,0))

    for i in range(int(max(image_arr.shape))):
        left=random.randrange(0,image_arr.shape[0])
        right=left+filter_size
        top=random.randrange(0,image_arr.shape[0])
        bottom=top+filter_size
        image=find_color([np.average(image_arr[left:right,top:bottom,0]),np.average(image_arr[left:right,top:bottom,1]),np.average(image_arr[left:right,top:bottom,2])])[0].name
        emoji_arr=np.array(Image.open(os.path.join(__location__, 'emojis/',image)))

        #open emoji as image
        img=Image.fromarray(emoji_arr)

        #make whitespace transparent
        img = img.convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(item)

        #paste images
        canvas_img.paste(img,(top,left),mask=img)
        


    # #convert white to nan to ignore it
    # masked=np.where(image_arr == 255, np.nan, image_arr)
    # for i in range(0,image_arr.shape[1]-filter_size+1,step_size):
    #     for j in range(0,image_arr.shape[0]-filter_size+1,step_size):
    #         image=find_color([np.nanmean(masked[j:j+filter_size,i:i+filter_size,0]),np.nanmean(masked[j:j+filter_size,i:i+filter_size,1]),np.nanmean(masked[j:j+filter_size,i:i+filter_size,2])])[0].name
    #         emoji_arr=np.array(Image.open(os.path.join(__location__, 'emojis/',image)))
            
    #         #when we truncate we round down, so we offset the right-left field by 1 to the right
    #         left=(j+(filter_size//2))-79
    #         if left<0:
    #             emoji_arr=emoji_arr[int(abs(left)):,:,:]
    #             left=0

    #         right=(j+(filter_size//2))+81
    #         if right>image_arr.shape[0]:
    #             emoji_arr=emoji_arr[:int(image_arr.shape[0]-right),:,:]
    #             right=image_arr.shape[0]

    #         top=(i+(filter_size//2))-79
    #         if top<0:
    #             emoji_arr=emoji_arr[:,int(abs(top)):,:]
    #             top=0

    #         bottom=(i+(filter_size//2))+81
    #         if bottom>image_arr.shape[1]:
    #             emoji_arr=emoji_arr[:,:int(image_arr.shape[1]-bottom),:]
    #             bottom=image_arr.shape[1]

    #         #open emoji as image
    #         img=Image.fromarray(emoji_arr)

    #         #make whitespace transparent
    #         img = img.convert("RGBA")
    #         datas = img.getdata()
    #         newData = []
    #         for item in datas:
    #             if item[0] == 255 and item[1] == 255 and item[2] == 255:
    #                 newData.append((255, 255, 255, 0))
    #             else:
    #                 newData.append(item)
    #         img.putdata(item)

    #         #paste images
    #         canvas_img.paste(img,(top,left),mask=img)
    canvas_img.show()

img_proc()