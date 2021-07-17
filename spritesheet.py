import pygame as pg
from pygame.locals import *
import json


class Spritesheet:
    ## old spritesheet class for non json files (until I adjust spritesheet class to handle XML files to)

    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # fetch sprite from spritesheet
        image = pg.Surface((width, height))

        # take sprite from sprite sheet using xml/json coords >>> blit sprite onto image surface
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image


class Spritesheet_Loader:


    ## Parses spritesheet using json metadata to pull specified sprite;
    ## need to update for xml integration - although json hash output
    ## will usually be the preferred  file type

    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
        self.meta_data = filename.replace('png', 'json')

        # implement try and catch exception
        with open(self.meta_data) as file:
            self.sprite_key = json.load(file)
        file.close()

    def extract_image(self, name, colour_key,scale):
        sprite = self.sprite_key['frames'][name]['frame']
        x, y, width, height = sprite["x"], sprite["y"], sprite["w"], sprite["h"]

        # fetch sprite from spritesheet
        image = pg.Surface((width, height))
        image.set_colorkey(colour_key)

        # take sprite from sprite sheet using xml/json coords >>> blit sprite onto image surface
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // scale, height // scale))

        return image
