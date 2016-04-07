'''
Name: Xiangyu Ji
NetID: XJQ158
'''

"""Homework 1 of EECS 348: Intro to AI.

This file/module contains my personal solution for the 4 problem set of
assignment. Each problem aresolved with one function/Class.

"""

# Problem 1:
def binarySearch(L, v):
    """Search a value in a list with binary search.

    Search to decide if a given value exists in a list or not.

    Assumptions:
        If the length of the list is 1 (len(L) == 1), the list will still be
        halved one time base on the defination of binary search rather than just
        compare and return.
        Another word, base - case is: len(L) == 0.

    Args:
        L (list[int]): given list to be searched
        v (int) : value wants to be found/decide if its in the list

    Returns:
        A tuple contains:
            bool: True if the given value exists in the given list, False if not
            int: how many times the function halved the list with the binary search
        An example:
            (True, 4)
    """
    #: int: initial a variable to record the number of halve when conduting search
    cut_time = 0
    if v == None:
        return (False, cut_time)
    length_of_list = len(L)
    if length_of_list == 0:
        return (False, cut_time)
    else:
        top = 0
        tail = length_of_list - 1
        while top <= tail:
            mid = (top + tail) / 2
            if L[mid] == v:
                return (True, cut_time)
            elif L[mid] < v:
                top = mid + 1
                cut_time += 1
            else:
                tail = mid - 1
                cut_time += 1
        return (False, cut_time)

# print "------------------Binary Search Test---------------------------"
# L = [0,4,6,12,13,25,27]
# print "binarySearch test case #1: " + str(binarySearch(L,-1) == (False,3))
# print "binarySearch test case #1: " + str(binarySearch(L,13) == (True,2))
# print "binarySearch test case #1: " + str(binarySearch(L,25) == (True,1))
# print "binarySearch test case #2: " + str(binarySearch(L,12) == (True,0))
# print "binarySearch test case #3: " + str(binarySearch(L,25) == (True,1))
#
# L = [0]
# print "binarySearch test case #1: " + str(binarySearch(L,-1) == (False,1))
#
# L = [0, 4, 23, 26]
# print "binarySearch test case #2: " + str(binarySearch(L,-1) == (False,2))
# print "------------------Binary Search Test end---------------------------"



def mean(L):
    """Calculate the mean value of a given list

    Given a int list, calculate the mean of all the elements inside the list

    Assumptions:
        The function would return 0 if the input list is None or the lenght of
        the input list is 0.

    Args:
        L (list[int]): given list to be calculated.

    Returns:
        0: if the input list does not exist or is empty.
        float: the mean value of the list

        example:
            @input: []
            @output: 0

            @input: [1, 2]
            @output: 1.5
    """
    if L == None:
        return 0
    length_of_list = len(L)
    if length_of_list == 0:
        return 0
    sum_of_list = 0
    for i in L:
        sum_of_list += i
    return float(sum_of_list) / float(length_of_list)

#
# print "----------mean value test-----------------"
# x = [5,1,2,3,1]
# y = [5,1,2,3,1,4]
# print "mean test case #1: " + str(mean(x) == float(12)/float(5))
# print "mean test case #2: " + str(mean(y) == float(16)/float(6))
# print "----------mean value test end---------------"


def median(L):
    """Calculate the meadian value of the given list.

    Given a int list, fetch the median value of it.

    Assumptions:
        The function would return 0 if the input list is None or the lenght of
        the input list is 0.

    Args:
        L (list[int]): given list to be calculated.

    Returns:
        0: if the input list does not exist or is empty.
        float: the median value of the list

        example:
            @input: []
            @output: 0

            @input: [1, 2, 3]
            @output: 2
    """
    if L == None:
        return 0
    length_of_list = len(L)
    L.sort() #: python function to sort the input list in-place
    if length_of_list % 2:
        return L[length_of_list / 2]
    else:
        return float(L[length_of_list / 2] + L[length_of_list / 2 - 1]) / float(2)
# print "-----------median value test-----------------"
# x = [5,1,2,3,1]
# y = [5,1,2,3,1,4]
# print "median test case #1: " + str(median(x) == 2)
# print "median test case #2: " + str(median(y) == 2.5)
# print "-----------median value test end-----------------"

def bfs(tree, elem):
    """Breadth first search of a tree structure to find an element.

    Given a tree structure represented by list of lists, use breadth first
    search order to find the given element in the tree.

    Assumptions:
        The BFS will search from left to right.

        The function will return False if the tree is empty/the given element
        is None.

    Args:
        tree (list[ list[int] ]): a list of list representing the tree.
        elem (int): an integer representing the node element to be found in the tree.

    Returns:
        bool: True if the element is in the tree, False if not.
    """
    if tree == None or elem == None:
        return False
    if len(tree) == 0:
        return False
    #: implement the BFS with use python list as queue
    node_list = list()
    node_list.append(tree)
    while len(node_list) > 0:
        #: use Python list to behave like queue fullfill FIFO
        #: temp_node: store the first element in the existing queue
        #: list[1:]: remove the first element from the list to refresh the list
        temp_node = node_list[0]
        node_list = node_list[1:]
        print temp_node[0]
        if temp_node[0] == elem:
            return True
        for k in temp_node[1:]:
            node_list.append(k)
    return False

# print "-----------------test of Problem 3:--------------------"
# myTree = [4, [10, [33], [2]], [3], [14, [12]], [1]]
# print "bfs test case #1: " + str(bfs(myTree, 1) == True)
# print "bfs test case #2: " + str(bfs(myTree, 7) == False)
# print "-----------------end of test of Problem 3:--------------------"

