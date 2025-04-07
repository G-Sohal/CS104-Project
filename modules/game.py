import pygame as pg
import sys, random, math
from modules.game_objects import *

pg.init()

screen = pg.display.set_mode((1000, 600), pg.RESIZABLE)
pg.display.set_caption("Angry Birds v2.0")
background_image = pg.image.load("media/images/background.png")
background_image = pg.transform.scale(background_image, (1000, 600))

clock = pg.time.Clock()

font = pg.font.Font(None, 36)

def run_game(players):
  catapults = [Catapult(200, 450, "left"), Catapult(740, 450, "right")]
  fortresses = [Fortress(10, 400, 5), Fortress(840, 400, 5)]
    
  birds = [None, None]
  score = [0, 0]
  turn = 0

  dragging = False
  running = True

  while running:
    screen.blit(background_image, (0, 0))

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
            fortresses[1-turn].blocks.remove(block)
            score[turn] += 1
          birds[turn] = None
          turn = 1 - turn
          break
      if (bird.rect.y > 600 or bird.rect.x < 0 or bird.rect.x > 1000) and bird.is_launched :
        birds[turn] = None
        turn = 1 - turn
        
      for event in pg.event.get() :
        if event.type == pg.QUIT :
          running = False
        elif event.type == pg.MOUSEBUTTONDOWN :
          if bird and not bird.is_launched :
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
  pg.quit()
  sys.exit()        