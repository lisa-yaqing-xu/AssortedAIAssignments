###########################################
# you need to implement five funcitons here
###########################################
import copy
import random
def backtracking(filename):
    ###
    # use backtracking to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    startdata = readGameFile(filename); #read in file
    n = startdata['N']; #dimensions
    m = startdata['M'];
    k = startdata['K'];

    validboard = checkBoardIsValid(startdata['init_state'],n,m,k) #prelim checks of board is actually valid and not a troll board
    if not validboard:
        return ([[],[]], 0)
    consistency = {'val':0};

    def backtrack(board,row,col,n,m,k): #recursive backtracking algo
        newboard = copyState(board);
        if(newboard[row][col] == '-'):
            for i in range(1,n+1):
                newboard[row][col] = i;
                v = checkConsistency(newboard,row,col,n,m,k)
                consistency['val']+=1
                if v:
                    if col < n-1:
                        ret = backtrack(newboard,row,col+1,n,m,k) #catch return value
                        if ret:
                            return ret #if there's a value in there, return it
                        else:
                            continue #else dont
                    elif row < n-1:
                        ret = backtrack(newboard,row+1,0,n,m,k)
                        if ret:
                            return ret
                        else:
                            continue
                    else:
                        return newboard; # this is at the end of the board, return whatever's there since this already passed validity checks
        else: # this is if there's already values in
            if col < n-1:
                return backtrack(newboard,row,col+1,n,m,k)
            elif row < n-1:
                return backtrack(newboard,row+1,0,n,m,k)
            else:
                return newboard; #end of board etc
    board = backtrack(startdata['init_state'],0,0,n,m,k);

    return (board, consistency['val'])

def backtrackingMRV(filename):
    ###
    # use backtracking + MRV to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    startdata = readGameFile(filename);
    n = startdata['N'];
    m = startdata['M'];
    k = startdata['K'];

    validboard = checkBoardIsValid(startdata['init_state'],n,m,k)
    const = getConstraints(startdata['init_state'],n,m,k) # construct constraints matrix
    const_cells = const["cells"] #make copy of this too, since im going to just straight up remove things when they're used
    constraints = const["constraints"]
    if not validboard:
        return ([[],[]], 0)

    consistency = {'val':0};

    init_cell = mrv_heuristic(const_cells,constraints,n,m,k);

    def backtrack(board,cell,cells_left,const_matrix,n,m,k,depth): #modified backtrack algo
        newboard = copyState(board)
        const = const_matrix
        cl = cells_left[:]
        cl.remove(cell)
        next = False;
        if(len(cl) > 0):
            next = mrv_heuristic(cl,const,n,m,k)
        assignments = const[cell[0]][cell[1]][:]
        while len(assignments) >= 0: #instead of iterating through the entire grid, just whatver assignments on this one constraint
            if len(assignments) == 0:
                return False;
            i = assignments[0]
            newboard[cell[0]][cell[1]] = i
            v = checkConsistency(newboard,cell[0],cell[1],n,m,k)
            consistency['val']+=1
            if v:
                if not next:
                    return newboard
                else:
                    ret = backtrack(newboard,next,cl,const,n,m,k,depth+1) # go to the next constrained variable
                    if ret:
                        return ret
                    else:
                        assignments.remove(i)
            else:
                assignments.remove(i)
    board = []
    board = backtrack(startdata['init_state'],init_cell,const_cells,constraints,n,m,k,1)
    return (board, consistency['val'])

