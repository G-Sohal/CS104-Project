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

    score_text = font.render(f"Score: {score1} - {score2}", True, "black")
    screen.blit(score_text, (400, 150))

    resume_text = font.render("Left game mid-session? Press P to resume", True, "black")
    screen.blit(resume_text, (400, 175))
    restart_text = font.render("Want to start over again? Press R to restart", True, "black")
    screen.blit(restart_text, (400, 200))
    exit_text = font.render("Press ESC to exit", True, "black")
    screen.blit(exit_text, (400, 250))

    running = True
    while running :
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN :
                if event.key == pg.K_r :
                    return True
                elif event.key == pg.K_p :
                    return False
                elif event.key == pg.K_ESCAPE :
                    running = False
                if event.key == pg.K_ESCAPE :
                    running = False
        pg.display.flip()
        pg.time.delay(200)
 # Option  to go back is just wanted to see rankings mid-game