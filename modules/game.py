import pygame as pg
import sys, random, math
from modules.game_objects.block import *
from modules.game_objects.catapult import *
from modules.game_objects.fortress import *
from modules.game_objects.bird import *
from modules.game_over import ranking
from data.constants import *

pg.init()

pg.display.set_caption("Angry Birds v2.0")

(w, h) = (70, 70)
button_rect = pg.Rect((10, 10), (w, h))
reload_rect = pg.Rect((70, 10), (w, h))
ranking_rect = pg.Rect((130, 10), (w, h))

clock = pg.time.Clock()

def run_game(players):
  catapults = [Catapult(200, 450, "left"), Catapult(740, 450, "right")]
  fortresses = [Fortress(10, 350, 3, 5), Fortress(840, 350, 3, 5)]
    
  birds = [None, None]
  score = [0, 0]
  turn = 0

  dragging = False
  running = True
  game_over = False

  while running:
    screen.blit(background_image, (0, 0))
    screen.blit(pause_button, button_rect.topleft)
    screen.blit(reload_button, reload_rect.topleft)
    screen.blit(ranking_button, ranking_rect.topleft)

    catapults[0].construct(screen)
    catapults[1].construct(screen)
    fortresses[0].construct(screen)
    fortresses[1].construct(screen)

    player_turn = font.render(f"{players[turn]}'s Turn", True, "black")
    scoreboard = font.render(f"Score: {score[0]} - {score[1]}", True, "black")
    screen.blit(player_turn, (400, 50))
    screen.blit(scoreboard, (400, 100))

    if birds[turn] is None :
      x = catapults[turn].rect.centerx - 25
      y = catapults[turn].rect.top - 10
      birds[turn] = Bird(x, y, random.choice(["Red", "Chuck", "Blues", "Bomb"]), turn)
      bird = birds[turn]

    else :
      bird.update()
      bird.draw(screen)

      for block in fortresses[1-turn].blocks[:] :
        if bird.rect.colliderect(block.rect) :
          damage = bird.damage(block.type)
          if block.hit(damage) :
            fortresses[1-turn].existing_blocks[block.row, block.col] = False
            fortresses[1-turn].blocks.remove(block)

            for b in fortresses[1-turn].blocks:
              if b.row == block.row and b.col <= block.col:
                b.falling = True

            score[turn] += 1
          birds[turn] = None
          turn = 1 - turn
          break
      if (bird.rect.y > 550 or bird.rect.x < 0 or bird.rect.x > 1000) and bird.is_launched :
        birds[turn] = None
        turn = 1 - turn
        
      for event in pg.event.get() :

        if event.type == pg.QUIT:
          running = False
        
        elif event.type == pg.MOUSEBUTTONDOWN :
          if button_rect.collidepoint(pg.mouse.get_pos()):
            screen.blit(resume_button, button_rect.topleft)
            paused = True 
            while paused:
              for event in pg.event.get():
                  if event.type == pg.QUIT:
                      running = False
                      paused = False
                  elif event.type == pg.MOUSEBUTTONDOWN:
                      if button_rect.collidepoint(pg.mouse.get_pos()):
                          screen.blit(pause_button, button_rect.topleft)
                          paused = False
              pg.display.flip()
              clock.tick(30)
          elif reload_rect.collidepoint(pg.mouse.get_pos()):
              catapults = [Catapult(200, 450, "left"), Catapult(740, 450, "right")]
              fortresses = [Fortress(10, 400, 3, 5), Fortress(840, 400, 3, 5)]
                
              birds = [None, None]
              score = [0, 0]
              turn = 0
              continue
          elif ranking_rect.collidepoint(pg.mouse.get_pos()):
            game_over = True
            running = False
            ranking(players, score[0], score[1])
          elif bird and not bird.is_launched :
            drag_start = pg.mouse.get_pos()
            dragging = True
        elif event.type == pg.MOUSEMOTION:
            if dragging and bird and not bird.is_launched:
                current_pos = pg.mouse.get_pos()
                bird.rect.center = current_pos
        elif event.type == pg.MOUSEBUTTONUP :
          if bird and dragging :
            drag_end = pg.mouse.get_pos()
            dx = drag_start[0] - drag_end[0]
            dy = drag_start[1] - drag_end[1]
            theta = math.atan2(dy, dx)
            bird.velocityy = bird.speed * math.sin(theta)
            bird.velocityx = bird.speed * math.cos(theta)
            bird.is_launched = True
            dragging = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and bird and bird.is_launched:
                bird.special_effect()
    
      if dragging and bird:
            sling_x, sling_y = catapults[turn].rect.centerx, catapults[turn].rect.top + 30
            pg.draw.line(screen, (139, 69, 19), (sling_x - 10, sling_y), bird.rect.center, 5)
            pg.draw.line(screen, (139, 69, 19), (sling_x + 10, sling_y), bird.rect.center, 5)

      pg.display.flip()
      clock.tick(60)
  
  if game_over :
    ranking(players, score[0], score[1])
  
  pg.quit()
  sys.exit()        