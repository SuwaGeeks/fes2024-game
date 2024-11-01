import pygame as pg

class Config():
    
    key_map = {
        'exit' : pg.K_ESCAPE,
        'shot' : pg.K_z,
        'up'   : pg.K_UP,
        'down' : pg.K_DOWN,
        'right': pg.K_RIGHT,
        'left' : pg.K_LEFT,
    }
    
    pad_map = {
        'exit' : 0,
        'shot' : 1,
    }

    use_gamepad = False
    
    is_debug = True

    
    # Game settings
    fps = 60
    screen_w = 600
    screen_h = 800
    
    # UI settings
    ui_frame_width = 5
    ui_frame_bottom_width = 96
    
    # area limits
    top_limit = ui_frame_width
    bottom_limit = screen_h - ui_frame_bottom_width
    right_limit = screen_w - ui_frame_width
    left_limit = ui_frame_width
    
    
    # Player settings
    player_speed = 10
    player_shot_cycle = 20
    player_god_time = 2 * fps
    
    player_default_level = 1
    player_default_hp = 3
    player_default_mp = 3
    
    
    # Enemy settings
    enemy_ttl = 15 * fps