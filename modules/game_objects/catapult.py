import pygame as pg

from data.constants import *

class Catapult:
    def __init__(self, x, y, type):
        self.image = pg.image.load(catapult_images[type]).convert_alpha()
        self.image = pg.transform.scale(self.image, (80, 150))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

    def construct(self, screen):
        screen.blit(self.image, self.rect.topleft)