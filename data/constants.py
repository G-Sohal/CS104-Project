import pygame as pg
screen_width = 1080
screen_height = 630
screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)

font = pg.font.Font(None, 36)
font_heading = pg.font.Font(None, 42)

background_image = pg.image.load("media/images/background.png")
background_image = pg.transform.scale(background_image, screen.get_size())

game_over_background = pg.image.load("media/images/background.png")
game_over_background = pg.transform.scale(game_over_background, screen.get_size())

front_bg_image = pg.image.load("media/images/front_background.jpg")
front_bg_image = pg.transform.scale(front_bg_image, (screen_width, screen_height))

(w, h) = (80, 80)

reload_button = pg.image.load("media/images/buttons/reload.png")
reload_button = pg.transform.scale(reload_button, (w, h))
pause_button = pg.image.load("media/images/buttons/pause.png")
pause_button = pg.transform.scale(pause_button, (w, h))
resume_button = pg.image.load("media/images/buttons/resume.png")
resume_button = pg.transform.scale(resume_button, (w, h))
reload_button = pg.image.load("media/images/buttons/reload.png")
reload_button = pg.transform.scale(reload_button, (w, h))
ranking_button = pg.image.load("media/images/buttons/ranking.png")
ranking_button = pg.transform.scale(ranking_button, (w, h))
# settings_button = pg.image.load("media/images/buttons/settings.png")

button_rect = pg.Rect((10, 10), (w, h))
reload_rect = pg.Rect((70, 10), (w, h))
ranking_rect = pg.Rect((130, 10), (w, h))

gravity = 0.5
drag = 0.5

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

bird_images_motion = {
    "Red": "media/images/birds/red.png",
    "Chuck": "media/images/birds/chuck.png",
    "Blues": "media/images/birds/blue.png",
    "Bomb": "media/images/birds/bomb.png",
}

bird_images_hit = {
    
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

red_feather = pg.image.load("media/images/red_feather.png").convert_alpha()
red_feather = pg.transform.scale(red_feather, (screen_width//50, screen_width//50))
red_feathers = [
    red_feather,
    pg.transform.flip(red_feather, True, False),
]

bomb_damage = pg.image.load("media/images/bomb_damage.png").convert_alpha()
# make screen_height and screen_width be gloabl and independant -- not so hard-coded
# mention other global variables

# TO -DO :
'''HIGH PRIORITY'''
# - moving blocks customization
# - let birds bounce - make bird.velocityy be negative when it hits the ground
'''MEDIUM PRIORITY'''
'''LOW PRIORITY'''
# - modularise code a bit more...
# - add a background music ?
# - make arenas with different backgrounds, fortress block types, and catapult types
