import pygame as pg
screen_width = 1500
screen_height = 800
screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)

font = pg.font.Font("media/fonts/angrybirds.ttf", 36)
font_heading = pg.font.Font("media/fonts/angrybirds.ttf", 42)

angry_birds_logo = pg.image.load("media/images/logo.png")
angry_birds_logo = pg.transform.scale(angry_birds_logo, (screen_width*0.6, screen_height//3))

background_image = pg.image.load("media/images/background1.jpg")
background_image = pg.transform.scale(background_image, screen.get_size())

game_over_background = pg.image.load("media/images/background1.jpg")
game_over_background = pg.transform.scale(game_over_background, screen.get_size())

front_bg_image = pg.image.load("media/images/background1.jpg")
front_bg_image = pg.transform.scale(front_bg_image, (screen_width, screen_height))

pg.mixer.init()
pg.mixer.music.load("media/sounds/theme_song.ogg")
pg.mixer.music.play(-1) 
pg.mixer.music.set_volume(0.7)
music = True

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
music_on_button = pg.image.load("media/images/buttons/music.png")
music_on_button = pg.transform.scale(music_on_button, (w, h))
music_off_button = pg.image.load("media/images/buttons/music_off.png")
music_off_button = pg.transform.scale(music_off_button, (w, h))
music_button = [music_off_button, music_on_button]
play_button =  pg.image.load("media/images/buttons/play.png")
play_button = pg.transform.scale(play_button, (200, 150))

button_rect = pg.Rect((10, 10), (w, h))
reload_rect = pg.Rect((70, 10), (w, h))
ranking_rect = pg.Rect((130, 10), (w, h))
music_rect = pg.Rect((screen_width-80, 10), (w, h))

ground = screen_height * 0.87 ## check

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

bird_images_motion = {
    "Red": "media/images/birds/red.png",
    "Chuck": "media/images/birds/chuck.png",
    "Blues": "media/images/birds/blue.png",
    "Bomb": "media/images/birds/bomb.png",
}

bird_images_hit = {
    
}

cw, ch = 60, 90
red_card = pg.image.load("media/images/cards/red_card.png")
red_card = pg.transform.scale(red_card, (cw, ch))
chuck_card = pg.image.load("media/images/cards/chuck_card.png")
chuck_card = pg.transform.scale(chuck_card, (cw, ch))
blues_card = pg.image.load("media/images/cards/blues_card.png")
blues_card = pg.transform.scale(blues_card, (cw, ch))
bomb_card = pg.image.load("media/images/cards/bomb_card.png")
bomb_card = pg.transform.scale(bomb_card, (cw, ch))

card_images = {
    "Red" : red_card,
    "Chuck" : chuck_card,
    "Blues" : blues_card,
    "Bomb" : bomb_card,
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
# - let birds bounce - make bird.velocityy be negative when it hits the ground
'''MEDIUM PRIORITY'''
'''LOW PRIORITY'''
# - modularise code a bit more...
# - add a background music ?
# - make arenas with different backgrounds, fortress block types, and catapult types
