# this is better than "import settings" since it circumvents having to pre-pend "settings"
from game import *

game = Game()

#############
# Game Loop #
#############
game.main_menu()
while game.running:
    game.start()
    game.game_over()

pg.quit()
sys.exit()
