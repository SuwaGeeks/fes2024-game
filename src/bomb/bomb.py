import pygame as pg
import math
from typing import Union
from config import Config as CFG

from ..enemy.enemy import EnemyBase
from ..player.player import Player

class Bomb(pg.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.is_bomming = False
        self.damage = 100
        self.radius = 0
        self.speed = 16
        self.player_id = None
        self.x = None
        self.y = None
        self.damaged_enemy_ids = set()
        
        
    def bomb(
        self,
        player: Player,
    ) -> None:
        
        if not self.is_bomming and player.mp > 0:
            pg.mixer.Sound('assets/sounds/bomb.mp3').play()
            self.is_bomming = True
            self.player_id = player.id
            self.x, self.y = player.rect.center
            self.damaged_enemy_ids = set()
            player.mp -= 1
            return True
        else:
            return False

        
    def update(
        self,
        enemies: list[EnemyBase],
        boss
        # TODO: bomb と player が循環参照するので良くない
        # boss: Union[BossBase, None]
    ) -> None:
        """ボムのアップデート

        Parameters
        ----------
        enemies : list[EnemyBase]
            敵のインスタンス
        boss : Union[BossBase, None]
            ボスのインスタンス
        """
        if (self.is_bomming):
            self.radius += self.speed
            
            # 範囲内の雑魚敵にダメージを与える
            for enemy in enemies:
                x, y = enemy.rect.center
                r = math.sqrt((x-self.x)**2 + (y-self.x)**2)
                
                if self.radius > r and id(enemy) not in self.damaged_enemy_ids:
                    enemy.hp -= self.damage
                    self.damaged_enemy_ids.add(id(enemy))
            
            # 範囲内のボスにダメージを与える
            if boss is not None:
                x, y = boss.rect.center
                r = math.sqrt((x-self.x)**2 + (y-self.x)**2)
                
                if self.radius > r and id(boss) not in self.damaged_enemy_ids:
                    boss.hp -= self.damage
                    self.damaged_enemy_ids.add(id(boss))
                    
                    
            # 半径が画面よりも大きくなればボムを終了
            if self.radius > max(CFG.screen_h, CFG.screen_w):
                self.is_bomming = False
                self.radius = 0
                self.damaged_enemy_ids = set()
    
    def blit(
            self, 
            screen: pg.Surface
        ) -> None:
        """ボムを描画する

        Parameters
        ----------
        screen : pg.Surface
            スクリーンのオブジェクト
        """
        if self.is_bomming:
            pg.draw.circle(screen, '#00bfff', (self.x, self.y), self.radius, 3)