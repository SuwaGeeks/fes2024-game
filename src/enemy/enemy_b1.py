import pygame as pg
import random
import math

from .enemy import EnemyBase
from ..bullet.bullet_p1 import BulletP1
from ..bullet.bullet import BulletBase
from config import Config as CFG

class EnemyB1(EnemyBase):
    
    def __init__(
        self,
        x: int = None,
        y: int = None,
        w: int = 48,
        h: int = 48
    ) -> None:
        """雑魚敵を作成

        Parameters
        ----------
        x : int
            雑魚敵の初期x座標
        y : int
            雑魚敵の初期y座標
        w : int
            雑魚敵の横幅
        h : int
            雑魚敵の高さ
        """
        super().__init__(x, y, w, h)
        
        # 弾の一定間隔に発射するために用意
        self.shot_cycle = 1 * CFG.fps
        self.speed  = 5
        
        self.ttl = CFG.enemy_ttl
        self.dist_x, self.dist_y = self._random_pos_to_move()
               
        # hp, score, surface を上書き
        self.score = 100
        self.hp = 3
        
        self.surface = pg.image.load('assets/enemy/b1_enemy.png')
        self.surface = pg.transform.scale(self.surface, (self.w, self.h))
    
    
    def update(
        self, 
        enemy_bullets: list[BulletBase],
        player_bullets: list[BulletBase],
    ) -> int:
        """雑魚敵の更新処理

        Parameters
        ----------
        enemy_bullets : list[BulletBase]
            が発射した弾のリスト
        player_bullets : list[BulletBase]
            プレイヤーが発射した弾のリスト

        Returns
        -------
        int
            - 撃破: スコア
            - 消滅: -1
            - それ以外: 0
        """
        
        self.ttl -= 1
        self.shot_cycle -= 1
        
        # 移動の処理を書く
        x = self.dist_x - self.rect.x
        y = self.dist_y - self.rect.y
        norm = math.sqrt(x**2 + y**2)
        
        if norm > 5:
            self.rect.x += (x / norm) * self.speed
            self.rect.y += (y / norm) * self.speed
        else:
            self.dist_x, self.dist_y = self._random_pos_to_move()
            
        # タイムオーバの敵は画面外にフェードアウト
        if self.ttl < 0:
            self.dist_x, self.dist_y = self._random_pos_to_despawn()  
        
        
        # 弾の発射処理，enemy_bulletsに弾のインスタンスをappendすれば弾が発射される
        if self.shot_cycle == 0:
            enemy_bullets.append(BulletP1(self.rect.center[0], self.rect.top, 0, 20))
            self.shot_cycle = 60
        
        
        return super().update(enemy_bullets, player_bullets)
        
        