def dfs(tree, elem):
    """Depth first search of a tree structure to find an element.

    Given a tree structure represented by list of lists, use depth first
    search order to find the given element in the tree.
    Create a helper functin dfs_iterate_tree() to iterate through the tree

    Assumptions:
        The DFS process will search from left to right for the tree.

        The function will return False if the tree is empty/the given element
        is None.

    Args:
        tree (list[ list[int] ]): a list of list representing the tree.
        elem (int): an integer representing the node element to be found in the tree.

    Returns:
        bool: True if the element is in the tree, False if not.
    """
    #: first check the input
    if tree == None or elem == None:
        return False
    if len(tree) == 0:
        return False
    #: the elem is found in the tree only when the helper function return True
    return dfs_iterate_tree(tree, elem) == True

def dfs_iterate_tree(tree, elem):
    """Helper function of dfs(), iterate through the tree to find an element with recursion.

    Recursively go through the node in the tree

    Assumptions:
        The scale of the input tree structure will not cause the stackoverflow
        in Python

    Args:
        tree (list[list[int]]): a list of list representing the origin/subtree.
        elem (int): an integer representing the node element to be found in the subtree.

    Returns:
        None: if the elem is not found
        True: if the elem is found in the tree
    """
    print tree[0]
    #: the elem which is being checked, every time the root of the subtree
    if tree[0] == elem:
        return True
    #: if the root of the subtree not equal to the elem, recursive to next level of subtree
    #: list[1:] will return the element except the first element of list, return [] if
    #: the list only contain one element.
    for sub_tree in tree[1:]:
        if dfs_iterate_tree(sub_tree, elem):
            return True
# print "-------------Test of DFS---------------"
# myTree = [4, [10, [33], [2]], [3], [14, [12]], [1]]
# print "dfs test case #1: " + str(dfs(myTree, 1) == True)
# print "dfs test case #2: " + str(dfs(myTree, 12) == True)
# print "-------------end test of DFS---------------"

class TTTBoard():
    """A class for managing a game of Tic Tac Toe.

    This is a class created to manamge the basic behavior of the game. The game
    is designed to have the layout the square of 3 * 3.

    The game support a 2 player game each representated by X or O.

    '*' means empty position.

    Attributes:
        board (list[str]):
            a list representing the layout of the 3 * 3 game.
            * if the position is empty.
            X or O if the postion is taken by the assigned player.
    """
    def __init__(self):
        """Initial the empty board for the game.
        """
        self.board = ['*' for i in xrange(9)]

    def __str__(self):
        """String function for the class.

        A string represenation of the 3 * 3 board of the on-going contion.

        Returns:
            str: a 3 rows of 3 items each format string representating the board.
        """
        out_string = ''
        for i in xrange(3):
            for j in xrange(3):
                out_string += self.board[i * 3 + j]
                out_string += ' '
            out_string += "\r\n"
        return out_string


    def makeMove(self, player, pos):
        """Place a move for player in the position.

        Change the broad of the game if a player wants to change the position.

        Args:
            player (string): 'X' or 'O', a player of game.
            pos (int): a number representating the position, starting from top left to right bottom.

        Returns:
            bool: True if the move can be made, False if not.
        """
        #: check if the input pos is valid for the game.
        if pos > 8 or pos < 0 or self.board[pos] != '*':
            return False
        self.board[pos] = player
        return True

    def hasWon(self, player):
        """Check if the player has won the game.

        Check if the player occupy all the same line/row/diagonal.

        Args:
            player (string): 'X' or 'O', a player in the game.

        Returns:
            bool: True if the player has one, False if not.
        """
        #: first check if the palyer has occupied all the same row/same colum
        for i in range(3):
            #: int(0/1): use these to variable to mark if the player has all the ssame row/column.
            is_colum_same = 1
            is_row_same = 1
            for j in range(3):
                if self.board[i * 3 + j] != player:
                    is_row_same = 0
                if self.board[i + j * 3] != player:
                    is_colum_same = 0
            #: directly return if the player win with same row/colum.
            if is_row_same or is_colum_same:
                return True
        #: check if the player has occupied either of 2 diagonal line.
        if self.board[0] == player and self.board[4] == player and self.board[8] == player:
            return True
        if self.board[2] == player and self.board[4] == player and self.board[6] == player:
            return True
        return False

    def is_full(self):
        """Check if the board of the game is already full.

        Check if the board has occupied by the players.

        Returns:
            bool: True if the board is full, False if not.
        """
        for character in self.board:
            if character == '*':
                return False
        return True

    def gameOver(self):
        """Check if the game can be over.

        Check if the board can over, means either player 'X' wins or player 'O'
        wins or the board of the game is full.

        Returns:
            bool: True if the game can be over, False if not.
        """
        if self.is_full() or self.hasWon('X') or self.hasWon('O'):
            return True
        return False

    def clear(self):
        """Reset the game.

        Set all the value of the board to be '*' to clear the board and reset the game.
        """
        self.board = ['*' for i in xrange(9)]

print "\nProblem 4: \n"

myB = TTTBoard()
print myB
myB.makeMove("X", 8)
myB.makeMove("O", 7)
myB.makeMove("X", 5)
myB.makeMove("O", 6)
myB.makeMove("X", 2)
print myB

print "tic tac toe test case #1: " + str(myB.hasWon("X") == True)
print "tic tac toe test case #2: " + str(myB.hasWon("O") == False)
