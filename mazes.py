from keras.utils import Progbar
import numpy as np

class Maze:
    class Node:
        def __init__(self, position):
            self.Position = position
            self.Neighbours = [None, None, None, None]
            #self.Weights = [0, 0, 0, 0]

    def __init__(self, im):
        
        width = im.size[0]
        height = im.size[1]
        
        kk=Progbar(target=(width-2)*(height-2))
        
        data = list(im.getdata(0))
        lastNode= None

        self.start = None
        self.end = None

        # Top row buffer
        topnodes = [None] * width
        count = 0

        # Start row
        for x in range (1, width - 1):
            if data[x] > 0:
                self.start = Maze.Node((0,x))
                topnodes[x] = self.start
                count += 1
                break

        for y in range (1, height - 1):
            #print ("row", str(y)) # Uncomment this line to keep a track of row progress

            rowoffset = y * width
            rowaboveoffset = rowoffset - width
            rowbelowoffset = rowoffset + width

            # Initialise previous, current and next values
            prv = False
            cur = False
            nxt = data[rowoffset + 1] > 0

            leftnode = None

            for x in range (1, width - 1):
                kk.add(1)
                # Move prev, current and next onwards. This way we read from the image once per pixel, marginal optimisation
                prv = cur
                cur = nxt
                nxt = data[rowoffset + x + 1] > 0

                n = None

                if cur == False:
                    # ON WALL - No action
                    continue

                if prv == True:
                    if nxt == True:
                        # PATH PATH PATH
                        # Create node only if paths above or below
                        if data[rowaboveoffset + x] > 0 or data[rowbelowoffset + x] > 0:
                            n = Maze.Node((y,x))
                            leftnode.Neighbours[1] = n
                            n.Neighbours[3] = leftnode
                            leftnode = n
                            lastNode = n
                    else:
                        # PATH PATH WALL
                        # Create path at end of corridor
                        n = Maze.Node((y,x))
                        leftnode.Neighbours[1] = n
                        n.Neighbours[3] = leftnode
                        leftnode = None
                        lastNode = n
                else:
                    if nxt == True:
                        # WALL PATH PATH
                        # Create path at start of corridor
                        n = Maze.Node((y,x))
                        leftnode = n
                        lastNode = n
                    else:
                        # WALL PATH WALL
                        # Create node only if in dead end
                        if (data[rowaboveoffset + x] == 0) or (data[rowbelowoffset + x] == 0):
                            #print ("Create Node in dead end")
                            n = Maze.Node((y,x))
                            lastNode = n

                # If node isn't none, we can assume we can connect N-S somewhere
                if n != None:
                    # Clear above, connect to waiting top node
                    if (data[rowaboveoffset + x] > 0):
                        t = topnodes[x]
                        t.Neighbours[2] = n
                        n.Neighbours[0] = t

                    # If clear below, put this new node in the top row for the next connection
                    if (data[rowbelowoffset + x] > 0):
                        topnodes[x] = n
                    else:
                        topnodes[x] = None

                    count += 1

        self.NodeList=[]
        templist=[lastNode]
        visited=[lastNode.Position]
        kk=Progbar(target=(np.sum(np.array(im))*1.5)//255)
        #fig=plt.figure()?
        while templist!=[]:
            node=templist.pop()
            kk.add(1)
            for neigh in [k for k in node.Neighbours if k != None and (k.Position not in visited) and (k not in templist)]:
                templist.append(neigh)
                visited.append(neigh.Position)
        
            self.NodeList.append((node.Position,node))
        
        self.NodeList=dict(self.NodeList)
        self.count = count
        self.width = width
        self.height = height