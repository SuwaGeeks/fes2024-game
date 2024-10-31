import pygame as pg
from src.player.player import Player
from src.enemy.enemy_b1 import EnemyB1
from src.enemy.enemy import EnemyBase

from config import Config as CFG

class GameManager():
    """ゲーム全体を管理するクラス
    
    """
    
    def __init__(self, screen_w: int, screen_h: int):
        pg.init()
        self.screen = pg.display.set_mode((screen_w, screen_h))
        
        self.ui = None
        self.player = Player(screen_w/2 - 48/2, screen_h*0.8, 48, 48)
        
        self.score = 0
        self.player_bullets = []
        self.enemy_bullets = []
        self.enemies: list[EnemyBase] = []
        self.boss = None
        
        self.enemies.append(EnemyB1(100, 100))
    
    
    def update(self):
        self.player.update()
        # TODO: 敵の消滅処理
        # TODO: スコアの加算
        enemy_rets = [enemy.update(self.player_bullets) for enemy in self.enemies]
        pg.display.update()
        
    
    def blit(self):
        self.screen.fill(pg.Color("WHITE")) 
        
        for enemy in self.enemies:
            enemy.blit(self.screen)
            
        self.player.blit(self.screen)
        
    
    def delay(self):
        pg.time.Clock().tick(60)
    
    
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