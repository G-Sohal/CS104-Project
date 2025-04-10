import pygame as pg
from data.constants import *

pg.init()

def ranking(players, score1, score2) :
    screen.blit(game_over_background, (0, 0))
    game_over_text = font.render("Game Over", True, "black")
    screen.blit(game_over_text, (400, 50))

    if score1 > score2 :
        winner_text = font.render(f"{players[0]} won!", True, "black")
    elif score1 < score2 :
        winner_text = font.render(f"{players[1]} won!", True, "black")
    else :
        winner_text = font.render("It was a tie!", True, "black")
    screen.blit(winner_text, (400, 100))

    running = True
    while running :
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN :
                if event.key == pg.K_ESCAPE :
                    running = False
        pg.display.flip()
        pg.time.delay(200)
