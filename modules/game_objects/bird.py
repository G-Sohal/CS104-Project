import pygame as pg
from data.constants import *

class Bird:
    def __init__(self, x, y, type, turn):
        self.type = type
        self.turn = turn
        self.image = pg.image.load(bird_images[type]).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image = pg.transform.flip(self.image, turn, False)

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = bird_speeds[type]
        self.velocityx = 0
        self.velocityy = 0
        self.is_launched = False
        self.special_effect_used = False # for new Blues created
        self.damage = block_damage[type] # dict item is callable

    def update(self):
        if self.is_launched:
            self.velocityy += gravity
            self.rect.x += self.velocityx
            self.rect.y += self.velocityy

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def special_effect(self) :
        if not self.special_effect_used :
            self.special_effect_used = True
            if self.type == "Chuck" :
                self.velocityx *= 2
                self.velocityy *= 2
                return (self,)
            elif self.type == "Blues" :
                blue_copy = Bird(self.rect.x - 20, self.rect.y + 50, "Blues", self.turn)
                blue_copy_2 = Bird(self.rect.x + 30, self.rect.y - 50, "Blues", self.turn)
                blue_copy.velocityx = self.velocityx
                blue_copy.velocityy = self.velocityy
                blue_copy_2.velocityx = self.velocityx
                blue_copy_2.velocityy = self.velocityy
                blue_copy.is_launched = True
                blue_copy_2.is_launched = True
                blue_copy.special_effect_used = True
                blue_copy_2.special_effect_used = True
                return (self, blue_copy, blue_copy_2)
            elif self.type == "Bomb" :
                self.damage = {"wood": 0.40, "ice": 0.80, "stone": 0.40}
                self.image = pg.image.load(bird_images["Bomb_special"]).convert_alpha()
                self.image = pg.transform.scale(self.image, (50, 50))
                self.image = pg.transform.flip(self.image, self.turn, False)
                return (self,)
            elif self.type == "Red" :
                self.rect.x += 50
                self.rect.y -= 50
                return (self,)