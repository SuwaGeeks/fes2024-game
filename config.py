import pygame as pg

class Config():
    
    key_map = {
        'exit' : pg.K_ESCAPE,
        'up'   : pg.K_UP,
        'down' : pg.K_DOWN,
        'right': pg.K_RIGHT,
        'left' : pg.K_LEFT,
    }
    
    pad_map = {
        
    }
    
    is_debug = True
    
    screen_w = 800
    screen_h = 600
    
    player_speed = 10
    player_default_level = 1
    player_default_hp = 1
    player_default_mp = 1