# File: Player.py
# Author(s) names AND netid's:
# -----------------------
# |    name    |  Netid |
# -----------------------
# | Xiangyu Ji |        |
# -----------------------
# |  Chong Yan | cyu422 |
# -----------------------
# |  Lin Jiang | ljh235 |
# -----------------------
# Date: Apirl 22nd 2016
# Group work statement: <All group members were present and
#                       contributing during all work on this project.>
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

        """Implement the alpha-beta prune search algorithm to choose a move

        We improved minimax algorithm by proning some branches of the tree that could
        never influence the final result.

        Args:
            board (object): The distribution of the stones in the MancalaBoard.
            ply (int): The number of layers to go in the tree.

        return:
            the best score and move so far, or return (-1,-1) if the game is over

        """

        move = -1
        score = -INFINITY
        turn = self

        # if we're at ply 0, we need to call our eval function & return
        if ply == 0:
            return (self.score(board), m)
        # if board.gameOver() is false means that plauers can't make a move,
        # the game is over. return (-1, -1)
        if board.gameOver():
            return (-1, -1)
        # value_range = [-INFINITY, INFINITY]
        alpha = -INFINITY
        beta = INFINITY
        for m in board.legalMoves(self):
            # initiate a new board
            nb = deepcopy(board)
            # make a move
            nb.makeMove(self, m)

            opp = MancalaPlayer(self.opp, self.type, self.ply)
            s = opp.minValue_pruning(nb, ply-1, turn, alpha, beta)
            # check what the opponent would do next
            # if the result is better than our best score so far,
            # save that move, and score
            if s > score:
                move = m
                score = s
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        # return the best score and move so far,
        # or return (-1,1) if the game is over
        return score, move

    def maxValue_pruning(self, board, ply, turn, alpha, beta):
        """ Find the max value for the next move for this player at a given
            board configuation.

        Args:
            board (object): The distribution of the stones in the MancalaBoard.
            ply (int): The number of layers to go in the tree.
            turn (Player): Which player is supposed to move.
            alpha (int): The lower bound of score.
            beta (int): The upper bound of score.

        return:
            The best score this layer get.

        """
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
        """ Find the min value for the next move for this player at a given
            board configuation. Returns score.

        Args:
            board (object): The distribution of the stones in the MancalaBoard.
            ply (int): The number of layers to go in the tree.
            turn (Player): Which player is supposed to move.
            alpha (int): The lower bound of score.
            beta (int): The upper bound of score.

        return:
            The best score this layer get.

        """
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
        """ Returns the next move that this player wants to make"""
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
        """ Calculate the score based on the distribution
            of the Mancalaboard for the player """
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
        #     return board.scoreCups[self.num - 1]/float(48)
        return self.score_calculate(board)

    def score_calculate(self, board):

        """Helper function to customize the claculatation the score for the player

        Args:
            board (object): The distribution of the stones in the MancalaBoard.

        return:
            The score for the current board state.

        """
        # if the playerNum is 1, then we could calculate the score
        if self.num == 1:
            score_variant = board.scoreCups[0] - board.scoreCups[1]
            stone_variant = sum(board.P1Cups) - sum(board.P2Cups)
            # initiate overflow
            overflow = 0
            for i in xrange(board.NCUPS):
                # calculate the stones for playerNum 2 according to the weighted pits
                overflow -= max(0, board.P2Cups[i] - (i + 1))
                # calculate the stones for playerNum 1 according to the weighted pits
                overflow += max(0, board.P1Cups[i] - (6 - i))
            # return the weighted score for playerNum 1
            return float(0.9) * score_variant + float(0.9) * stone_variant + float(0.7) * overflow
        else:
            # if the playerNum is 2, then we could calculate the score
            score_variant = board.scoreCups[1] - board.scoreCups[0]
            stone_variant = sum(board.P2Cups) - sum(board.P1Cups)
            # initiate overflow
            overflow = 0
            for i in xrange(board.NCUPS):
                # calculate the stones for playerNum 2 according to the weighted pits
                overflow += max(0, board.P2Cups[i] - (i + 1))
                # calculate the stones for playerNum 1 according to the weighted pits
                overflow -= max(0, board.P1Cups[i] - (6 - i))
            # return the weighted score for playerNum 2
            return float(0.9) * score_variant + float(0.9) * stone_variant + float(0.7) * overflow
