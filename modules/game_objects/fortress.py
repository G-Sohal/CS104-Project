import pygame as pg
import random

from data.constants import *
from modules.game_objects.block import *

class Fortress :
    def __init__(self, x, y, width, height, moving) :
        self.x = x
        self.y = y
        self.columns = 3
        self.block_size = 50
        self.blocks = []
        for i in range(width) :
            for j in range(height) :
                self.blocks.append(Block(x + i*50, y + j*50, random.choice(["wood", "ice", "stone"]), i, j, moving))
        self.existing_blocks = np.ones((width, height), dtype=bool)

    def construct(self, screen) :
        for block in self.blocks:
            if self.existing_blocks[block.row, block.col]:
                block.update()
                block.construct(screen)

    def set_position(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.x = x
        self.y = y
        for block in self.blocks:
            block.rect.x += dx
            block.rect.y += dy