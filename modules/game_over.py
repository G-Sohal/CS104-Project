import pygame as pg
from data import constants
pg.init()

def ranking(players, score1, score2, done = False) :
    constants.game_over_background = pg.transform.scale(constants.game_over_background, constants.screen.get_size())
    constants.screen.blit(constants.game_over_background, (0, 0))
    game_over_text = constants.font_heading.render("Game Over", True, "red")
    constants.screen.blit(game_over_text, (constants.screen_width//2 - (game_over_text.get_width())//2, 50))

    if score1 > score2 :
        winner_text = constants.font.render(f"{players[0]} won!", True, "black")
    elif score1 < score2 :
        winner_text = constants.font.render(f"{players[1]} won!", True, "black")
    else :
        winner_text = constants.font.render("It was a tie!", True, "black")
    constants.screen.blit(winner_text, (constants.screen_width//2 - (winner_text.get_width())//2, constants.screen_height//4))

    score_text = constants.font.render(f"Score: {score1} - {score2}", True, "black")
    constants.screen.blit(score_text, (constants.screen_width//2 - (score_text.get_width())//2, constants.screen_height//4 + 100))

    if not done :
        resume_text = constants.font.render("Left game mid-session? Press R to resume", True, "black")
        constants.screen.blit(resume_text, (constants.screen_width//2 - (resume_text.get_width())//2, constants.screen_height//2))
    exit_text = constants.font.render("Press ESC to exit", True, "black")
    constants.screen.blit(exit_text, (constants.screen_width//2 - (exit_text.get_width())//2, constants.screen_height - 150))

    running = True
    while running :
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN :
                if event.key == pg.K_r and not done:
                    return "resume"
                elif event.key == pg.K_ESCAPE :
                    return "exit"
        pg.display.flip()
 # Option  to go back is just wanted to see rankings mid-game