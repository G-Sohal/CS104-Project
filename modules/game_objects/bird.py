import pygame as pg
import math
from data import constants

class Bird:
    def __init__(self, x, y, type, turn):
        self.type = type
        self.turn = turn
        self.image = pg.image.load(constants.bird_images[type]).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image = pg.transform.flip(self.image, turn, False)
        self.original_image = self.image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = constants.bird_speeds[type]
        self.velocityx = 0
        self.velocityy = 0
        self.is_launched = False
        self.special_effect_used = False # for new Blues created
        self.damage = constants.block_damage[type] # dict item is callable

    def update(self, level):
        if self.is_launched:
            self.velocityy += constants.gravity
            if level == 2 : self.velocityx -= constants.drag*(1-2*self.turn)
            self.rect.x += self.velocityx
            self.rect.y += self.velocityy
            if self.rect.bottom >= constants.ground : # make it to ground
                self.rect.bottom = constants.ground
                self.velocityy *= -0.5
                if abs(self.velocityy) < 1 :
                    self.rect.x = constants.screen_width*2
                #     self.rect.y = constants.screen_height*2
                #     self.is_launched = False
            self.angle = math.degrees(math.atan2(-self.velocityy, self.velocityx))
            self.angle = max(min(self.angle, 30), -30)

            self.image = pg.transform.rotate(self.original_image, -self.angle)

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
                blue_copy = Bird(self.rect.x, self.rect.y, "Blues", self.turn)
                blue_copy_2 = Bird(self.rect.x, self.rect.y, "Blues", self.turn)
                blue_copy.velocityx = self.velocityx - 5
                blue_copy.velocityy = self.velocityy + 5
                blue_copy_2.velocityx = self.velocityx + 5
                blue_copy_2.velocityy = self.velocityy - 5
                blue_copy.is_launched = True
                blue_copy_2.is_launched = True
                blue_copy.special_effect_used = True
                blue_copy_2.special_effect_used = True
                return (self, blue_copy, blue_copy_2)
            elif self.type == "Bomb" :
                self.damage = {"wood": 0.80, "ice": 0.80, "stone": 0.90}
                self.image = pg.image.load(constants.bird_images["Bomb_special"]).convert_alpha()
                self.image = pg.transform.scale(self.image, (50, 50))
                self.image = pg.transform.flip(self.image, self.turn, False)
                self.original_image = self.image
                return (self,)
            elif self.type == "Red" :
                self.velocityx *= 2
                return (self,)