def backtrackingMRVfwd(filename):
    ###
    # use backtracking +MRV + forward propogation
    # to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    startdata = readGameFile(filename);
    n = startdata['N'];
    m = startdata['M'];
    k = startdata['K'];
    validboard = checkBoardIsValid(startdata['init_state'],n,m,k)
    const = getConstraints(startdata['init_state'],n,m,k) # construct constraints matrix
    const_cells = const["cells"] #make copy of this too, since im going to just straight up remove things when they're used
    constraints = const["constraints"]
    if not validboard:
        return ([[],[]], 0)
    consistency = {'val':0};

    def forward_check(cell,const,val,n,m,k):
        const_m = const;
        for i in range (0,n):
            row_n = const_m[cell[0]][i];
            if(val in const_m[cell[0]][i] and not i == cell[1]):
                row_n.remove(val)
                l = len(row_n);
                if l== 0:
                    return False # if any empty slots on row check, return false
            col_n = const_m[i][cell[1]];
            if(val in col_n and not i == cell[0]):
                col_n.remove(val)
                l = len(col_n);
                if l== 0:
                    return False #empty slots on col check
            rc = getCellRC(cell[0],cell[1],n,m,k)
            cellr = rc['rows'][int(i/k)];
            cellc = rc['cols'][int(i%k)];
            cell_n = const_m[cellr][cellc];
            if(val in cell_n and not cellc == cell[1] and not cellr == cell[0]):
                cell_n.remove(val);
                l = len(cell_n)
                if l== 0:
                    return False #empty slots on block check
        return True
    init_cell = mrv_heuristic(const_cells,constraints,n,m,k);

    def backtrack(board,cell,cells_left,const_matrix,n,m,k,depth): #basically the same as standard mrv using both forward checking and consistency to check
        newboard = copyState(board)
        const = copy.deepcopy(const_matrix)
        cl = cells_left[:]
        #print(cl)
        cl.remove(cell)
        #print(cell)
        next = False;
        if(len(cl) > 0):
            next = mrv_heuristic(cl,const,n,m,k)
        #print(next)
        assignments = const[cell[0]][cell[1]][:]
        while len(assignments) >= 0:
            if len(assignments) == 0:
                return False;
            #print(depth)
            #print(assignments)
            i = assignments[0]
            newboard[cell[0]][cell[1]] = i
            #print("start foward check")
            const_m = copy.deepcopy(const)
            v = forward_check(cell,const_m,i,n,m,k)
            v_2 = checkConsistency(newboard,cell[0],cell[1],n,m,k)
            consistency['val']+=1
            if v and v_2:
                if not next:
                    return newboard
                else:
                    ret = backtrack(newboard,next,cl,const_m,n,m,k,depth+1)
                    if ret:
                        return ret
                    else:
                        assignments.remove(i)
            else:
                assignments.remove(i)
    board = []
    board = backtrack(startdata['init_state'],init_cell,const_cells,constraints,n,m,k,1)
    return (board, consistency['val'])

