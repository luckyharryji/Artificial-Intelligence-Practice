from MancalaGUI import *

import xjq158

# player1 = Player(1, Player.ABPRUNE, 10)
player1 = xjq158.xjq158(1, xjq158.Player.ABPRUNE, 5)

player2 = xjq158.xjq158(2, xjq158.Player.CUSTOM)

# player2 = MancalaPlayer(2, Player.ABPRUNE, 10)
# player2 = MancalaPlayer(2, Player.HUMAN)


startGame(player1, player2)
