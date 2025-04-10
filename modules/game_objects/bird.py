import pygame as pg
from data.constants import *

class Bird:
    def __init__(self, x, y, type, turn):
        self.type = type

        self.image = pg.image.load(bird_images[type]).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image = pg.transform.flip(self.image, turn, False)

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = bird_speeds[type]
        self.velocityx = 0
        self.velocityy = 0
        self.is_launched = False
        self.special_effect_used = False

    def damage(self, block_type):
        return block_damage[self.type][block_type]

    def update(self):
        if self.is_launched:
            self.velocityy += gravity
            self.rect.x += self.velocityx
            self.rect.y += self.velocityy

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def special_effect(self) :
        if not self.special_effect_used :
            if self.type == "Chuck" :
                self.velocityx *= 2
                self.velocityy *= 2
            elif self.type == "Blues" :
                self.rect.x += 50
                self.rect.y -= 50
            elif self.type == "Bomb" :
                self.damage = {m: d * 3 for m, d in self.damage.items()}
            elif self.type == "Red" :
                self.rect.x += 50
                self.rect.y -= 50
        self.special_effect_used = True