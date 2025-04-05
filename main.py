import pygame as pg
import sys
from modules.front_menu import *
from modules.game import *

player1, player2 = player_names()

start_button()

game = Game(player1, player2)

game.run()
pg.quit()
sys.exit()
