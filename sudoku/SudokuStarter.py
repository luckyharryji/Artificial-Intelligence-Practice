#!/usr/bin/env python
import struct, string, math
import copy

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""

    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)


    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val

    return board

def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)



def solve(initial_board, forward_checking = False, MRV = False, Degree = False,
    LCV = False, MCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """

    # res = []
    count = 0

    status_space = initial_status_space(initial_board, forward_checking)

    result, after_count = solve_helper_new(initial_board, status_space, forward_checking, MRV, MCV, LCV, count)

    if not result:
        print "No Solution"
    return result


def solve_helper_new(initial_board, status_space, forward_checking, MRV, MCV, LCV, count):
    #if the board is complete, the puzzle is solved
    if is_complete(initial_board):
        return initial_board, count

    next_row, next_col = find_next_pos_new(initial_board, status_space, forward_checking, MRV, MCV, LCV)

    if next_row == None or next_col == None:
        return initial_board
        if is_complete(initial_board):
            return initial_board, count
        else:
            return None, count

    if LCV:
        temp_domain_list = LCV_helper(initial_board, status_space, next_row, next_col)
    else:
        temp_domain_list = status_space[str(next_row) + ',' + str(next_col)]
    if temp_domain_list:
        for value in temp_domain_list:
            if (not forward_checking and is_legal(initial_board, next_row, next_col, value)) or (LCV and is_legal(initial_board, next_row, next_col, value)) or (forward_checking and not LCV):
                temp_board = copy.deepcopy(initial_board)
                temp_board.set_value(next_row, next_col, value)
                count += 1

                temp_status_space = copy.deepcopy(status_space)
                if forward_checking:
                    temp_status_space = forward_checking_helper(initial_board, temp_status_space, next_row, next_col, value)

                result, count = solve_helper_new(temp_board, temp_status_space, forward_checking, MRV, MCV, LCV, count)

                if result != None:
                    return result, count
    return None, count


def is_legal(initial_board, row, col, val):
    '''
    Decide if it is leagel to set val in [row, col] for board
    '''
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    for i in range(initial_board.BoardSize):
        if ((BoardArray[row][i] == val) and i != col):
            return False
        if ((BoardArray[i][col] == val) and i != row):
            return False
    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
        for j in range(subsquare):
            if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] == val)
                and (SquareRow*subsquare + i != row)
                and (SquareCol*subsquare + j != col)):
                    return False
    return True


def initial_status_space(initial_board, forward_checking):
    '''
    Initial the reamaining value for the board
    '''
    board = initial_board.CurrentGameBoard
    size = initial_board.BoardSize
    status_space = dict()
    for i in xrange(size):
        for j in xrange(size):
            status_space[str(i) + ',' + str(j)] = list()
            if board[i][j] == 0:
                for value in xrange(1,size+1):
                    if forward_checking:
                        if is_legal(initial_board, i, j, value):
                            status_space[str(i) + ',' + str(j)].append(value)
                    else:
                        status_space[str(i) + ',' + str(j)].append(value)
            else:
                status_space[str(i) + ',' + str(j)] = None
    return status_space


def find_next_pos_new(initial_board, status_space, forward_checking, MRV, MCV, LCV):

    """Chooses an unassigned location to try values in based on which heuristics are on
    """
    #MRV = choose the variable with the fewest values left
    board = initial_board.CurrentGameBoard
    size = initial_board.BoardSize
    next_row = None
    next_col = None
    if forward_checking and MRV:
        temp_length = size + 1
        for i in xrange(size):
            for j in xrange(size):
                if board[i][j] == 0 and status_space[str(i) + ',' + str(j)] and 0 < len(status_space[str(i) + ',' + str(j)]) < temp_length:
                    temp_length = len(status_space[str(i) + ',' + str(j)])
                    next_row = i
                    next_col = j
                    if temp_length == 1:
                        break
        return next_row, next_col
    else:
        for i in xrange(size):
            for j in xrange(size):
                if board[i][j] == 0:
                    return i, j
    return None, None



def forward_checking_helper(initial_board, status_space, row, col, value):

    board = initial_board.CurrentGameBoard
    size = initial_board.BoardSize

    for col_index in xrange(size):
        temp_value_list = status_space[str(row) + ',' + str(col_index)]
        if temp_value_list:
            status_space[str(row) + ',' + str(col_index)] = [x for x in temp_value_list if x != value]

    for row_index in xrange(size):
        temp_value_list = status_space[str(row_index) + ',' + str(col)]
        if temp_value_list:
            status_space[str(row_index) + ',' + str(col)] = [x for x in temp_value_list if x != value]

    subsquare = int(math.sqrt(size))
    start_row = row - row % subsquare
    start_col = col - col % subsquare
    for i in xrange(subsquare):
        for j in xrange(subsquare):
            temp_value_list = status_space[str(i + start_row) + ',' + str(j + start_col)]
            if temp_value_list:
                status_space[str(i + start_row) + ',' + str(j + start_col)] = [x for x in temp_value_list if x != value]
    return status_space

def LCV_helper(initial_board, status_space, row, col):
    candidate_list = status_space[str(row) + ',' + str(col)]
    board = initial_board.CurrentGameBoard
    size = initial_board.BoardSize

    inconsistanct_count_dict = dict()

    for value in candidate_list:
        inconsistanct_count_dict[value] = 0
        temp_board = copy.deepcopy(initial_board)
        temp_board.set_value(row, col, value)
        for i in xrange(size):
            for j in xrange(size):
                if i != row or j != col:
                    temp_value_list = status_space[str(i) + ',' + str(j)]
                    if temp_value_list:
                        for temp_value in temp_value_list:
                            if not is_legal(temp_board, i, j, temp_value):
                                inconsistanct_count_dict[value] += 1
    return sorted(candidate_list, key = lambda val: inconsistanct_count_dict[val])


'''
=======================================
'''
def solve_old(initial_board, forward_checking = False, MRV = False, Degree = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """


    # print "Your code will solve the initial_board here!"
    # print "Remember to return the final board (the SudokuBoard object)."
    # print "I'm simply returning initial_board for demonstration purposes."
    res = []
    count = 0
    space = initial_status_space(initial_board, forward_checking)
    print space
    solve_helper(initial_board, 0, 0, res, count)
    print res[1]
    return res[0]


def solve_helper(initial_board, row, col, res, count):
    if len(res) > 1:
        return
    if is_complete(initial_board):
        print "Found Solution!!!"
        #initial_board.print_board()
        res.append(copy.deepcopy(initial_board))
        res.append(count)
        return

    r, c = find_next_pos(initial_board, row, col)
    # print r, ", ", c
    if r == None or c == None:
        return initial_board
    for val in range(1, initial_board.BoardSize + 1):
        if is_legal(initial_board, r, c, val):
            initial_board.set_value(r, c, val)
            solve_helper(initial_board, r, c, res, count + 1)
            initial_board.set_value(r, c, 0)


def find_next_pos(initial_board, row, col):
    BoardArray = initial_board.CurrentGameBoard
    for i in range(col, initial_board.BoardSize):
        if BoardArray[row][i] == 0:
            return row, i
    for r in range(row + 1, initial_board.BoardSize):
        for c in range(initial_board.BoardSize):
            if BoardArray[r][c] == 0:
                return r, c
