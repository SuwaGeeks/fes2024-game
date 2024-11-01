import pygame as pg

from config import Config as CFG

class Title(pg.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.is_continue = False
        self.font_title = pg.font.SysFont(None, 64)
        self.font_hint = pg.font.SysFont(None, 32)
        
    def update(self):
        self.text_title = self.font_title.render(f'Pyun Pyun 2', True, pg.Color('WHITE'))
        self.text_hint = self.font_hint.render(f'press enter to play', True, pg.Color('WHITE'))
        
        
        # ボタンを押すとアクションを実行
        joy = pg.joystick.Joystick(0)
        key = pg.key.get_pressed()
        if any(key) or any([joy.get_button(btn) for btn in range(joy.get_numbuttons())]):
            self.is_continue = True
        
    def blit(self, screen: pg.Surface) -> None:
        text_center = CFG.screen_w / 2 - self.text_title.get_width() / 2
        screen.blit(self.text_title, (text_center, 300))
        
        text_center = CFG.screen_w / 2 - self.text_hint.get_width() / 2
        screen.blit(self.text_hint, (text_center, 350))