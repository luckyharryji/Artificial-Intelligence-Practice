# File: Player.py
# Author(s) names AND netid's:
# -----------------------
# |    name    |  Netid |
# -----------------------
# | Xiangyu Ji |  xjq158|     |
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
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
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
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
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
        if board.gameOver():
            return (-1, -1)
        #: initial the alpha-beta value in upper level
        alpha = -INFINITY
        beta = INFINITY
        for m in board.legalMoves(self):
            nb = deepcopy(board)
            nb.makeMove(self, m)

            opp = xjq158(self.opp, self.type, self.ply)

            #: pass alpha, beta into next level
            s = opp.minValue_pruning(nb, ply-1, turn, alpha, beta)
            # check what the opponent would do next
            # if the result is better than our best score so far,
            # save that move, and score
            if s > score:
                move = m
                score = s
            alpha = max(alpha, score)
            # cut branch instantly
            if beta <= alpha:
                break
        return score, move

    def maxValue_pruning(self, board, ply, turn, alpha, beta):
        """ For the alpha-beta pruning, find the max value for the next move for
            this player at a given board configuation, while cut-branch as
            algorithm demonstration.

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
            opponent = xjq158(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue_pruning(nextBoard, ply-1, turn, alpha, beta)
            score = max(score, s)
            alpha = max(alpha, score)
            #: cut branch
            if beta <= alpha:
                break
        return score


    def minValue_pruning(self, board, ply, turn, alpha, beta):
        """ For alpha-beta pruning, find the min value for the next move for
            this player at a given board configuation. Returns score.

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
            opponent = xjq158(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue_pruning(nextBoard, ply-1, turn, alpha, beta)
            score = min(score, s)
            beta = min(beta, score)
            #: cut branch
            if beta <= alpha:
                break
        return score

    def custom_move(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move)

        Our custom player mainly focus on the improvement of the heuristic score
        function for the game.

        Also, it would force the player to choose the move if can give the player
        a second chance to play

        The depth of the move search is set static to be 10.
        """

        move = -1
        score = -INFINITY
        turn = self

        if self.num == 1:
            cups = board.P1Cups
        else:
            cups = board.P2Cups

        #: encourage the AI player to first chose the move that can earn seacond
        #: chance, from right to left in the player's viewpoint.
        for i in range(board.NCUPS):
            if cups[6 - i - 1] == i + 1:
                return 100, 6 - i

        if ply == 0:
            #if we're at ply 0, we need to call our eval function & return
            return (self.score(board), m)
        if board.gameOver():
            return (-1, -1)  # Can't make a move, the game is over


        alpha = -INFINITY
        beta = INFINITY
        for m in board.legalMoves(self):
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = xjq158(self.opp, self.type, self.ply)
            s = opp.minValue_pruning(nb, ply-1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return score, move


    def chooseMove(self, board):
        """ Returns the next move that this player wants to make"""
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            val, move = self.custom_move(board, 10)
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class xjq158(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Calculate the score based on the distribution
            of the Mancalaboard for the player

            This part would encourage the score to add more 100 in wining
            condition and minus 100 in losing
        """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        if board.hasWon(self.num):
            return self.score_calculate(board) + float(100.0)
        elif board.hasWon(self.opp):
            return self.score_calculate(board) - float(100.0)
        else:
            return self.score_calculate(board)

    def score_calculate(self, board):

        """Helper function to customize the claculatation the score for the player

        Consider condition:
            - encourage the stone in self manala be more than the opponent by difference
            - encourage the total stones in self pits/holes to be more than the opponent
            - avoid pits with 0 stone to reduce the risk of being eaten
            - avoid moving stons to opponent's pits

        The weight of these variables are pre-tuned in the range of (0, 1.5),
        in step of 0.1.

        As result, we choose 0.9, 0.9, 0.2, 1.3

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
            capture = 0
            for i in xrange(board.NCUPS):
                # calculate the stones for playerNum 2 according to the weighted pits
                overflow -= max(0, board.P2Cups[i] - (i + 1))
                # calculate the stones for playerNum 1 according to the weighted pits
                overflow += max(0, board.P1Cups[i] - (6 - i))
                if board.P2Cups[i] > 0 and board.P2Cups[i] <= 5 - i and board.P2Cups[i + board.P2Cups[i]] == 0:
                    capture = max(capture, board.P1Cups[5 - i - board.P2Cups[i]])

            return float(0.9) * score_variant + float(0.9) * stone_variant + float(0.2) * overflow - float(1.3) * capture
        else:
            # if the playerNum is 2, then we could calculate the score
            score_variant = board.scoreCups[1] - board.scoreCups[0]
            stone_variant = sum(board.P2Cups) - sum(board.P1Cups)
            # initiate overflow
            overflow = 0
            capture = 0
            for i in xrange(board.NCUPS):
                # calculate the stones for playerNum 2 according to the weighted pits
                overflow += max(0, board.P2Cups[i] - (i + 1))
                # calculate the stones for playerNum 1 according to the weighted pits
                overflow -= max(0, board.P1Cups[i] - (6 - i))
                if board.P1Cups[i] > 0 and board.P1Cups[i] <= 5 - i and board.P1Cups[i + board.P1Cups[i]] == 0:
                    capture = max(capture, board.P2Cups[5 - i - board.P1Cups[i]])

            return float(0.9) * score_variant + float(0.9) * stone_variant + float(0.2) * overflow - float(1.3) * capture
