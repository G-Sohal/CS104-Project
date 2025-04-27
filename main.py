import pygame as pg
import sys

pg.init()

from modules.front_menu import *
from modules.game import *

pg.display.set_caption("Angry Birds v2.0")

score_sessions = []

# start_button()
# mode = mode()
level = level()
# players = player_names()
# rows, cols = dimension_fortress()
players = ["A", "B"]
mode = 0
level = 0
rows = 4
cols = 3
game = Game(players, mode, level, rows, cols)
score = game.run()
score_sessions.append(score)

pg.quit()
sys.exit()