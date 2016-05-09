#!/usr/bin/env python
import struct, string, math
import copy
import time

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
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """

    start = time.clock()

    #: initail the possible domain value status space for the board
    status_space = initial_status_space(initial_board, forward_checking)

    #: variable used for count the number of level
    count = 0
    result, after_count = solve_helper_new(initial_board, status_space, forward_checking, MRV, Degree, LCV, count)

    elapsed = (time.clock() - start)
    print "total test : ", after_count, " value"
    print("Time used:",elapsed)
    if not result:
        print "No Solution"
    return result


def solve_helper_new(initial_board, status_space, forward_checking, MRV, Degree, LCV, count):
    '''
    Main recursive function for the game solving problem

    iterate through the status space for the remaining domain value until find
    the solution/solution does not exist
    '''
    #: return if the board is a valid solution
    if is_complete(initial_board):
        return initial_board, count
    #: choose the next variable position to be assigned
    next_row, next_col = find_next_pos_new(initial_board, status_space, forward_checking, MRV, Degree, LCV)
    if next_row == None or next_col == None:
        return initial_board, count
        # if is_complete(initial_board):
        #     return initial_board, count
        # else:
        #     return None, count
    if LCV:
        temp_domain_list = LCV_helper(initial_board, status_space, next_row, next_col)
    else:
        temp_domain_list = status_space[str(next_row) + ',' + str(next_col)]
    if temp_domain_list:
        for value in temp_domain_list:
            # decide if value for the position is leagel by here
            if forward_checking or is_legal(initial_board, next_row, next_col, value):
                temp_board = copy.deepcopy(initial_board)
                temp_status_space = copy.deepcopy(status_space)
                temp_board.set_value(next_row, next_col, value)
                #: count the number of variable assignment
                count += 1
                if forward_checking:
                    temp_status_space = forward_checking_helper(initial_board, temp_status_space, next_row, next_col, value)
                result, count = solve_helper_new(temp_board, temp_status_space, forward_checking, MRV, Degree, LCV, count)
                if result != None:
                    return result, count
    return None, count


def is_legal(initial_board, row, col, val):
    '''
    Decide if it is leagel to set val in [row, col] for board

    Decide if in the Same row, Same col, Same square
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
    Create the remaining domain status space for the input game board

    If forward_checking is set to True, check to see if it is leagel to set the
    specific value, else, create the list with all possible value for the board

    Input:
        initial_board(SudokuBoard): the input of the game board
        forward_checking(bool): Whether to use the forward_checking strategy

    Output:
        dict():
            key: 'row, col';
            value: the remaining value choice for the input
                if the square is already occupied by the input: None
                else is the list of possible value for the space
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


def find_next_pos_new(initial_board, status_space, forward_checking, MRV, Degree, LCV):
    '''
    choose the next variable to be testified based on the input heuristic choice

    Input:
        initial_board(SudokuBoard): game board input
        status_space(dict): domain status space for the board
        ... different heuristic choice
    Output:
        row, col(int, int): the next position to be recursived and testified
        None, None: there are no position to be testified, invalid
    '''
    board = initial_board.CurrentGameBoard
    size = initial_board.BoardSize
    next_row = 0
    next_col = 0
    if MRV:
        temp_length = size + 1
        for i in xrange(size):
            for j in xrange(size):
                if board[i][j] == 0 and status_space[str(i) + ',' + str(j)] != None and 0 < len(status_space[str(i) + ',' + str(j)]) < temp_length:
                    temp_length = len(status_space[str(i) + ',' + str(j)])
                    next_row = i
                    next_col = j
                    #: if find a position with only one remaining value, return
                    if temp_length == 1:
                        return next_row, next_col
        return next_row, next_col
    elif Degree:
        temp_constriant_number = -1
        for i in xrange(size):
            for j in xrange(size):
                if board[i][j] == 0 and (status_space[str(i) + ',' + str(j)] != None):
                    constraints_variable_number = degress_heuristic_helper(initial_board, i, j)
                    if constraints_variable_number > temp_constriant_number:
                        temp_constriant_number = constraints_variable_number
                        next_row = i
                        next_col = j
        return next_row, next_col
    else:
        for i in xrange(size):
            for j in xrange(size):
                if board[i][j] == 0:
                    return i, j
    return None, None

def degress_heuristic_helper(initial_board, row, col):
    '''
    Helper function for degree heuristic

    Find the number of constraint variable for the give position row, col
    Input:
        initial_board(@SudokuBoard): Input game board
        row, col(int): position of the variable
    Output:
        constraint_variable_count(int): number of constraint variable for the position
    '''
    board = initial_board.CurrentGameBoard
    size = initial_board.BoardSize

    constraint_variable_count = 0

    for index in xrange(size):
        if board[row][index] == 0 and index != col:
            constraint_variable_count += 1
        if board[index][col] == 0 and index != row:
            constraint_variable_count += 1

    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = col // subsquare

    for i in xrange(subsquare):
        for j in xrange(subsquare):
            if board[SquareRow*subsquare + i][SquareCol*subsquare + j] == 0:
                if (SquareRow*subsquare + i != row) or (SquareCol*subsquare + j != col):
                    constraint_variable_count += 1
    return constraint_variable_count

def forward_checking_helper(initial_board, status_space, row, col, value):
    '''
    Behave forward checking for the game board

    Remove inconsistant value if set value to the position row, col
    '''
    board = initial_board.CurrentGameBoard
    size = initial_board.BoardSize

    #: remove inconsistant value in same row
    for col_index in xrange(size):
        temp_value_list = status_space[str(row) + ',' + str(col_index)]
        if temp_value_list:
            status_space[str(row) + ',' + str(col_index)] = [x for x in temp_value_list if x != value]

    #: remove inconsistant value in same col
    for row_index in xrange(size):
        temp_value_list = status_space[str(row_index) + ',' + str(col)]
        if temp_value_list:
            status_space[str(row_index) + ',' + str(col)] = [x for x in temp_value_list if x != value]

    #: remove inconsistant value in same square
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
    '''
    Return the list of possible value for the position(row, col)
    in the order that each rules out the fewest choices for other unassigned variables.

    Input:
        initial_board(@SudokuBoard): game board input
        status_space(dict): remaining domain space
        row, col(int): position
    Output:
        list: the possible value for the position
    '''
    candidate_list = status_space[str(row) + ',' + str(col)]
    board = initial_board.CurrentGameBoard
    size = initial_board.BoardSize
    #: dict to record number of inconsistant choice for other variable
    inconsistanct_count_dict = dict()
    if candidate_list:
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
        return sorted(candidate_list, key = lambda val: inconsistanct_count_dict[val], reverse = True)
    else:
        return []
