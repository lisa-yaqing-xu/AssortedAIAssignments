import pegSolitaireUtils
import config
import Queue
import math
import numpy

def ItrDeepSearch(pegSolitaireObject):

    #################################################
    # Must use functions:
    # getNextState(self,oldPos, direction)
    #
    # we are using this function to count,
    # number of nodes expanded, If you'll not
    # use this grading will automatically turned to 0
    #################################################
    #
    # using other utility functions from pegSolitaireUtility.py
    # is not necessary but they can reduce your work if you
    # use them.
    # In this function you'll start from initial gameState
    # and will keep searching and expanding tree until you
    # reach goal using Iterative Deepning Search.
    # you must save the trace of the execution in pegSolitaireObject.trace
    # SEE example in the PDF to see what to save
    #
    #################################################
    if pegSolitaireObject.isEndState():
        return True

    hasSolution = False  # do we have the solution yet
    max_depth = 1  # current max depth value, will be increment
      # is there at least 1 node that can reach the depth specified

    while (not hasSolution):
        c_depth = 0
        id_list = []
        path_list = []
        path_dir_list = []
        more_expand = {"val":False}
        move_up = False
        for i in range(max_depth):

            id_list.append(0)
            path_list.append([])
            path_dir_list.append([])
        ##print max_depth
        while True: #this was once a recursive function but python didn't like that once it got too deep
            ##print "========="
            ##print "current depth"+str(c_depth)
            ##print "max depth"+str(max_depth)
            ##print id_list
            ##print path_list
            ##print path_dir_list
            ##print "EXPAND MORE "+str(more_expand['val'])
            # if depth0 and maxdepth bigger than 0, and !moveup,
            # generate all possible first moves and put them into first layer path_list and their directions
            # and immediately go to first depth1 node, also save direction
            # if depth0 and moveup, return false
            # this is just to check if we started out with an already solved board
            # and thus don't have to do anything
            if c_depth == 0 and max_depth > 0:
                ##print "state 0"
                if move_up:
                    ##print "state 0.1"
                    break
                else:
                    pegSolitaireObject.findPossibleMoves(path_list[c_depth], path_dir_list[c_depth])
                    if len(path_list[c_depth]) > 0:
                        if max_depth == 1:
                            more_expand['val'] = True
                        c_depth += 1
                        continue
                    else:
                        break
            ##print "current node "+str(path_list[c_depth-1][id_list[c_depth-1]])
            # if we're at maxdepth, we check through all the sibling nodes (increment id list on each recursive call)
            # then after the last one idwise then we check the go up flag and decrease depth
            if c_depth == max_depth:
                ##print "state 1"
                pegSolitaireObject.getNextState(path_list[c_depth-1][id_list[c_depth-1]],path_dir_list[c_depth-1][id_list[c_depth-1]])
                if(pegSolitaireObject.isEndState()):
                    ##print "state 1.1"
                    hasSolution = True
                    break
                pegSolitaireObject.restoreLastState()
                if id_list[c_depth - 1] == len(path_list[c_depth - 1])-1:
                    ##print "state 1.2"
                    id_list[c_depth-1] = 0
                    path_list[c_depth-1][:] = []
                    path_dir_list[c_depth-1][:] = []
                    move_up = True
                    c_depth -= 1
                    continue
                id_list[c_depth-1] += 1
                continue
            # check if index at depth is same as the last index, if so, remove all elements out of path_list/dir
            # at the equal level and keep going up and check the moveup flag
            # call revert-state here
            if id_list[c_depth - 1] == len(path_list[c_depth - 1]) - 1 and move_up:
                ##print "state 3"
                id_list[c_depth - 1] = 0
                path_list[c_depth - 1][:] = []
                path_dir_list[c_depth - 1][:] = []
                pegSolitaireObject.restoreLastState()
                c_depth -= 1
                continue
            # if depth greater than 0 but smaller than maxdepth and we're not at maxindex and moveup is checked
            # because we came up from a deeper depth, then increment index on current level and uncheck moveup
            if c_depth > 0 and c_depth < max_depth:
                ##print "state 4"
                if id_list[c_depth - 1] < len(path_list[c_depth - 1]) - 1 and move_up:
                    ##print "state 4.1"
                    pegSolitaireObject.restoreLastState()
                    id_list[c_depth - 1] += 1
                    move_up = False
                pegSolitaireObject.getNextState(path_list[c_depth-1][id_list[c_depth-1]],path_dir_list[c_depth-1][id_list[c_depth-1]])
                pegSolitaireObject.findPossibleMoves(path_list[c_depth], path_dir_list[c_depth])
                if c_depth == max_depth-1:
                    more_expand['val'] = more_expand['val'] or len(path_list[c_depth]) > 0
    
                if len(path_list[c_depth]) == 0: #found nothing
                    ##print "state 4.2"
                    pegSolitaireObject.restoreLastState()
                    if id_list[c_depth - 1] == len(path_list[c_depth - 1]) - 1: #last one in its depth too
                        ##print "state 4.2.1"
                        move_up = True
                        id_list[c_depth-1] = 0
                        path_list[c_depth-1][:] = []
                        path_dir_list[c_depth-1][:] = []
                        c_depth -= 1
                        continue
                    else:
                        ##print "state 4.2.2"
                        id_list[c_depth - 1] += 1
                        continue
                c_depth += 1
                continue
            # whether or not we backtracked or not, if we're not at maxdepth and moveup is unchecked, we expand that node and
            # find all the possible next moves


        if not more_expand['val']:
            print "NO ANSWER FOUND"
            break
        else : #okay so I totally misunderstood the trace and only recorded the from coordinates
            ll = len(pegSolitaireObject.trace) #but I'm not rewriting the algo
            for i in range(ll): # so I'll just merge in the dir
                l = ll-i-1
                t = pegSolitaireObject.trace[l]
                d = pegSolitaireObject.trace_dir[l]
                pegSolitaireObject.trace.insert(l+1,(t[0]+2*d[0],t[1]+2*d[1]))

        max_depth += 1

