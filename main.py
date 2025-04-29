import pygame as pg
import sys

pg.init()

from modules.front_menu import *
from modules.game import *

pg.display.set_caption("Angry Birds v2.0")

score_sessions = []

front_menu = FrontMenu()
# front_menu.run()
front_menu.start_button() # add a loading thing
mode = front_menu.mode()
level = front_menu.level()
players = front_menu.player_names()
rows, cols = front_menu.dimension_fortress()
method = front_menu.method()

game = Game(players, mode, level, rows, cols, method)
score = game.run()
score_sessions.append(score)

pg.quit()
sys.exit()