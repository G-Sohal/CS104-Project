import pygame as pg
import sys, random, math
from modules.game_objects import *

pg.init()

screen = pg.display.set_mode((1000, 600), pg.RESIZABLE)
pg.display.set_caption("Angry Birds v2.0")
background_image = pg.image.load("media/images/background.png")
background_image = pg.transform.scale(background_image, (1000, 600))

clock = pg.time.Clock()

font = pg.font.Font(None, 36)

def run_game(players):
    screen.blit(background_image, (0, 0))

    left_catapult = Catapult(200, 450, "left")
    right_catapult = Catapult(740, 450, "right")
    left_catapult.draw(screen)
    right_catapult.draw(screen)

    left_fortress = Fortress(10, 400, 5)
    right_fortress = Fortress(840, 400, 5)
    left_fortress.construct(screen)
    right_fortress.construct(screen)

    turn = 0
    score = [0, 0]
    running = True
    while running:
        turn_text = font.render(f"{players[turn]}'s Turn", True, "black")
        screen.blit(turn_text, (400, 50))
        score_text = font.render(f"Score: {score[0]} - {score[1]}", True, "black")
        screen.blit(score_text, (400, 100))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    
        pg.display.flip()
    #     clock.tick(60)
    
    pg.quit()
    sys.exit()