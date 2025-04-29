import pygame as pg
import numpy as np
import random, math

from data.constants import *

class Block :
    def __init__(self, x, y, type, row, col, moving) :
        self.type = type
        self.row = row
        self.col = col
        self.rect = pg.Rect(x, y, 50, 50)
        self.health = 1
        # self.colour = block_rgb[type]
        self.image = pg.image.load(block_images[type]["1"]).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.velocity_y = 0
        self.falling = False
        self.moving = moving
        self.delta_x = 0
        self.delta_y = 0
        self.dir = 1

    def construct(self, screen) :
        screen.blit(self.image, self.rect.bottomleft)
        # pg.draw.rect(screen, self.colour, self.rect, border_radius=5)
        # pg.draw.rect(screen, (100, 100, 100), self.rect, width=1, border_radius=5)

    def hit(self, damage) :
        self.health -= damage
        if self.health <= 0 :
            self.color = (0, 0, 0)
            self.rect.x = -1000
            return True
        elif self.health <= 0.2 :
            self.image = pg.image.load(block_images[self.type]["0.2"]).convert_alpha()
            self.image = pg.transform.scale(self.image, (50, 50))
            return False
        elif self.health <= 0.4 :
            self.image = pg.image.load(block_images[self.type]["0.4"]).convert_alpha()
            self.image = pg.transform.scale(self.image, (50, 50))
            return False
        elif self.health <= 0.6 :   
            self.image = pg.image.load(block_images[self.type]["0.6"]).convert_alpha()
            self.image = pg.transform.scale(self.image, (50, 50))
            return False
        elif self.health <= 0.8 :
            self.image = pg.image.load(block_images[self.type]["0.8"]).convert_alpha()
            self.image = pg.transform.scale(self.image, (50, 50))
            return False
        elif self.health <= 1 :
            return False
        
    def update(self) :
        if self.falling:
            self.rect.y += 5
            self.delta_y += 5
            if self.delta_y >= 50 :
                self.falling = False
                self.delta_y = 0
        if self.moving:
            if self.delta_x <= -50:
                self.dir = 1
                self.delta_x = -50
            elif self.delta_x >= 50:
                self.dir = -1
                self.delta_x = 50
            self.rect.x += 2 * self.dir
            self.delta_x += 2 * self.dir
            # pg.time.wait()
            
