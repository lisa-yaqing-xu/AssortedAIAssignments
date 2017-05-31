import readGame
import config

#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_wall(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################
end_state = [[-1, -1, 0, 0, 0, -1, -1], [-1, -1, 0, 0, 0, -1, -1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0], [-1, -1, 0, 0, 0, -1, -1], [-1, -1, 0, 0, 0, -1, -1]]


class game:
    def __init__(self, filePath):
        self.gameState = readGame.readGameState(filePath)
        self.nodesExpanded = 0
        self.initState = self.copyGameState(self.gameState)
        self.trace = []
        self.trace_dir = []  # direction of the move, to restore last gamestate

    def is_corner(self, pos):
        if pos[0] < 0 or pos[0] > 6 or pos[1] < 0 or pos[1] > 6:
            return True
        ########################################
        # You have to make changes from here
        # check for if the new positon is a corner or not
        # return true if the position is a corner
        return self.gameState[pos[0]][pos[1]] == -1

    def getNextPosition(self, oldPos, direction):
        #########################################
        # YOU HAVE TO MAKE CHANGES HERE
        # See DIRECTION dictionary in config.py and add
        # this to oldPos to get new position of the peg if moved
        # in given direction , you can remove next line
        a = oldPos[0] + direction[0]
        b = oldPos[1] + direction[1]
        return (a,b);

    def is_validMove(self, oldPos, direction):
        #########################################
        # DONT change Things in here
        # In this we have got the next peg position and
        # below lines check for if the new move is a corner
        newPos = self.getNextPosition(oldPos, direction)
        if self.is_corner(newPos):
            return False
        #########################################

        ########################################
        # YOU HAVE TO MAKE CHANGES BELOW THIS
        # check for cases like:
        # if new move is already occupied
        # or new move is outside peg Board
        # Remove next line according to your convenience

        if newPos[0] < 0 or newPos[0] > 6 or newPos[1] < 0 or newPos[1] > 6:  # outside the board
            return False
        if self.gameState[oldPos[0]][oldPos[1]] == 1 and self.gameState[newPos[0]][newPos[1]] == 1:  # has peg to jump over
            newPos = self.getNextPosition(newPos, direction);
            if newPos[0] < 0 or newPos[0] > 6 or newPos[1] < 0 or newPos[1] > 6:  # check if it's outside the board now
                return False  # nope.avi
            if self.gameState[newPos[0]][newPos[1]] == 0:  # cool, it's empty
                return True

        return False

    def getNextState(self, oldPos, direction):
        ###############################################
        # DONT Change Things in here
        self.nodesExpanded += 1
        if not self.is_validMove(oldPos, direction):
            print "Error, You are not checking for valid move"
            exit(0)
        ###############################################
        ###############################################
        # YOU HAVE TO MAKE CHANGES BELOW THIS
        # Update the gameState after moving peg
        # eg: remove crossed over pegs by replacing it's
        # position in gameState by 0
        # and updating new peg position as 1

        self.gameState[oldPos[0]][oldPos[1]] = 0  # the one to move
        newPos = self.getNextPosition(oldPos, direction);  # the one to delete
        self.gameState[newPos[0]][newPos[1]] = 0
        newPos = self.getNextPosition(newPos, direction);  # the one to fill
        self.gameState[newPos[0]][newPos[1]] = 1

        self.trace.append(oldPos);
        self.trace_dir.append(direction);

        return self.gameState


    def isEndState(self):
        if self.gameState == end_state:
            return True;
        # checks for endstate
        return False

    def copyGameState(self, gs):
        state = [row[:] for row in gs]
        return state

    def restoreLastState(self):
        oldPos = self.trace.pop()
        direction = self.trace_dir.pop()

        self.gameState[oldPos[0]][oldPos[1]] = 1  # put it back
        newPos = self.getNextPosition(oldPos, direction);  # put this one back too
        self.gameState[newPos[0]][newPos[1]] = 1
        newPos = self.getNextPosition(newPos, direction);  # empty again
        self.gameState[newPos[0]][newPos[1]] = 0

        return True

    def findPossibleMoves(self, list, list_dir):
        dirs = [config.DIRECTION.get('N'), config.DIRECTION.get('S'), config.DIRECTION.get('E'),
                config.DIRECTION.get('W')]
        for i in range(7):
            for j in range(7):
                pos = (i,j)
                for k in range(4):
                    if (self.is_validMove(pos, dirs[k])):
                        list.append(pos)
                        list_dir.append(dirs[k])

        return
