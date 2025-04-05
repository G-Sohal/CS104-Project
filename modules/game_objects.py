import pygame as pg
import random

colours = {
    "wood": (139, 69, 19),
    "ice": (173, 216, 230),
    "stone": (128, 128, 128)
}

catapult_images = {
    "left": "media/images/catapults/left.png",
    "right": "media/images/catapults/right.png"
}

bird_images = {
    "Red": "media/images/birds/red.png",
    "Chuck": "media/images/birds/chuck.png",
    "Blues": "media/images/birds/blues.png",
    "Bomb": "media/images/birds/bomb.png"
}

block_damage = {
    "Red": {"wood": 25, "ice": 25, "stone": 25},
    "Chuck": {"wood": 40, "ice": 15, "stone": 15},
    "Blues": {"wood": 15, "ice": 40, "stone": 15},
    "Bomb": {"wood": 15, "ice": 15, "stone": 40}
}

class Block :
    def __init__(self, x, y, type, health = 1) :
        self.type = type
        self.rect = pg.Rect(x, y, 50, 50)
        self.health = health

        self.colour = colours[type]
        self.colour = tuple(int(colour * health) for colour in self.colour)

    def draw(self, screen) :
        pg.draw.rect(screen, self.colour, self.rect, border_radius=5)
        pg.draw.rect(screen, (100, 100, 100), self.rect, width=1, border_radius=5)

class Fortress :
    def __init__(self, x, y, height) :
        self.blocks = []
        for i in range(3) :
            for j in range(height) :
                self.blocks.append(Block(x + i*50, y + j*50, random.choice(["wood", "ice", "stone"])))

    def construct(self, screen) :
        for block in self.blocks :
            block.draw(screen)

class Catapult:
    def __init__(self, x, y, type):
        self.image = pg.image.load(catapult_images[type]).convert_alpha()
        self.image = pg.transform.scale(self.image, (80, 150))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Bird :
    def __init__(self, type) :
        self.type = type
        self.image = pg.image.load(bird_images[type]).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        
    def get_damage(self):
        return block_damage[self.type]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)