import pygame as pg
import sys
from modules.front_menu import *
from modules.game import *

players =["a", "b"]
# players = player_names()

# start_button()

game = run_game(players)

game.run()
pg.quit()
sys.exit()
