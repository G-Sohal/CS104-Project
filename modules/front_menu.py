import pygame as pg
import sys
from data import constants

class FrontMenu :
    def dimension_fortress(self) :
        constants.screen.blit(constants.front_bg_image, (0, 0))
        constants.screen.blit(constants.music_button[int(constants.music)], constants.music_rect.topleft)
        statement_rows = "Enter the number of rows of the fortress :"
        statement_cols = "Enter the number of columns of the fortress :"
        running = True
        rows = ""
        cols = ""
        dim = "rows"
        while running :
                constants.screen.blit(constants.front_bg_image, (0, 0))
                constants.screen.blit(constants.music_button[int(constants.music)], constants.music_rect.topleft)

                statement_surface_rows = constants.font_heading.render(statement_rows, True, "black")
                statement_surface_cols = constants.font_heading.render(statement_cols, True, "black")

                constants.screen.blit(statement_surface_rows, (constants.screen_width//2 - (statement_surface_rows.get_width())//2, constants.screen_height//2 - (statement_surface_rows.get_height())//2 - 100))
                constants.screen.blit(statement_surface_cols, (constants.screen_width//2 - (statement_surface_cols.get_width())//2, constants.screen_height//2 - (statement_surface_cols.get_height())//2 + 100))
                
                rows_surface = constants.font.render(rows, True, "black")
                cols_surface = constants.font.render(cols, True, "black")
                text_width = max(rows_surface.get_width(), 150)

                coordinates_rows = pg.Rect(constants.screen_width//2 - text_width//2, constants.screen_height//2 - 50, text_width, 50)
                coordinates_cols = pg.Rect(constants.screen_width//2 - text_width//2, constants.screen_height//2 + 150, text_width, 50)

                color_rows = (63, 191, 127) if len(rows) == 0 else (0, 200, 200)
                color_cols = (63, 191, 127) if len(cols) == 0 else (0, 200, 200)

                pg.draw.rect(constants.screen, color_rows, coordinates_rows, border_radius=5)
                pg.draw.rect(constants.screen, color_cols, coordinates_cols, border_radius=5)

                constants.screen.blit(rows_surface, rows_surface.get_rect(center=coordinates_rows.center))
                constants.screen.blit(cols_surface, cols_surface.get_rect(center=coordinates_cols.center))

                pg.display.flip()
                for event in pg.event.get() :
                    if event.type == pg.QUIT :
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.VIDEORESIZE :
                        constants.screen_width = event.w
                        constants.screen_height = event.h
                        constants.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                        constants.front_bg_image = pg.transform.scale(constants.front_bg_image, (event.w, event.h))
                    elif event.type == pg.MOUSEBUTTONDOWN :
                        if coordinates_rows.collidepoint(event.pos) :
                            dim = "rows"
                        elif coordinates_cols.collidepoint(event.pos) :
                            dim = "cols"
                        elif constants.music_rect.collidepoint(pg.mouse.get_pos()):
                            if pg.mixer.music.get_busy():
                                pg.mixer.music.pause()
                                constants.music = False
                            else:
                                pg.mixer.music.unpause()    
                                constants.music = True  
                    elif event.type == pg.KEYDOWN :
                        if event.key == pg.K_RETURN and rows.isdigit() and cols.isdigit() :
                            if int(rows) > 0 and int(cols) > 0:
                                return (int(rows), int(cols))
                        elif event.key == pg.K_BACKSPACE :
                            if dim == "rows":
                                rows = rows[:-1]
                            elif dim == "cols":
                                cols = cols[:-1]
                        elif event.key == pg.K_TAB :
                            if dim == "rows" :
                                dim = "cols"
                            else :
                                dim = "rows"
                        elif event.key == pg.K_DOWN :
                            dim = "cols"
                        elif event.key == pg.K_UP :
                            dim = "rows"
                        else :
                            if event.unicode.isdigit() :
                                if dim == "rows":
                                    rows += event.unicode
                                elif dim == "cols":
                                    cols += event.unicode

    def player_names(self):
        players = []
        name = ""
        running = True
        while running:
            constants.screen.blit(constants.front_bg_image, (0, 0))
            constants.screen.blit(constants.music_button[int(constants.music)], constants.music_rect.topleft)
            if len(players) == 0:
                statement = "Enter the name of the first player :"
            else:
                statement = "Enter the name of the second player :"

            statement_surface = constants.font_heading.render(statement, True, "black")
            constants.screen.blit(statement_surface, (constants.screen_width//2 - (statement_surface.get_width())//2, constants.screen_height//2 - (statement_surface.get_height())//2 - 100))

            name_surface = constants.font.render(name, True, "black")
            text_width = max(name_surface.get_width(), 150)
            coordinates = pg.Rect(constants.screen_width//2 - text_width//2, constants.screen_height//2, text_width, 50)

            color = (63, 191, 127) if len(name) == 0 else (0, 200, 200)
            pg.draw.rect(constants.screen, color, coordinates, border_radius=5)
            constants.screen.blit(name_surface, name_surface.get_rect(center=coordinates.center))

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.VIDEORESIZE :
                    constants.screen_width = event.w
                    constants.screen_height = event.h
                    constants.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    constants.front_bg_image = pg.transform.scale(constants.front_bg_image, (event.w, event.h))
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
                elif event.type == pg.MOUSEBUTTONDOWN :
                    if constants.music_rect.collidepoint(pg.mouse.get_pos()):
                        if pg.mixer.music.get_busy():
                            pg.mixer.music.pause()
                            constants.music = False
                        else:
                            pg.mixer.music.unpause()    
                            constants.music = True  
        return players

    def mode(self):
        constants.screen.blit(constants.front_bg_image, (0, 0))
        constants.screen.blit(constants.music_button[int(constants.music)], constants.music_rect.topleft)
        mode_text = [
            constants.font_heading.render("TIMED MODE", True, "black"),
            constants.font_heading.render("FORTRESS DESTRUCTION", True, "black")
        ]
        coordinates = [None, None]
        running = True

        while running:
            constants.screen.blit(constants.front_bg_image, (0, 0))
            constants.screen.blit(constants.music_button[int(constants.music)], constants.music_rect.topleft)

            coordinates[0] = pg.Rect(constants.screen_width//2 - (mode_text[0].get_width())//2 - 10,
                                constants.screen_height//2 - mode_text[0].get_height() - 100, 
                                mode_text[0].get_width() + 20, 
                                mode_text[0].get_height() + 20)
            coordinates[1] = pg.Rect(constants.screen_width//2 - (mode_text[1].get_width())//2 - 10,
                                constants.screen_height//2 + mode_text[1].get_height() + 100, 
                                mode_text[1].get_width() + 20, 
                                mode_text[1].get_height() + 20)

            for i in range(2):
                color = (63, 191, 127) if coordinates[i].collidepoint(pg.mouse.get_pos()) else (45, 169, 106)
                pg.draw.rect(constants.screen, color, (coordinates[i]), border_radius=10)
                constants.screen.blit(mode_text[i], (coordinates[i].x + 10, coordinates[i].y + 10))

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.VIDEORESIZE :
                    constants.screen_width = event.w
                    constants.screen_height = event.h
                    constants.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    constants.front_bg_image = pg.transform.scale(constants.front_bg_image, (event.w, event.h))
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if coordinates[0].collidepoint(event.pos):
                        return 1
                    elif coordinates[1].collidepoint(event.pos):
                        return 2
                    elif constants.music_rect.collidepoint(pg.mouse.get_pos()):
                        if pg.mixer.music.get_busy():
                            pg.mixer.music.pause()
                            constants.music = False
                        else:
                            pg.mixer.music.unpause()    
                            constants.music = True  

    def level(self):
        constants.screen.blit(constants.front_bg_image, (0, 0))
        constants.screen.blit(constants.music_button[int(constants.music)], constants.music_rect.topleft)
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
            constants.screen.blit(constants.front_bg_image, (0, 0))
            coordinates.clear()
            constants.screen.blit(constants.music_button[int(constants.music)], constants.music_rect.topleft)

            for i in range(3):
                x = (constants.screen_width // 4) * (i + 1)

                title_surf = constants.font_heading.render(titles[i], True, "black")
                desc_surf = constants.font.render(descriptions[i], True, "black")
                subdesc_surf = constants.font.render(sub_descriptions[i], True, "black")

                width = max(title_surf.get_width(), desc_surf.get_width(), subdesc_surf.get_width()) + 20
                height = title_surf.get_height() + desc_surf.get_height() + subdesc_surf.get_height() + 30

                rect = pg.Rect(x - width // 2, constants.screen_height // 2 - height // 2, width, height)
                coordinates.append(rect)

                color = (63, 191, 127) if rect.collidepoint(pg.mouse.get_pos()) else (45, 169, 106)
                pg.draw.rect(constants.screen, color, rect, border_radius=10)

                constants.screen.blit(title_surf, title_surf.get_rect(centerx=rect.centerx, y=rect.y + 10))
                constants.screen.blit(desc_surf, desc_surf.get_rect(centerx=rect.centerx, y=rect.y + 15 + title_surf.get_height()))
                constants.screen.blit(subdesc_surf, subdesc_surf.get_rect(centerx=rect.centerx, y=rect.y + 20 + title_surf.get_height() + desc_surf.get_height()))

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.VIDEORESIZE :
                    constants.screen_width = event.w
                    constants.screen_height = event.h
                    constants.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    constants.front_bg_image = pg.transform.scale(constants.front_bg_image, (event.w, event.h))
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if coordinates[0].collidepoint(event.pos):
                        return 0
                    elif coordinates[1].collidepoint(event.pos):
                        return 1
                    elif coordinates[2].collidepoint(event.pos):
                        return 2
                    elif constants.music_rect.collidepoint(pg.mouse.get_pos()):
                        if pg.mixer.music.get_busy():
                            pg.mixer.music.pause()
                            constants.music = False
                        else:
                            pg.mixer.music.unpause()    
                            constants.music = True  

    def start_button(self) :
        constants.screen.blit(constants.angry_birds_logo, (0, 0))
        constants.screen.blit(constants.front_bg_image, (0, 0))
        constants.screen.blit(constants.music_button[int(constants.music)], constants.music_rect.topleft)
        
        running =  True
        while running :
            constants.screen.blit(constants.front_bg_image, (0, 0))
            constants.screen.blit(constants.angry_birds_logo, (constants.screen_width*0.1, 20))
            constants.screen.blit(constants.music_button[int(constants.music)], constants.music_rect.topleft)
            play_button_rect = constants.play_button.get_rect(center=(constants.screen_width // 2, constants.screen_height // 2))
            constants.screen.blit(constants.play_button, play_button_rect)

            pg.display.flip()

            for event in pg.event.get() :
                if event.type == pg.QUIT :
                    pg.quit()
                    sys.exit()
                elif event.type == pg.VIDEORESIZE :
                    constants.screen_width = event.w
                    constants.screen_height = event.h
                    constants.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    constants.front_bg_image = pg.transform.scale(constants.front_bg_image, (event.w, event.h))
                    constants.angry_birds_logo = pg.transform.scale(constants.angry_birds_logo, (event.w*0.75, event.h//3))
                elif event.type == pg.MOUSEBUTTONDOWN :
                    if play_button_rect.collidepoint(event.pos):
                        running = False
                    elif constants.music_rect.collidepoint(pg.mouse.get_pos()):
                        if pg.mixer.music.get_busy():
                            pg.mixer.music.pause()
                            constants.music = False
                        else:
                            pg.mixer.music.unpause()    
                            constants.music = True  