def distance(p0,p1): #this will be used for f(n)
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def countPegs(gs):
    pegs = 0;
    for i in range(7):
        pegs+=gs[i].count(1)
    return pegs

def aStar(pegSolitaireObject, heuristic):
    # I'm going to write one AStar base algo and just 2 plug-in heuristics
    # because I don't like repeating code anyway
    if pegSolitaireObject.isEndState(): #if it starts at the end state i'm not even gonna bother running the loop
        print "STARTED AT THE END STATE"
        return True
    pq = Queue.PriorityQueue(0) #start with priority queue
    #setup heuristic calculations here so i can just plug them in
    corner = [(2,0),(4,0),(0,2),(0,4),(2,6),(4,6),(6,2),(4,2)]
    def heuristic1(gs,node,dir,prev_weight): # weighted by number of isolated pegs after the move
        iso_peg = 0;
        for i in range(7):
            for j in range(7):
                iso = True;
                if (i <= 1 and j <= 1) or (i <= 1 and j >= 5) or (i >= 5 and j <= 1) or (i >=5 and j>=5):
                    continue #these are the -1 sections, so just skip over
                if i > 0: # at a location with a peg (1), check for the peg has other pegs next to it
                    iso = iso and gs[i][j] == 1 and not gs[i-1][j] == 1 #using and operator, at any point a peg has another
                if i < 6:
                    iso = iso and gs[i][j] == 1 and not gs[i+1][j] == 1 #peg next to it, then it is not isolated and it will be false
                if j > 0:
                    iso = iso and gs[i][j] == 1 and not gs[i][j-1] == 1
                if j < 6:
                    iso = iso and gs[i][j] == 1 and not gs[i][j+1] == 1

                if iso:
                    iso_peg+=1
        return prev_weight+iso_peg*3#+distance((node[0]+2*dir[0],node[1]+2*dir[1]),(3,3))
        #i was gonna also use distance to center but that actually slows it down than if i just use the h(n) here so
        #the isolated peg h(n) by 2-3x resulted in best runtimes

    def heuristic2(gs,node,dir,prev_weight): #corner pegs left
        numcorners = 0;
        for i in range(8):
            numcorners += (gs[corner[i][0]][corner[i][1]] == 1)

        return prev_weight+numcorners#+distance((node[0]+2*dir[0],node[1]+2*dir[1]),(3,3))
        #weighting the num of corners heavier gives a generally faster execution time and less nodes expanded



    init_list = []
    init_list_dir = []
    pegSolitaireObject.findPossibleMoves(init_list,init_list_dir)

    # this basically pushes child nodes to the priority queue
    # pass in the pegsolitare game object, any information about the parent tree and the gamestate of the parent
    def pushChildren(pegSolitaireObject, parentgs, parentweight, parentlist, parentdirs, nodelist, nodelist_dir):
        for i in range(len(nodelist)):
            nodes = [] #make copies of everything since I plan on appending data in here, so the original is not changed
            nodes[:]= parentlist #although honestly this is also my first time writing python so I have no idea how
            nodes_dir = [] #python handles memory management
            nodes_dir[:] = parentdirs #help
            nodes.append(nodelist[i])
            nodes_dir.append(nodelist_dir[i]) #anyway i keep track of directions too so i can revert states/calc dist/ check answers by hand
            pegSolitaireObject.gameState = pegSolitaireObject.copyGameState(parentgs) #make copies so i can save the state
            pegSolitaireObject.getNextState(nodelist[i],nodelist_dir[i])
            gs = pegSolitaireObject.copyGameState(pegSolitaireObject.gameState);
            move = {"nodes": nodes, "direction": nodes_dir, "gameState": gs} #this gets pushed into the pq
            weight = 0;
            if heuristic ==1: #do heuristic
                weight = heuristic1(gs,nodelist[i],nodelist_dir[i],parentweight)
            elif heuristic ==2:
                weight = heuristic2(gs,nodelist[i],nodelist_dir[i],parentweight)
            pegSolitaireObject.restoreLastState(); #go back to the last state for the next sibling
            node = (weight,move) # put into pq
            pq.put(node)

    pushChildren(pegSolitaireObject,pegSolitaireObject.gameState,0,[],[],init_list,init_list_dir) # put in init states

    solved = False
    while not pq.empty(): #A* loop
        head = pq.get() # pop head of priority queue
        pegSolitaireObject.gameState = head[1]["gameState"]
       # print head[1]["nodes"]
        if pegSolitaireObject.isEndState(): #if winning
            solved = True
            pegSolitaireObject.trace = head[1]["nodes"]
            pegSolitaireObject.trace_dir = head[1]["direction"]
            ll = len(pegSolitaireObject.trace) #see iterative deepening search one
            for i in range(ll):
                l = ll-i-1
                t = pegSolitaireObject.trace[l]
                d = pegSolitaireObject.trace_dir[l]
                pegSolitaireObject.trace.insert(l+1,(t[0]+2*d[0],t[1]+2*d[1]))
            break
        #else expandchild

        children = []
        children_dir = []
        pegSolitaireObject.findPossibleMoves(children,children_dir)

        #calculate each child heuristic value and add w
        #push them to the priority queue
        pushChildren(pegSolitaireObject,head[1]["gameState"],head[0],head[1]["nodes"],head[1]["direction"],children,children_dir)

    if not solved:
        print "NO ANSWER FOUND"
    return True

