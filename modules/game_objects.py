import pygame as pg
import random, math

gravity = 0.5
drag = 0.1

block_images = {
    "wood": { "1": "media/images/blocks/wood100.png", "0.8": "media/images/blocks/wood80.png", "0.6": "media/images/blocks/wood60.png", "0.4": "media/images/blocks/wood40.png", "0.2": "media/images/blocks/wood20.png" },
    "ice": {"1": "media/images/blocks/ice100.png", "0.8": "media/images/blocks/ice80.png", "0.6": "media/images/blocks/ice60.png", "0.4": "media/images/blocks/ice40.png", "0.2": "media/images/blocks/ice20.png"},
    "stone": {"1": "media/images/blocks/stone100.png", "0.8": "media/images/blocks/stone80.png", "0.6": "media/images/blocks/stone60.png", "0.4": "media/images/blocks/stone40.png", "0.2": "media/images/blocks/stone20.png"}
}

# block_rgb = {
#     "wood": (139, 69, 19),
#     "ice": (173, 216, 230),
#     "stone": (128, 128, 128)
# }

catapult_images = {
    "left": "media/images/catapults/left.png",
    "right": "media/images/catapults/right.png"
}

bird_images = {
    "Red": "media/images/birds/red.png",
    "Chuck": "media/images/birds/chuck.png",
    "Blues": "media/images/birds/blue.png",
    "Bomb": "media/images/birds/bomb.png"
}

bird_speeds = {
    "Red" : 20,
    "Chuck" : 32,
    "Blues" : 25,
    "Bomb" : 17
}

block_damage = {
    "Red": {"wood": 0.25, "ice": 0.25, "stone": 0.25},
    "Chuck": {"wood": 0.40, "ice": 0.20, "stone": 0.20},
    "Blues": {"wood": 0.20, "ice": 0.40, "stone": 0.20},
    "Bomb": {"wood": 0.20, "ice": 0.15, "stone": 0.40}
}

class Block :
    def __init__(self, x, y, type) :
        self.type = type
        self.rect = pg.Rect(x, y, 50, 50)
        self.health = 1
        # self.colour = block_rgb[type]
        self.image = pg.image.load(block_images[type]["1"]).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))

    def construct(self, screen) :
        screen.blit(self.image, self.rect.topleft)
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

class Fortress :
    def __init__(self, x, y, height) :
        self.x = x
        self.y = y
        self.columns = 3
        self.block_size = 50
        self.blocks = []
        for i in range(3) :
            for j in range(height) :
                self.blocks.append(Block(x + i*50, y + j*50, random.choice(["wood", "ice", "stone"])))

    def construct(self, screen) :
        for block in self.blocks :
            block.construct(screen)


class Catapult:
    def __init__(self, x, y, type):
        self.image = pg.image.load(catapult_images[type]).convert_alpha()
        self.image = pg.transform.scale(self.image, (80, 150))
        self.rect = self.image.get_rect(topleft=(x, y))

    def construct(self, screen):
        screen.blit(self.image, self.rect.topleft)

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