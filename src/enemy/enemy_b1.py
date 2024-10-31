import pygame as pg

from .enemy import EnemyBase
from config import Config as CFG

class EnemyB1(EnemyBase):
    
    def __init__(
        self,
        x: int,
        y: int,
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
               
        # hp, score, surface を上書き
        self.score = 100
        self.hp = 3
        
        self.surface = pg.image.load('assets/enemy/b1_enemy.png')
        self.surface = pg.transform.scale(self.surface, (self.w, self.h))
    
    
    def update(self, bullets: list[pg.Surface]) -> int:
        """雑魚敵の更新処理

        Parameters
        ----------
        bullet : list[pg.Surface]
            自機が発射した弾のリスト

        Returns
        -------
        int
            - 撃破: スコア
            - 消滅: -1
            - それ以外: 0
        """
        
        # 移動の処理を書く
        self.rect.x += 10
        self.rect.x %= CFG.screen_w
        
        
        return super().update(bullets)
        
        