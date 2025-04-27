import pygame as pg
import sys, random, math
from modules.game_objects.block import *
from modules.game_objects.catapult import *
from modules.game_objects.fortress import *
from modules.game_objects.bird import *
from modules.game_over import ranking
from data.constants import *

class Game:
    screen_width = screen_width
    screen_height = screen_height
    screen = screen
    background_image = background_image
    clock = pg.time.Clock()

    def __init__(self, players, mode, level, rows, cols):
        self.players = players
        self.mode = mode
        self.level = level
        self.rows = rows
        self.cols = cols
        self.moving = level > 0
        self.catapults = [Catapult(60 + cols*50, self.screen_height*0.75, "left"), Catapult(self.screen_width - 120 - 50*cols, self.screen_height*0.75, "right")]
        self.fortresses = [Fortress(20, self.screen_height*0.66, 3, 4, self.moving), Fortress(self.screen_width - 20 - 50*cols, self.screen_height*0.66, 3, 4, self.moving)]
        self.birds = [None, None]
        self.bird_list = []
        self.score = [0, 0]
        self.initial_turn = random.randint(0, 1)
        self.turn = self.initial_turn
        self.dragging = False
        self.running = True
        self.game_over = False
        self.projectile_coordinates = []
        self.special_effect_coordinates = []
        self.start_time = pg.time.get_ticks()
        self.pause_time = 0

    def run(self):
        while self.running:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(pause_button, button_rect.topleft)
            self.screen.blit(reload_button, reload_rect.topleft)
            self.screen.blit(ranking_button, ranking_rect.topleft)

            self.catapults[0].construct(self.screen)
            self.catapults[1].construct(self.screen)
            self.fortresses[0].construct(self.screen)
            self.fortresses[1].construct(self.screen)

            player_turn = font.render(f"{self.players[self.turn]}'s Turn", True, "black")
            scoreboard = font.render(f"Score: {self.score[0] * 20 :.0f} - {self.score[1] * 20 :.0f}", True, "black")

            if self.mode == 1:
                time = int(60 - ((pg.time.get_ticks() - self.start_time - self.pause_time) / 1000))
                colour = "black" if time > 10 else "red"
                time_left = font.render(f"Time Left: {time}", True, colour)
                if time <= 0:
                    ranking(self.players, self.score[0], self.score[1], True)
                    self.running = False
                self.screen.blit(time_left, (self.screen_width//2 - (time_left.get_width())//2, self.screen_height//4 - 50))
            self.screen.blit(player_turn, (self.screen_width//2 - (player_turn.get_width())//2, self.screen_height//4 - 100))
            self.screen.blit(scoreboard, (self.screen_width//2 - (scoreboard.get_width())//2, self.screen_height//4 - 150))

            if self.birds[self.turn] is None:
                self.projectile_coordinates = []
                self.special_effect_coordinates = []
                x = self.catapults[self.turn].rect.centerx - 25
                y = self.catapults[self.turn].rect.top - 10
                self.birds[self.turn] = Bird(x, y, random.choice(["Red", "Chuck", "Blues", "Bomb",]), self.turn)
                self.bird_list.append(self.birds[self.turn])

            for bird in self.bird_list:
                if bird.special_effect_used: self.special_effect_coordinates.append(bird.rect.center)
                elif not self.dragging: self.projectile_coordinates.append(bird.rect.center)
                bird.update(self.level)
                bird.draw(self.screen)

            new_list = []
            for bird in self.bird_list:
                hit = False
                for block in self.fortresses[1 - self.turn].blocks[:]:
                    if bird.rect.colliderect(block.rect):
                        damage = bird.damage[block.type]
                        self.score[self.turn] += damage
                        if block.hit(damage):
                            self.fortresses[1 - self.turn].existing_blocks[block.row, block.col] = False
                            self.fortresses[1 - self.turn].blocks.remove(block)
                            for b in self.fortresses[1 - self.turn].blocks:
                                if b.row == block.row and b.col <= block.col:
                                    b.falling = True
                            self.score[self.turn] += 1
                        hit = True
                        break
                if hit:
                    continue
                if not bird.is_launched:
                    new_list.append(bird)
                elif 0 <= bird.rect.centerx <= self.screen_width and bird.rect.bottom < self.screen_width:
                    new_list.append(bird)
            self.bird_list = new_list

            if self.birds[self.turn] is not None and self.birds[self.turn].is_launched:
                active_birds = [b for b in self.bird_list if b.turn == self.turn and b.is_launched]
                if len(active_birds) == 0:
                    self.birds[self.turn] = None
                    self.turn = 1 - self.turn

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.VIDEORESIZE:
                    self.screen_width = event.w
                    self.screen_height = event.h
                    self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    self.background_image = pg.transform.scale(self.background_image, (event.w, event.h))
                    self.catapults[0].rect.x = 60 + self.cols * 50
                    self.catapults[0].rect.y = self.screen_height * 0.75
                    self.catapults[1].rect.x = self.screen_width - 120 - 50 * self.cols
                    self.catapults[1].rect.y = self.screen_height * 0.75
                    self.fortresses[0].set_position(20, self.screen_height * 0.66)
                    self.fortresses[1].set_position(self.screen_width - 20 - 50 * self.cols, self.screen_height * 0.66)
                    self.dragging = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(pg.mouse.get_pos()):
                        self.screen.blit(resume_button, button_rect.topleft)
                        paused = True
                        while paused:
                            for event in pg.event.get():
                                if event.type == pg.QUIT:
                                    self.running = False
                                    paused = False
                                elif event.type == pg.MOUSEBUTTONDOWN:
                                    if button_rect.collidepoint(pg.mouse.get_pos()):
                                        self.screen.blit(pause_button, button_rect.topleft)
                                        paused = False
                            pg.display.flip()
                            self.clock.tick(30)
                    elif reload_rect.collidepoint(pg.mouse.get_pos()):
                        self.catapults = [Catapult(self.screen_width//60 + 200, self.screen_height*0.75, "left"), Catapult(self.screen_width - 360, self.screen_height*0.75, "right")]
                        self.fortresses = [Fortress(self.screen_width//60, self.screen_height*0.66, 3, 4, self.moving), Fortress(self.screen_width - 160, self.screen_height*0.66, 3, 4, self.moving)]
                        self.birds = [None, None]
                        self.bird_list = []
                        self.score = [0, 0]
                        self.turn = 0
                        continue
                    elif ranking_rect.collidepoint(pg.mouse.get_pos()):
                        pause_start = pg.time.get_ticks()
                        result = ranking(self.players, self.score[0], self.score[1])
                        pause_end = pg.time.get_ticks()
                        self.pause_time += pause_end - pause_start
                        if result == 'resume':
                            continue
                        elif result == 'restart':
                            pass
                        elif result == 'exit':
                            pg.quit()
                            exit()
                    elif self.birds[self.turn] and not self.birds[self.turn].is_launched:
                        self.drag_start = self.birds[self.turn].rect.center
                        self.dragging = True
                elif event.type == pg.MOUSEMOTION:
                    if self.dragging and self.birds[self.turn] and not self.birds[self.turn].is_launched:
                        current_pos = pg.mouse.get_pos()
                        self.birds[self.turn].rect.center = current_pos
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
                        self.birds[self.turn].is_launched = True
                        self.dragging = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE and self.birds[self.turn] and self.birds[self.turn].is_launched:
                        self.bird_list = self.birds[self.turn].special_effect()

            if self.birds[self.turn]:
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
                    pg.draw.line(self.screen, (139, 69, 19), (sling_x - 10, sling_y), end_position, 3)
                    pg.draw.line(self.screen, (139, 69, 19), (sling_x + 15, sling_y), end_position, 3)
                elif self.birds[self.turn].is_launched:
                    for coord in self.projectile_coordinates:
                        pg.draw.circle(self.screen, (255, 255, 255), coord, 3.5)
                    for coord in self.special_effect_coordinates:
                        if self.birds[self.turn].type == "Red":
                            self.screen.blit(red_feathers[self.turn], coord)
                        else:
                            pg.draw.circle(self.screen, (255, 255, 255), coord, 3.5)
            pg.display.flip()
            self.clock.tick(60)

        pg.quit()
        sys.exit()
        return abs(self.score[0] - self.score[1])