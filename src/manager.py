import pygame as pg
from src.player.player import Player

from config import Config as CFG

class GameManager():
    """ゲーム全体を管理するクラス
    
    """
    
    def __init__(self, screen_w: int, screen_h: int):
        pg.init()
        self.screen = pg.display.set_mode((screen_w, screen_h))
        self.player = Player(screen_w/2 - 48/2, screen_h*0.7, 48, 48)
        
    
    def blit(self):
        self.screen.fill(pg.Color("WHITE")) 
        self.player.blit(self.screen)
    
    def update(self):
        self.player.update()
        pg.display.update()
        
    def is_continue(self) -> bool:
        
        # windowの[x]ボタンで終了
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return False
            
        # ゲームに割り当てられた終了ボタンで終了
        key = pg.key.get_pressed()
        if key[CFG.key_map['exit']]:
            pg.quit()
            return False
            
        return True