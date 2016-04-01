'''
Name: Xiangyu Ji
NetID: XJQ158
'''

def binarySearch(L, v):
    cut_time = 0
    if v == None:
        return (False, cut_time)
    length_of_list = len(L)
    if length_of_list == 0:
        return (False, cut_time)
    elif length_of_list == 1:
        return (L[0] == v, cut_time)
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
#
# L = [0,4,6,12,13,25,27]
# print "binarySearch test case #1: " + str(binarySearch(L,-1) == (False,3))
# print "binarySearch test case #2: " + str(binarySearch(L,12) == (True,0))
# print "binarySearch test case #3: " + str(binarySearch(L,25) == (True,1))
#

def mean(L):
    if L == None:
        return 0
    length_of_list = len(L)
    if length_of_list == 0:
        return 0
    sum_of_list = 0
    for i in L:
        sum_of_list += i
    return float(sum_of_list) / length_of_list

x = [5,1,2,3,1]
y = [5,1,2,3,1,4]
# print "mean test case #1: " + str(mean(x) == float(12)/float(5))
# print "mean test case #2: " + str(mean(y) == float(16)/float(6))

def median(L):
    if L == None:
        return 0
    length_of_list = len(L)
    L.sort()
    if length_of_list % 2:
        return L[length_of_list / 2]
    else:
        return float(L[length_of_list / 2] + L[length_of_list / 2 - 1]) / float(2)
# print "median test case #1: " + str(median(x) == 2)
# print "median test case #2: " + str(median(y) == 2.5)


def bfs(tree, elem):
    if tree == None or elem == None:
        return False
    if len(tree) == 0:
        return False

    node_list = list()
    node_list.append(tree)
    while len(node_list) > 0:
        temp_node = node_list[0]
        node_list = node_list[1:]
        print temp_node[0]
        if temp_node[0] == elem:
            return True
        for k in temp_node[1:]:
            node_list.append(k)
    return False

# print "\nProblem 3: \n"
#
# myTree = [4, [10, [33], [2]], [3], [14, [12]], [1]]
# # print "bfs test case #1: " + str(bfs(myTree, 1) == True)
# # print "bfs test case #2: " + str(bfs(myTree, 7) == False)

def dfs(tree, elem):
    if tree == None or elem == None:
        return False
    if len(tree) == 0:
        return
    return dfs_tree(tree, elem) == True

def dfs_tree(tree, elem):
    print tree[0]
    if tree[0] == elem:
        return True
    for sub_tree in tree[1:]:
        if dfs_tree(sub_tree, elem):
            return True

# print "dfs test case #1: " + str(dfs(myTree, 1) == True)
# print "dfs test case #2: " + str(dfs(myTree, 7) == False)


class TTTBoard():
    def __init__(self):
        self.board = ['*' for i in xrange(9)]
    def __str__(self):
        out_string = ''
        for i in xrange(3):
            for j in xrange(3):
                out_string += self.board[i * 3 + j]
                out_string += ' '
            out_string += "\r\n"
        return out_string


    def makeMove(self, player, pos):
        if pos > 8 or pos < 0 or self.board[pos] != '*':
            return False
        self.board[pos] = player
        return True

    def hasWon(self, player):
        for i in range(3):
            is_colum_same = 1
            is_row_same = 1
            for j in range(3):
                if self.board[i * 3 + j] != player:
                    is_row_same = 0
                if self.board[i + j * 3] != player:
                    is_colum_same = 0
            if is_row_same or is_colum_same:
                return True
        if self.board[0] == player and self.board[4] == player and self.board[8] == player:
            return True
        if self.board[2] == player and self.board[4] == player and self.board[6] == player:
            return True
        return False

    def is_full(self):
        for character in self.board:
            if character == '*':
                return False
        return True

    def gameOver(self):
        if self.is_full() or self.hasWon('X') or self.hasWon('O'):
            return True
        return False

    def clear(self):
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
