# File: Player.py
# Author(s) names AND netid's:
# Date:
# Group work statement: <please type the group work statement
#      given in the pdf here>
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4

    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)

    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        print "mini max moving"

        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""

        print "get max value"

        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score

    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        print "get min value"

        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        print "get score"
        if board.hasWon(self.num):
            return self.num, "  Won"
            return 100.0
        elif board.hasWon(self.opp):
            return self.opp, "  Won"
            return 0.0
        else:
            print "tie game"
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        print "Alpha Beta Move not yet implemented"
        #returns the score adn the associated moved
        cups = board.getPlayersCups(self.num)
        for i in range(0,6):
            print cups[i]
        move = -1
        score = [-INFINITY, INFINITY]
        turn = self
        firstChild = True
        for m in board.legalMoves(self):
            print m
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValueOfAlpahBeta(nb, ply-1, turn, score, firstChild)
            #and see what the opponent would do next
            if s >= score[0]:
                #if the result is better than our best score so far, save that move,score
                move = m
                score[0] = s
            firstChild = False
        #return the best score and move so far
        return score[0], move

    def maxValueOfAlpahBeta(self, board, ply, turn, score, firstChild):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""

        print "get max value"
        current_firstChild = True
        if board.gameOver():
            return turn.score(board)
        current_score = [-INFINITY, INFINITY]
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValueOfAlpahBeta(nextBoard, ply-1, turn, current_score, current_firstChild)
            #print "s in minValue is: " + str(s)
            if not firstChild:
                if s > score[1]:
                    return s
                else:
                    if s > current_score[0]:
                        current_score[0] = s
                    if s > score[0]:
                        score[0] = s
            else:
                if score[1] == INFINITY:
                    score[1] = s
                if s < current_score[0]:
                    current_score[0] = s
                    score[1] = s
            current_firstChild = False
        return current_score[0]

    def minValueOfAlpahBeta(self, board, ply, turn, score, firstChild):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        print "get min value"

        if board.gameOver():
            return turn.score(board)
        current_score = [-INFINITY, INFINITY]
        current_firstChild = True
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValueOfAlpahBeta(nextBoard, ply-1, turn, current_score, current_firstChild)
            #print "s in minValue is: " + str(s)
            if not firstChild:
                if s < score[0]:
                    return s
                else:
                    if s < current_score[1]:
                        current_score[1] = s
                    if s < score[1]:
                        score[1] = s
            else:
                if score[0] == -INFINITY:
                    score[0] = s
                if s < current_score[1]:
                    current_score[1] = s
                    score[0] = s
            current_firstChild = False
        return current_score[1]

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        print "choose move"

        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            print "call mini max start:  "
            print "ply is : ", self.ply
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            print "one return here"
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            print "======================move by ABPRUNE==============================="
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            print "Custom player not yet implemented"
            return -1
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class MancalaPlayer(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        cups = board.getPlayersCups(self.num)
        w = [6,5,4,3,2,1]
        s = board.scoreCups[self.num - 1] * 20
        sum = 0
        for i in xrange(6):
            sum += cup[i]
            if cups[i] == 0:
                s += i * 2
            s += cups[i] * w[i]
        return s

    def scoreHelper(self, board):