def backtrackingMRVcp(filename):
    ###
    # use backtracking + MRV + cp to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    startdata = readGameFile(filename);
    n = startdata['N'];
    m = startdata['M'];
    k = startdata['K'];
    validboard = checkBoardIsValid(startdata['init_state'],n,m,k)

    const = getConstraints(startdata['init_state'],n,m,k) # construct constraints matrix
    const_cells = const["cells"] #make copy of this too, since im going to just straight up remove things when they're used
    constraints = const["constraints"]
    if not validboard:
        return ([[],[]], 0)
    #print("board is valid")
    #for i in range(0,startdata['N']):
        #print(startdata['init_state'][i])
        #print(constraints[i])
        #print(const_cells)
    consistency = {'val':0};

    def const_prop(cell,const,val,n,m,k): #similar algo to forward check except it goes into more detail,
    # if there's anything that would constrain another, it would get checked too. No wonder it's slower lol
        const_m = const;
        for i in range (0,n):
            row_n = const_m[cell[0]][i];
            if(val in const_m[cell[0]][i] and not i == cell[1]):
                row_n.remove(val)
                l = len(row_n);
                if l == 1:
                    return const_prop((cell[0],i),const_m,row_n[0],n,m,k)
                elif l== 0:
                    return False
            col_n = const_m[i][cell[1]];
            if(val in col_n and not i == cell[0]):
                col_n.remove(val)
                l = len(col_n);
                if l == 1:
                    return const_prop((i,cell[1]),const_m,col_n[0],n,m,k)
                elif l== 0:
                    return False
            rc = getCellRC(cell[0],cell[1],n,m,k)
            cellr = rc['rows'][int(i/k)];
            cellc = rc['cols'][int(i%k)];
            cell_n = const_m[cellr][cellc];
            if(val in cell_n and not cellc == cell[1] and not cellr == cell[0]):
                cell_n.remove(val);
                l = len(cell_n)
                if l == 1:
                    return const_prop((cellr,cellc),const_m,cell_n[0],n,m,k)
                elif l== 0:
                    return False
        return True
    init_cell = mrv_heuristic(const_cells,constraints,n,m,k);

    def backtrack(board,cell,cells_left,const_matrix,n,m,k,depth): #same thing really
        #print("depth%s"%depth)
        newboard = copyState(board)
        const = copy.deepcopy(const_matrix)
        cl = cells_left[:]
        #print(cl)
        cl.remove(cell)
        #print(cell)
        next = False;
        if(len(cl) > 0):
            next = mrv_heuristic(cl,const,n,m,k)
        #print(next)
        assignments = const[cell[0]][cell[1]][:]
        while len(assignments) >= 0:
            if len(assignments) == 0:
                return False;
            #print(depth)
            #print(assignments)
            i = assignments[0]
            newboard[cell[0]][cell[1]] = i
            #print("start foward check")
            const_m = copy.deepcopy(const);
            v = const_prop(cell,const_m,i,n,m,k)
            v_2 = checkConsistency(newboard,cell[0],cell[1],n,m,k)
            consistency['val']+=1
            if v and v_2:
                if not next:
                    return newboard
                else:
                    ret = backtrack(newboard,next,cl,const_m,n,m,k,depth+1)
                    if ret:
                        return ret
                    else:
                        assignments.remove(i)
            else:
                assignments.remove(i)
    board = []
    board = backtrack(startdata['init_state'],init_cell,const_cells,constraints,n,m,k,1)
    return (board, consistency['val'])




def minConflict(filename):
    ###
    # use minConflict to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    startdata = readGameFile(filename);
    n = startdata['N'];
    m = startdata['M'];
    k = startdata['K'];
    validboard = checkBoardIsValid(startdata['init_state'],n,m,k)

    const = getConstraints(startdata['init_state'],n,m,k) # construct constraints matrix
    const_cells = const["cells"] #make copy of this too, since im going to just straight up remove things when they're used
    constraints = const["constraints"]
    if not validboard:
        return ([[],[]], 0)
    consistency = {'val':0};

    def minimize_conflict(cell,const_m,n,m,k): #basically checks for in row, col, block
        #if the number of constrained blocks that share the same values, and go for the least occuring value
        #print(cell)
        c_const = const_m[cell[0]][cell[1]];
        leastConf = n+1;
        least = n*3
        for val in c_const:
            count = 0;
            for i in range (0,n):
                row_n = const_m[cell[0]][i];
                if(val in row_n):
                    count += 1;
                col_n = const_m[i][cell[1]];
                if(val in col_n):
                    count += 1;
                rc = getCellRC(cell[0],cell[1],n,m,k)
                cellr = rc['rows'][int(i/k)];
                cellc = rc['cols'][int(i%k)];
                cell_n = const_m[cellr][cellc];
                if(val in cell_n):
                    count+=1;
            if(count < least):
                least = count;
                leastConf = val;
        c_const = [val];
        return val;

    def min_conf(board,const_cells,const,it,n,m,k):
        init_len = len(const_cells) #max iterations be the # of cells that require a set of constraints * j times
        j = it;
        oneit = False
        while j > 0:
            const_c = const_cells[:]
            const_m = copy.deepcopy(const)
            for i in range(0,init_len):
                rand = random.randint(0,len(const_c)-1);
                #print(const_c)
                #print(rand)
                next = const_c[rand];
                const_c.remove(next);
                val = minimize_conflict(next,const_m,n,m,k)
                board[next[0]][next[1]] = val;
                if ((i == init_len-1 or oneit)):
                    v = checkBoardIsValid(board,n,m,k)
                    consistency['val']+=1
                    if v:
                        return board
            oneit = True;
            j-=1
        return False;
    board = min_conf(startdata['init_state'],const_cells,constraints,5,n,m,k);
    return (board, consistency['val'])

