from MancalaGUI import *

# player1 = Player(1, Player.ABPRUNE, 10)
player1 = MancalaPlayer(1, Player.HUMAN)

player2 = MancalaPlayer(2, Player.CUSTOM)

# player2 = MancalaPlayer(2, Player.ABPRUNE, 10)
# player2 = MancalaPlayer(2, Player.HUMAN)

startGame(player1, player2)
