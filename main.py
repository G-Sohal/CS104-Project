import pygame as pg
import sys
from modules.front_menu import *
from modules.game import *

players = player_names()
mode = mode()
start_button()

run_game(players, mode)

pg.quit()
sys.exit()