def readGameFile(filename):
    #general initial gamestate reader, based on HW1's gamestate reader
    fileHandle = open(filename, 'r')
    size = fileHandle.readline().strip().split(';')[0].split(',');
    start_array = [];

    for i in range (0,len(size)):
        size[i]=int(size[i]);
    for i in range (0,size[0]):
        line = fileHandle.readline().strip().split(';')[0];
        line = line.split(',');
        for j in range (0,len(line)):
            if(line[j] != '-'):
                line[j]=int(line[j]);
        start_array.append(line)

    return {'init_state':start_array, 'N':size[0], 'M':size[1], 'K':size[2]}

def copyState(s):
    state = [row[:] for row in s]
    return state

def checkConsistency(board, row, col, n,m,k):
    #row check and col check
    for i in range(0,n):
        if(i != col and board[row][i] == board[row][col]): # and board[row][col] != '-'
            return False
        if(i != row and board[i][col] == board[row][col]):
            return False
    #print("pass row/col, starting rc check")
    #cell check
    rc = getCellRC(row,col,n,m,k);
    #print(rc)
    for r in rc['rows']:
        for c in rc['cols']:
            if(r == row and c == col):
                continue
            elif (board[r][c] == board[row][col]):
                #print(board[r][c])
                return False
            #print(board[r][c])
   # print("pass rc")
    return True

def checkBoardIsValid(board,n,m,k): #generally only used for init
    for r in range(0,n):
        for c in range(0,n):
            if board[r][c] == '-':
                continue;
            if checkConsistency(board,r,c,n,m,k) == False:
                return False
    return True

def getCellRC(r,c,n,m,k):
    rows = []
    cols = []
    rowquad = int(r/m);
    colquad = int(c/k);
    rows.append(rowquad*m);
    cols.append(colquad*k);
    for i in range(1,m):
        rows.append(rows[i-1]+1)
    for i in range(1,k):
        cols.append(cols[i-1]+1);
    return {'rows':rows,'cols':cols}

def getConstraints(board,n,m,k):
    constraints = [];
    constrained_cells = []
    for i in range(0,n):
        constraints.append([]) #rows
        for j in range (0,n):
            if board[i][j] != '-':
                constraints[i].append([board[i][j]])
            else:
                constrained_cells.append((i,j));
                constraints[i].append(range(1,n+1));
                for x in range(0,n):
                    #check row
                    if(board[i][x] != '-' and board[i][x] in constraints[i][j]):
                        constraints[i][j].remove(board[i][x]);
                    #check col
                    if(board[x][j] != '-' and board[x][j] in constraints[i][j]):
                       constraints[i][j].remove(board[x][j]);
                    #check cells
                    rc = getCellRC(i,j,n,m,k);
                    #print(rc)
                    #print(x)
                    #print("cell r%s c%s"%(int(x/k),int(x%k)))
                    cellr = rc['rows'][int(x/k)];
                    cellc = rc['cols'][int(x%k)];
                    #print ("check r%s c%s"%(cellr,cellc) )
                    if(board[cellr][cellc] != '-' and board[cellr][cellc] in constraints[i][j]):
                        constraints[i][j].remove(board[cellr][cellc]);

    return {'constraints':constraints,'cells':constrained_cells}

def mrv_heuristic(cells,constraints,n,m,k): # mrv
    vals = n;
    ind = 0
    for i in range(0,len(cells)):
        xr = cells[i][0];
        yc = cells[i][1];
        if(len(constraints[xr][yc]) < vals):
            vals =len(constraints[xr][yc])
            ind = i
    return cells[ind] #basically goes through the cells with constraints and finds one with the least

def printboard(board):
    for b in board:
        print(b)