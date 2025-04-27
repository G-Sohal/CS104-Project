import pygame as pg
from data.constants import *
pg.init()

def leaderboard(score_sessions) :
    screen.blit(game_over_background, (0, 0))
    game_over_text = font.render("Leaderboard", True, "black")
    screen.blit(game_over_text, (400, 50))

    sorted_sessions = sorted(score_sessions, key=lambda x: x[1], reverse=True)
    for i, session in enumerate(sorted_sessions[:5]):
        player_text = font.render(f"{i + 1}. {session[0]} - {session[1]}", True, "black")
        screen.blit(player_text, (400, 100 + i * 30))

    exit_text = font.render("Press ESC to exit", True, "black")
    screen.blit(exit_text, (400, 250))

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

def ranking(players, score1, score2, done = False) :
    screen.blit(game_over_background, (0, 0))
    game_over_text = font_heading.render("Game Over", True, "red")
    screen.blit(game_over_text, (screen_width//2 - (game_over_text.get_width())//2, 50))

    if score1 > score2 :
        winner_text = font.render(f"{players[0]} won!", True, "black")
    elif score1 < score2 :
        winner_text = font.render(f"{players[1]} won!", True, "black")
    else :
        winner_text = font.render("It was a tie!", True, "black")
    screen.blit(winner_text, (screen_width//2 - (winner_text.get_width())//2, screen_height//4))

    score_text = font.render(f"Score: {score1} - {score2}", True, "black")
    screen.blit(score_text, (screen_width//2 - (score_text.get_width())//2, screen_height//4 + 100))

    if not done :
        resume_text = font.render("Left game mid-session? Press P to resume", True, "black")
        screen.blit(resume_text, (screen_width//2 - (resume_text.get_width())//2, screen_height//2))
    restart_text = font.render("Want to start over again? Press R to restart", True, "black")
    screen.blit(restart_text, (screen_width//2 - (restart_text.get_width())//2, 3*screen_height//4 - 100))
    exit_text = font.render("Press ESC to exit", True, "black")
    screen.blit(exit_text, (screen_width//2 - (exit_text.get_width())//2, screen_height - 150))

    running = True
    while running :
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN :
                if event.key == pg.K_r :
                    return "restart"
                elif event.key == pg.K_p and not done:
                    return "resume"
                if event.key == pg.K_ESCAPE :
                    return "exit"
        pg.display.flip()
 # Option  to go back is just wanted to see rankings mid-game