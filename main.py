# this is better than "import settings" since it circumvents having to pre-pend "settings"
from game import *

game = Game()

#############
# Game Loop #
#############
while True:
    game.start()
