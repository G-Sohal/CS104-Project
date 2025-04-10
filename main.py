import pygame as pg
import sys
from modules.front_menu import *
from modules.game import *

players =["a", "b"] # for testing
# players = player_names()

# start_button()

run_game(players)

pg.quit()
sys.exit()