import pygame as pg
import sys
from data.constants import *

def player_names():
    players = []
    name = ""
    running = True
    while running:
        screen.blit(front_bg_image, (0, 0))
        if len(players) == 0:
          statement = "Enter the name of the first player :"
        else:
          statement = "Enter the name of the second player :"

        statement_surface = font_heading.render(statement, True, "black")
        screen.blit(statement_surface, (screen_width//2 - (statement_surface.get_width())//2,
                                         screen_height//2 - (statement_surface.get_height())//2 - 100))

        name_surface = font.render(name, True, "black")
        text_width = max(name_surface.get_width(), 150)
        coordinates = pg.Rect(screen_width//2 - text_width//2, screen_height//2, text_width, 50)

        color = (0, 124, 124) if len(name) == 0 else (0, 200, 200)
        pg.draw.rect(screen, color, coordinates, border_radius=5)
        screen.blit(name_surface, name_surface.get_rect(center=coordinates.center))

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if len(name) : players.append(name)
                    name = ""
                    if len(players) == 2:
                        running = False
                elif event.key == pg.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
    return players

def mode():
    screen.blit(front_bg_image, (0, 0))
    mode_text = [
        font_heading.render("TIMED MODE", True, "black"),
        font_heading.render("FORTRESS DESTRUCTION", True, "black")
    ]
    coordinates = [None, None]
    running = True

    while running:
        screen.blit(front_bg_image, (0, 0))

        coordinates[0] = pg.Rect(screen_width//2 - (mode_text[0].get_width())//2 - 10,
                              screen_height//2 - mode_text[0].get_height() - 100, 
                              mode_text[0].get_width() + 20, 
                              mode_text[0].get_height() + 20)
        coordinates[1] = pg.Rect(screen_width//2 - (mode_text[1].get_width())//2 - 10,
                              screen_height//2 + mode_text[1].get_height() + 100, 
                              mode_text[1].get_width() + 20, 
                              mode_text[1].get_height() + 20)

        for i in range(2):
            color = (0, 124, 124) if coordinates[i].collidepoint(pg.mouse.get_pos()) else (0, 62, 62)
            pg.draw.rect(screen, color, (coordinates[i]), border_radius=10)
            screen.blit(mode_text[i], (coordinates[i].x + 10,
                                        coordinates[i].y + 10))

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if coordinates[0].collidepoint(event.pos):
                    return 1
                elif coordinates[1].collidepoint(event.pos):
                    return 2

def level():
    screen.blit(front_bg_image, (0, 0))
    running = True

    titles = ["EASY", "MEDIUM", "HARD"]
    descriptions = [
        "No wind effect",
        "Wind effect",
        "Wind & Moving blocks"
    ]
    sub_descriptions = [
        "Great for beginners!",
        "Bit challenging!",
        "For experienced players!"
    ]

    coordinates = []

    while running:
        screen.blit(front_bg_image, (0, 0))
        coordinates.clear()

        for i in range(3):
            x = (screen_width // 4) * (i + 1)

            title_surf = font_heading.render(titles[i], True, "black")
            desc_surf = font.render(descriptions[i], True, "black")
            subdesc_surf = font.render(sub_descriptions[i], True, "black")

            width = max(title_surf.get_width(), desc_surf.get_width(), subdesc_surf.get_width()) + 20
            height = title_surf.get_height() + desc_surf.get_height() + subdesc_surf.get_height() + 30

            rect = pg.Rect(x - width // 2, screen_height // 2 - height // 2, width, height)
            coordinates.append(rect)

            color = (0, 124, 124) if rect.collidepoint(pg.mouse.get_pos()) else (0, 62, 62)
            pg.draw.rect(screen, color, rect, border_radius=10)

            screen.blit(title_surf, title_surf.get_rect(centerx=rect.centerx, y=rect.y + 10))
            screen.blit(desc_surf, desc_surf.get_rect(centerx=rect.centerx, y=rect.y + 15 + title_surf.get_height()))
            screen.blit(subdesc_surf, subdesc_surf.get_rect(centerx=rect.centerx, y=rect.y + 20 + title_surf.get_height() + desc_surf.get_height()))

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if coordinates[0].collidepoint(event.pos):
                    return 0
                elif coordinates[1].collidepoint(event.pos):
                    return 1
                elif coordinates[2].collidepoint(event.pos):
                    return 2

def start_button() :
  screen.blit(front_bg_image, (0, 0))
  # screen.blit(settings_button, (10, 10))
  
  running =  True
  while running :
    coordinates = pg.Rect(400, 275, 200, 50)

    color = (0, 124, 124) if coordinates.collidepoint(pg.mouse.get_pos()) else (0, 62, 62)
    pg.draw.rect(screen, color, coordinates, border_radius=10)

    start_text = font_heading.render("START", True, "black")
    screen.blit(start_text, start_text.get_rect(center=coordinates.center))

    pg.display.flip()

    for event in pg.event.get() :
      if event.type == pg.QUIT :
        pg.quit()
        sys.quit()
      elif event.type == pg.MOUSEBUTTONDOWN :
        if coordinates.collidepoint(event.pos):
          running = False

# def settings() :
#   screen.fill((128, 128, 128), (10, 10, 980, 580))
#   screen.blit(settings_button, (10, 10))
# for sound effects, music, etc.
#   running = True
#   while running :
#     for event in pg.event.get() :
       
#   pg.display.flip()