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
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
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
        move = -1
        score = -INFINITY
        turn = self

        if ply == 0:
            #if we're at ply 0, we need to call our eval function & return
            return (self.score(board), m)
        if board.gameOver():
            return (-1, -1)  # Can't make a move, the game is over
        # value_range = [-INFINITY, INFINITY]
        alpha = -INFINITY
        beta = INFINITY
        for m in board.legalMoves(self):
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = MancalaPlayer(self.opp, self.type, self.ply)
            s = opp.minValue_pruning(nb, ply-1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        #return the best score and move so far
        return score, move
        # return (-1,1)


    def maxValue_pruning(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver() or ply == 0:
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            opponent = MancalaPlayer(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue_pruning(nextBoard, ply-1, turn, alpha, beta)
            #print "s in maxValue is: " + str(s)
            score = max(score, s)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return score


    def minValue_pruning(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver() or ply == 0:
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            opponent = MancalaPlayer(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue_pruning(nextBoard, ply-1, turn, alpha, beta)
            #print "s in minValue is: " + str(s)
            score = min(score, s)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return score



    def customMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        cups = board.getPlayersCups(self.num)

        for i in xrange(len(cups)):
            if cups[i] == i + 1:
                return 100, i


        if ply == 0:
            #if we're at ply 0, we need to call our eval function & return
            return (self.score(board), m)
        if board.gameOver():
            return (-1, -1)  # Can't make a move, the game is over
        # value_range = [-INFINITY, INFINITY]
        alpha = -INFINITY
        beta = INFINITY
        for m in board.legalMoves(self):
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = MancalaPlayer(self.opp, self.type, self.ply)
            s = opp.minValue_pruning(nb, ply-1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        #return the best score and move so far
        return score, move
        # return (-1,1)


    def maxValue_custom(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver() or ply == 0:
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            opponent = MancalaPlayer(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue_pruning(nextBoard, ply-1, turn, alpha, beta)
            #print "s in maxValue is: " + str(s)
            score = max(score, s)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return score


    def minValue_custom(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver() or ply == 0:
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            opponent = MancalaPlayer(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue_pruning(nextBoard, ply-1, turn, alpha, beta)
            #print "s in minValue is: " + str(s)
            score = min(score, s)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return score


    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
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
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val

            print board.P1Cups
            print board.P2Cups

            # val2, move2 = self.minimaxMove(board, self.ply)
            # print "==========Minigmax=========="
            # print val2, move2
            # print "===========Pruning============"
            # print val, move
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            val, move = self.customMove(board, self.ply)
            return move
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
        #print "Calling score in MancalaPlayer"
        # return Player.score(self, board)
        # if board.hasWon(self.num):
        #     return 100.0
        # elif board.hasWon(self.opp):
        #     return 0.0
        # else:
        return self.score_calculate(board)
            # return board.scoreCups[self.num - 1]/float(48)

    def score_calculate(self, board):
        if self.num == 1:
            score_variant = board.scoreCups[0] - board.scoreCups[1]
            stone_variant = sum(board.P1Cups) - sum(board.P2Cups)
            overflow = 0
            for i in xrange(board.NCUPS):
                overflow -= max(0, board.P2Cups[i] - (i + 1))
                overflow += max(0, board.P1Cups[i] - (6 - i))
            return float(0.9) * score_variant + float(0.9) * stone_variant + float(0.7) * overflow
        else:
            score_variant = board.scoreCups[1] - board.scoreCups[0]
            stone_variant = sum(board.P2Cups) - sum(board.P1Cups)
            overflow = 0
            for i in xrange(board.NCUPS):
                overflow += max(0, board.P2Cups[i] - (i + 1))
                overflow -= max(0, board.P1Cups[i] - (6 - i))
            return float(0.9) * score_variant + float(0.9) * stone_variant + float(0.7) * overflow

    def score_calculate2(self, board):
        if self.num == 1:
            score_variant = board.scoreCups[0] - board.scoreCups[1]
            stone_variant = sum(board.P1Cups) - sum(board.P2Cups)
            empty_cup = 0
            for i in xrange(board.NCUPS):
                if board.P1Cups[i] == 0:
                    empty_cup += 6 - i
                if board.P2Cups[i] == 0:
                    empty_cup -= 6 - i
            return float(0.9) * score_variant + float(0.9) * stone_variant + float(1.0) * empty_cup
        else:
            score_variant = board.scoreCups[1] - board.scoreCups[0]
            stone_variant = sum(board.P2Cups) - sum(board.P1Cups)
            empty_cup = 0
            for i in xrange(board.NCUPS):
                if board.P1Cups[i] == 0:
                    empty_cup -= 6 - i
                if board.P2Cups[i] == 0:
                    empty_cup += 6 - i
            return float(0.9) * score_variant + float(0.9) * stone_variant + float(1.0) * empty_cup
