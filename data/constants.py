import pygame as pg
screen = pg.display.set_mode((1000, 600), pg.RESIZABLE)

font = pg.font.Font(None, 36)

background_image = pg.image.load("media/images/background.png")
background_image = pg.transform.scale(background_image, (1000, 600))

game_over_background = pg.image.load("media/images/background.png")
game_over_background = pg.transform.scale(game_over_background, (1000, 600))

reload_button = pg.image.load("media/images/buttons/reload.png")
reload_button = pg.transform.scale(reload_button, (70, 70))
pause_button = pg.image.load("media/images/buttons/pause.png")
pause_button = pg.transform.scale(pause_button, (70, 70))
resume_button = pg.image.load("media/images/buttons/resume.png")
resume_button = pg.transform.scale(resume_button, (70, 70))
reload_button = pg.image.load("media/images/buttons/reload.png")
reload_button = pg.transform.scale(reload_button, (70, 70))
ranking_button = pg.image.load("media/images/buttons/ranking.png")
ranking_button = pg.transform.scale(ranking_button, (70, 70))

gravity = 0.5
drag = 0.1

block_images = {
    "wood": { "1": "media/images/blocks/wood100.png", "0.8": "media/images/blocks/wood80.png", "0.6": "media/images/blocks/wood60.png", "0.4": "media/images/blocks/wood40.png", "0.2": "media/images/blocks/wood20.png" },
    "ice": {"1": "media/images/blocks/ice100.png", "0.8": "media/images/blocks/ice80.png", "0.6": "media/images/blocks/ice60.png", "0.4": "media/images/blocks/ice40.png", "0.2": "media/images/blocks/ice20.png"},
    "stone": {"1": "media/images/blocks/stone100.png", "0.8": "media/images/blocks/stone80.png", "0.6": "media/images/blocks/stone60.png", "0.4": "media/images/blocks/stone40.png", "0.2": "media/images/blocks/stone20.png"}
}

# block_rgb = {
#     "wood": (139, 69, 19),
#     "ice": (173, 216, 230),
#     "stone": (128, 128, 128)
# }

catapult_images = {
    "left": "media/images/catapults/left.png",
    "right": "media/images/catapults/right.png"
}

bird_images = {
    "Red": "media/images/birds/red.png",
    "Chuck": "media/images/birds/chuck.png",
    "Blues": "media/images/birds/blue.png",
    "Bomb": "media/images/birds/bomb.png",
    "Bomb_special": "media/images/birds/bomb_special.png",
}

bird_speeds = {
    "Red" : 23,
    "Chuck" : 23,
    "Blues" : 23,
    "Bomb" : 22
}

block_damage = {
    "Red": {"wood": 0.25, "ice": 0.25, "stone": 0.25},
    "Chuck": {"wood": 0.40, "ice": 0.20, "stone": 0.20},
    "Blues": {"wood": 0.20, "ice": 0.40, "stone": 0.20},
    "Bomb": {"wood": 0.20, "ice": 0.15, "stone": 0.40}
}


# make screen_height and screen_width be gloabl and independant -- not so hard-coded
# mention other global variables

# TO -DO :
'''HIGH PRIORITY'''
# - letting blues split into 3
# - let birds not be able to go through blocks when string is pulled onto the other side
# - let birds bounce - make bird.velocityy be negative when it hits the ground
'''MEDIUM PRIORITY'''
# - add trail to birds projectile - if speeded up then dots be conjusted or check accordingly
'''LOW PRIORITY'''
# - modularise code a bit more...
# - add a background music ?
# - make arenas with different backgrounds, fortress block types, and catapult types
