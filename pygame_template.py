import pygame as pg
from   pygame.locals import *
import os
import sys
# this is better than "import settings" since it circumvents having to pre-pend "settings"
from settings import *


# initialise pygame
pg.init()
# create game screen - requires width, height but can take additional flags
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Name the game window/screen
pg.display.set_caption("Top Down Bonanza")
# Create clock for time:frame tracking - used as a reference for maintaining desired fps
clock = pg.time.Clock()


# Game Loop #
while True:

    # maintain desired loop run speed
    clock.tick(FPS)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.fill(BLACK)

    pg.display.flip()



game = Game()