def aStarOne(pegSolitaireObject):
    #################################################
    # Must use functions:
    # getNextState(self,oldPos, direction)
    #
    # we are using this function to count,
    # number of nodes expanded, If you'll not
    # use this grading will automatically turned to 0
    #################################################
    #
    # using other utility functions from pegSolitaireUtility.py
    # is not necessary but they can reduce your work if you
    # use them.
    # In this function you'll start from initial gameState
    # and will keep searching and expanding tree until you
    # reach goal using A-Star searching with first Heuristic
    # you used.
    # you must save the trace of the execution in pegSolitaireObject.trace
    # SEE example in the PDF to see what to return
    #
    #################################################
    aStar(pegSolitaireObject,1)
    return True


def aStarTwo(pegSolitaireObject):
    #################################################
    # Must use functions:
    # getNextState(self,oldPos, direction)
    #
    # we are using this function to count,
    # number of nodes expanded, If you'll not
    # use this grading will automatically turned to 0
    #################################################
    #
    # using other utility functions from pegSolitaireUtility.py
    # is not necessary but they can reduce your work if you
    # use them.
    # In this function you'll start from initial gameState
    # and will keep searching and expanding tree until you
    # reach goal using A-Star searching with second Heuristic
    # you used.
    # you must save the trace of the execution in pegSolitaireObject.trace
    # SEE example in the PDF to see what to return
    #
    #################################################
    aStar(pegSolitaireObject,2)
    return True
