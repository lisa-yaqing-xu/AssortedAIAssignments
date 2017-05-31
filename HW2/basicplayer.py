from util import memoize, run_search_function

basic_statistics = [0,0]
def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score


def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass

def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()


def minimax(board, depth, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    import sys,time
    t = time.time(); #start timer
    n = [0] #this keeps track of nodes
    col = 0 #this is the starting column
    startdepth = depth; #keep track of start depth for win state checking
    def minimax_helper(board,depth,is_max,eval_fn,get_next_moves_fn,is_terminal_fn): #actual recursive function to min_max
        if(is_terminal_fn(depth,board)): #if this is a terminal state, whether by means of end depth or just someone won
            return eval_fn(board) #get eval
        if(is_max):
            best = -sys.maxint-1 #smallest int, practically infinity
            bestcol = 0 #keep track of the column
            for b in get_next_moves_fn(board): #iterate through the generator
                n[0]+=1; #add to node expansion count
                if(depth == startdepth and b[1].longest_chain(board.get_current_player_id())>=board.win_streak): #check win state
                    return b[0]; #if win state, straight return the col. No point in dawdling around
                eval = minimax_helper(b[1],depth-1,False,eval_fn,get_next_moves_fn,is_terminal_fn) #recursive call to get values
                if(best < eval): #if evaluated is better than best
                    best = eval; #then sub in the new evaluation for best
                    bestcol = b[0] #save column
            if(depth == startdepth): #if we at starting level of depth again, return the column as a result
                return bestcol;
            else:
                return best; #otherwise just keep on returning the eval up the recursion tree
        else: #min case, not gonna comment the rest because it's literally the same but with signs reversed.
            best = sys.maxint;
            bestcol = 0
            for b in get_next_moves_fn(board):
                n[0]+=1;
                if(depth == startdepth and b[1].longest_chain(board.get_current_player_id())>=board.win_streak):
                    return b[0];
                eval = minimax_helper(b[1],depth-1,True,eval_fn,get_next_moves_fn,is_terminal_fn) #all it does is just reverse the max/min field, really
                if(best > eval):
                    best = eval;
                    bestcol = b[0]
            if(depth == startdepth):
                return bestcol;
            else:
                return best;

    col = minimax_helper(board,depth,True,eval_fn,get_next_moves_fn,is_terminal_fn)
    elapsed_time = time.time() - t;

    print("%s seconds elapsed"%elapsed_time);
    print("%s nodes expanded"%n[0]);

    basic_statistics[0] += elapsed_time;
    basic_statistics[1] += n[0]
    return col



def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]


def new_evaluate(board):
    if board.is_game_over():
        #check for loss
        score = -1000
    else:
        delimiter = 1; #this is added to accomodate the longest running game mode, else it gets boring fast.
        multiplier = 1;
        if(board.game_mode == "longest"):
            delimiter = 3;
            multiplier = 2;
        # Have some consideration about survival; longest chain from the other player is also bad, so that's considered
        score = board.longest_chain(board.get_current_player_id()) * 10 - board.longest_chain(board.get_other_player_id())*5
        for row in range(6): # the centering algorithm makes sense, I kept it
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)
        if(board.longest_chain(board.get_current_player_id()) >= board.win_streak-delimiter): #significantly increase weight of almost winning
            score += 10
            score *= 2
        if(board.longest_chain(board.get_current_player_id()) >= board.win_streak-delimiter+1): #drastically increase weight of potentially winning
            score += 50
            score *= 5
        if(board.longest_chain(board.get_other_player_id()) >= board.win_streak-delimiter): #but it's bad if the other player almost win
            score -=100*multiplier
        if(board.longest_chain(board.get_other_player_id()) >= board.win_streak-delimiter+1): #and super bad if they can win too
            score -=500*multiplier
    return score



random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)
