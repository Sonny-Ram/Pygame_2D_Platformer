import pygame as pg
from pygame.locals import *


class Spritesheet:
    ## old spritesheet class for non json files (until I adjust spritesheet class to handle XML files to)

    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()


    def get_image(self, x,y,width,height):

        # fetch sprite from spritesheet
        image = pg.Surface((width, height))

        # take sprite from sprite sheet using xml/json coords >>> blit sprite onto image surface
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
