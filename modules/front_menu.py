import pygame as pg
import sys

pg.init()

screen = pg.display.set_mode((1000, 600), pg.RESIZABLE)
pg.display.set_caption("Angry Birds v2.0")
front_bg_image = pg.image.load("media/images/front_background.jpg")
front_bg_image = pg.transform.scale(front_bg_image, (1000, 600))

font = pg.font.Font(None, 36)
font_heading = pg.font.Font(None, 42)
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
        screen.blit(statement_surface, (300, 220))

        coordinates = pg.Rect(400, 275, 200, 50)

        color = (0, 124, 124) if len(name) == 0 else (0, 200, 200)
        pg.draw.rect(screen, color, coordinates, border_radius=5)

        name_surface = font.render(name, True, "black")
        screen.blit(name_surface, name_surface.get_rect(center=coordinates.center))

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    players.append(name)
                    name = ""
                    if len(players) == 2:
                        running = False
                elif event.key == pg.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
    return players

def start_button() :
  screen.blit(front_bg_image, (0, 0))

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