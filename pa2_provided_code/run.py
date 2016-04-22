from MancalaGUI import *

player1 = MancalaPlayer(1, Player.HUMAN)
player2 = MancalaPlayer(2, Player.ABPRUNE, 5)
# player2 = MancalaPlayer(2, Player.HUMAN)

startGame(player1, player2)
