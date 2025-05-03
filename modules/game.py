import pygame as pg
import sys, random, math
from modules.game_objects.block import *
from modules.game_objects.catapult import *
from modules.game_objects.fortress import *
from modules.game_objects.bird import *
from modules.game_over import ranking
from data import constants

class Game :
    clock = pg.time.Clock()

    def __init__(self, players, mode, level, rows, cols, method):
        self.players = players
        self.mode = mode
        self.level = level
        self.rows = rows
        self.cols = cols
        self.moving = level > 1
        self.catapults = [Catapult(150 + rows*50, constants.ground, "left"), Catapult(constants.screen_width - 220 - 50*rows, constants.ground, "right")]
        self.fortresses = [Fortress(90, constants.ground - 50*(cols + 1), rows, cols, self.moving), Fortress(constants.screen_width - 90 - 50*rows, constants.ground - 50*(cols + 1), rows, cols, self.moving)]
        self.birds = [None, None]
        self.bird_list = []
        # FOR CARD DECK GENERATION METHOD
        self.deck = {
            0 : random.choices(["Red", "Chuck", "Bomb", "Blues"], k=3),
            1 : random.choices(["Red", "Chuck", "Bomb", "Blues"], k=3),
        }
        self.card_rects = {
            0: [
                pg.Rect(50, constants.ground + 5, constants.cw, constants.ch),
                pg.Rect(150, constants.ground + 5, constants.cw, constants.ch),
                pg.Rect(250, constants.ground + 5, constants.cw, constants.ch),
            ],
            1: [
                pg.Rect(constants.screen_width - 300, constants.ground + 5, constants.cw, constants.ch),
                pg.Rect(constants.screen_width - 200, constants.ground + 5, constants.cw, constants.ch),
                pg.Rect(constants.screen_width - 100, constants.ground + 5, constants.cw, constants.ch),
            ],
        }
        self.score = [0, 0]
        # RANDOM ASSIGNMENT OF FIRST TURN ENSURING FAIRNESS
        self.turn = random.randint(0, 1)
        self.dragging = False
        self.running = True
        self.game_over = False
        self.projectile_coordinates = []
        self.special_effect_coordinates = []
        self.start_time = pg.time.get_ticks()
        # TO ENSURE CLOCK TIME STAYS THE SAME WHEN GAME IS PAUSED.
        self.pause_time = 0
        constants.background_image = pg.transform.scale(constants.background_image, screen.get_size())
        self.method = method
        # WHETHER OR NOT TO DISPLAY INFO BUTTON; DESCRIBES THE STATE OF TOGGLE
        self.info = False

    def run(self):
        while self.running:
            # RENDERING OF BACKGROUND AND BUTTONS
            constants.screen.blit(constants.background_image, (0, 0))
            constants.screen.blit(constants.pause_button, constants.button_rect.topleft)
            constants.screen.blit(constants.reload_button, constants.reload_rect.topleft)
            constants.screen.blit(constants.ranking_button, constants.ranking_rect.topleft)
            constants.screen.blit(constants.music_button[int(constants.music)], constants.music_rect.topleft)
            constants.screen.blit(constants.info_button, constants.info_rect.topleft)

            # RENDERING OF CATAPULTS ON THE SCREEN
            self.catapults[0].construct(constants.screen)
            self.catapults[1].construct(constants.screen)
            self.fortresses[0].construct(constants.screen)
            self.fortresses[1].construct(constants.screen)

            # DISPLAYING LIVE GAME EVENT STATS - CURRENT SCORE, TURN AND TIME REMAINING
            player_turn = constants.font.render(f"{self.players[self.turn]}'s Turn", True, "black")
            scoreboard = constants.font.render(f"Score: {self.score[0]} - {self.score[1]}", True, "black")

            # DISPLAY TIMER ONLY IF TIMED MODE WAS SELECTED
            if self.mode == 1:
                time = int(60 - ((pg.time.get_ticks() - self.start_time - self.pause_time) / 1000))
                colour = "black" if time > 10 else "red"
                time_left = constants.font.render(f"Time Left: {time}", True, colour)
                if time <= 0:
                    ranking(self.players, self.score[0], self.score[1], True)
                    self.running = False
                constants.screen.blit(time_left, (constants.screen_width//2 - (time_left.get_width())//2, constants.screen_height//4 - 50))
            
            constants.screen.blit(player_turn, (constants.screen_width//2 - (player_turn.get_width())//2, constants.screen_height//4 - 100))
            constants.screen.blit(scoreboard, (constants.screen_width//2 - (scoreboard.get_width())//2, constants.screen_height//4 - 150))

            # DISPLAY INFO STATEMENT IF TOGGLED ON
            if self.info :
                info_statement = "Press SPCAEBAR to activate special projectile effect"
                info_statement_surface = constants.font_small.render(info_statement, True, "black")
                constants.screen.blit(info_statement_surface, (180, 100))


            # IMMEDIATELY AFTER TURN OF THE PLAYER SHOWS UP; BEFORE THE PROJECTILE IS LAUNCHED
            if self.birds[self.turn] is None:
                # CLEAR THE PROJECTILE POINTS FOR A NEW TRAIL TO BE MARKED BY WHITE DOTS
                self.projectile_coordinates = []
                self.special_effect_coordinates = []
                # SHOW THE AVAILABLE BIRDS THE PLAYER CAN CHOOSE FROM IF METHOD IS DECK DRAW
                if self.method :
                    for i, bird in enumerate(self.deck[self.turn]) :
                        constants.screen.blit(constants.card_images[bird], self.card_rects[self.turn][i])
                # OTHERWISE RANDOMLY CHOOSE A PROJECTILE FOR THE PLAYER IN TURN
                else :
                    x = self.catapults[self.turn].rect.centerx - 25
                    y = self.catapults[self.turn].rect.top - 10
                    self.birds[self.turn] = Bird(x, y, random.choice(["Red", "Chuck", "Blues", "Bomb",]), self.turn)
                    self.bird_list.append(self.birds[self.turn])

            # USING BIRD_LIST IN CASE OF MULTIPLE BIRDS IN FLIGHT - LIKE BLUES
            # UPDATE TRAJECTORY POINTS BASED ON CURRENT POSITION FOR EACH BIRD IN BIRD_LIST
            for bird in self.bird_list:
                if bird.special_effect_used: self.special_effect_coordinates.append(bird.rect.center)
                elif not self.dragging: self.projectile_coordinates.append(bird.rect.center)
                bird.update(self.level)
                bird.draw(constants.screen)

            # MAKING THE BIRD DISAPPEAR IF IT SUCCESSFULLY COLLIDES WITH A BLOCK OR MOVES OUT OF VISIBLE SCREEN DIMENSIONS
            new_list = [] # LIST OF BIRDS STILL IN MOTION AND CAPABLE OF HITTING A BLOCK
            for bird in self.bird_list:
                hit = False
                for block in self.fortresses[1 - self.turn].blocks[:]:
                    if bird.rect.colliderect(block.rect):
                        damage = bird.damage[block.type]
                        self.score[self.turn] += int(damage*20) # TO AVOID FLOATS SINCE DAMAGE IS A FLOAT
                        if block.hit(damage):
                            # self.fortresses[1 - self.turn].existing_blocks[block.row, block.col] = False
                            self.fortresses[1 - self.turn].blocks.remove(block)
                            for b in self.fortresses[1 - self.turn].blocks:
                                if b.row == block.row and b.col <= block.col:
                                    b.falling = True # TO MAKE BLOCKS FALL UNER GRAVITY
                            self.score[self.turn] += 50 # BONUS POINTS FOR COMPLETE DAMAGE
                        hit = True
                        break
                if hit:
                    continue # BIRD INCAPABLE OF FURTHER HITS SO DISAPPEAR
                if not bird.is_launched:
                    new_list.append(bird)
                elif 0 <= bird.rect.centerx <= constants.screen_width and bird.rect.bottom < constants.screen_height:
                    new_list.append(bird) # BIRD STILL IN MOTION AND NOT HIT.
            self.bird_list = new_list

            # CHECK IF ALL BIRDS IN MOTION;
            # IF NOT - SWAP THE TURN
            if self.birds[self.turn] is not None and self.birds[self.turn].is_launched:
                done = True
                for bird in self.bird_list :
                    if bird.turn == self.turn and bird.is_launched :
                        done = False
                if done : 
                    self.birds[self.turn] = None
                    self.turn = 1 - self.turn

            # EXIT THE GAME IF A FORTRESS GETS COMPLETELY DESTROYED
            if not self.fortresses[0].blocks:
                ranking(self.players, self.score[0], self.score[1], True)
                self.running = False
            if not self.fortresses[1].blocks:
                ranking(self.players, self.score[0], self.score[1], True)
                self.running = False

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.VIDEORESIZE:
                    # UPDATING GLOBAL CONSTANTS IF WINDOW IS RESIZED
                    constants.screen_width = event.w
                    constants.screen_height = event.h
                    constants.ground = event.h * 0.87
                    constants.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    constants.background_image = pg.transform.scale(constants.background_image, (event.w, event.h))
                    constants.music_rect = pg.Rect((constants.screen_width-80, 10), (constants.w, constants.h))

                    self.catapults[0].rect.x = 150 + 50*self.rows
                    self.catapults[0].rect.bottom = constants.ground
                    self.catapults[1].rect.x = constants.screen_width - 220 - 50*self.rows
                    self.catapults[1].rect.bottom = constants.ground
                    if self.method :
                        self.card_rects = {
                            0: [
                                pg.Rect(50, constants.ground + 5, constants.cw, constants.ch),
                                pg.Rect(150, constants.ground + 5, constants.cw, constants.ch),
                                pg.Rect(250, constants.ground + 5, constants.cw, constants.ch),
                            ],
                            1: [
                                pg.Rect(constants.screen_width - 300, constants.ground + 5, constants.cw, constants.ch),
                                pg.Rect(constants.screen_width - 200, constants.ground + 5, constants.cw, constants.ch),
                                pg.Rect(constants.screen_width - 100, constants.ground + 5, constants.cw, constants.ch),
                            ],
                        }
                    if self.birds[self.turn] :
                        self.birds[self.turn].rect.topleft = (self.catapults[self.turn].rect.centerx - 25, self.catapults[self.turn].rect.top - 10)

                    self.fortresses[0].set_position(90, constants.ground - 50*(self.cols + 1))
                    self.fortresses[1].set_position(constants.screen_width - 90 - 50 * self.rows, constants.ground - 50*(self.cols + 1))

                    self.dragging = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if constants.button_rect.collidepoint(pg.mouse.get_pos()):
                        pause_start = pg.time.get_ticks()
                        constants.screen.blit(resume_button, button_rect.topleft)
                        paused = True
                        while paused:
                            for event in pg.event.get():
                                if event.type == pg.QUIT:
                                    self.running = False
                                    paused = False
                                elif event.type == pg.MOUSEBUTTONDOWN:
                                    if button_rect.collidepoint(pg.mouse.get_pos()):
                                        constants.screen.blit(pause_button, button_rect.topleft)
                                        paused = False
                            pg.display.flip()
                            self.clock.tick(30)
                        pause_end = pg.time.get_ticks()
                        # TIME ELAPSED DURING PAUSE- CREATES OFFSET
                        self.pause_time += pause_end - pause_start
                    elif constants.reload_rect.collidepoint(pg.mouse.get_pos()):
                        # RECREATE __INIT__ CONDITIONS
                        self.catapults = [Catapult(150 + self.rows*50, constants.ground, "left"), Catapult(constants.screen_width - 220 - 50*self.rows, constants.ground, "right")]
                        self.fortresses = [Fortress(90, constants.ground - 50*(self.cols + 1), self.rows, self.cols, self.moving), Fortress(constants.screen_width - 90 - 50*self.rows, constants.ground - 50*(self.cols + 1), self.rows, self.cols, self.moving)]
                        self.birds = [None, None]
                        self.bird_list = []
                        self.score = [0, 0]
                        self.turn = 0
                        self.start_time = pg.time.get_ticks()
                        self.pause_time = 0
                        continue
                    elif constants.ranking_rect.collidepoint(pg.mouse.get_pos()):
                        pause_start = pg.time.get_ticks()
                        result = ranking(self.players, self.score[0], self.score[1])
                        pause_end = pg.time.get_ticks()
                        self.pause_time += pause_end - pause_start
                        if result == 'resume':
                            continue
                        elif result == 'exit':
                            pg.quit()
                            exit()
                    elif constants.music_rect.collidepoint(pg.mouse.get_pos()):
                        if pg.mixer.music.get_busy():
                            pg.mixer.music.pause()
                            constants.music = False
                        else:
                            pg.mixer.music.unpause()    
                            constants.music = True         
                    elif constants.info_rect.collidepoint(pg.mouse.get_pos()) :
                        self.info = bool(1 - int(self.info))
                    elif self.birds[self.turn] and not self.birds[self.turn].is_launched:
                        self.drag_start = self.birds[self.turn].rect.center
                        self.dragging = True
                    elif not self.dragging and self.birds[self.turn] is None and self.method:
                        for i, rect in enumerate(self.card_rects[self.turn]) :
                            if rect.collidepoint(event.pos) :
                                selected_bird = self.deck[self.turn][i]
                                new_bird = Bird(self.catapults[self.turn].rect.centerx - 25, self.catapults[self.turn].rect.top - 10, selected_bird, self.turn)
                                self.birds[self.turn] = new_bird
                                self.bird_list.append(new_bird)
                                self.deck[self.turn][i] = random.choice(["Red", "Chuck", "Bomb", "Blues"])
                                break
                elif event.type == pg.MOUSEMOTION:
                    if self.dragging and self.birds[self.turn] and not self.birds[self.turn].is_launched:
                        current_pos = pg.mouse.get_pos()
                        sling_x, sling_y = self.catapults[self.turn].rect.centerx, self.catapults[self.turn].rect.top + 25
                        dx = current_pos[0] - sling_x
                        dy = current_pos[1] - sling_y
                        distance = math.hypot(dx, dy)

                        # LIMIT TO THE ELASTICITY OF THE SLING
                        if distance > 90:
                            scale = 90/distance
                            dx *= scale
                            dy *= scale

                        self.birds[self.turn].rect.center = (sling_x + dx, sling_y + dy)
                        # # DRAW THE SLING - WILL GLITCH HERE
                        # end_positionx = sling_x + dx
                        # end_positiony = sling_y + dy
                        # end_position = (end_positionx, end_positiony)
                        # pg.draw.line(constants.screen, (139, 69, 19), (sling_x - 10, sling_y), end_position, 4)
                        # pg.draw.line(constants.screen, (139, 69, 19), (sling_x + 15, sling_y), end_position, 4)
                        # self.birds[self.turn].rect.center = current_pos
                elif event.type == pg.MOUSEBUTTONUP:
                    if self.birds[self.turn] and self.dragging:
                        drag_end = self.birds[self.turn].rect.center
                        dx = self.drag_start[0] - drag_end[0]
                        dy = self.drag_start[1] - drag_end[1]
                        theta = math.atan2(dy, dx)
                        if abs(dx) < 5:
                            theta = math.pi / 2
                        elif abs(dy) < 5:
                            theta = 0
                        self.birds[self.turn].velocityy = self.birds[self.turn].speed * math.sin(theta) * abs(dx) * 0.013
                        self.birds[self.turn].velocityx = self.birds[self.turn].speed * math.cos(theta) * abs(dy) * 0.013
                        
                        # LIMIT THE OVERALL SPEED
                        self.birds[self.turn].velocityx = max(-20, min(20, self.birds[self.turn].velocityx))
                        self.birds[self.turn].velocityy = max(-20, min(20, self.birds[self.turn].velocityy))
                        self.birds[self.turn].is_launched = True
                        self.dragging = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE and self.birds[self.turn] and self.birds[self.turn].is_launched:
                        self.bird_list = self.birds[self.turn].special_effect()

            # CREATED OUTSIDE EVENT LOOP FOR NO GLITCHING
            if self.birds[self.turn]:
                # DRAW THE SLING
                if self.dragging:
                    sling_x, sling_y = self.catapults[self.turn].rect.centerx, self.catapults[self.turn].rect.top + 30
                    bird_x, bird_y = self.birds[self.turn].rect.centerx, self.birds[self.turn].rect.centery
                    dx = bird_x - sling_x
                    dy = bird_y - sling_y
                    distance = math.hypot(dx, dy)
                    if distance > 90:
                        scale = 90 / distance
                        dx *= scale
                        dy *= scale
                    end_positionx = sling_x + dx
                    end_positiony = sling_y + dy
                    end_position = (end_positionx, end_positiony)
                    self.birds[self.turn].rect.center = (end_positionx, end_positiony)
                    pg.draw.line(constants.screen, (139, 69, 19), (sling_x - 10, sling_y), end_position, 4)
                    pg.draw.line(constants.screen, (139, 69, 19), (sling_x + 15, sling_y), end_position, 4)
                # DRAW THE TRAJECTORY
                elif self.birds[self.turn].is_launched:
                    # LEAVE A TRAIL OF WHITE CIRCLES - SPECIAL TRAJECTORY EFFECTS
                    for coord in self.projectile_coordinates:
                        pg.draw.circle(constants.screen, (255, 255, 255), coord, 3.5)
                    for coord in self.special_effect_coordinates:
                        if self.birds[self.turn].type == "Red":
                            # A TRAIL OF RED FEATHERS IF BIRD TYPE IS RED; OTHERWISE CIRCLES ONLY.
                            constants.screen.blit(red_feathers[self.turn], coord)
                        else:
                            pg.draw.circle(constants.screen, (255, 255, 255), coord, 3.5)
            pg.display.flip()
            self.clock.tick(60)

        pg.quit()
        sys.exit()
        return abs(self.score[0] - self.score[1])