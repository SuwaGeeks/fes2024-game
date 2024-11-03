import pygame as pg


from .enemy import EnemyBase
from ..Bullet.bullet_e1 import BulletE1
from ..Bullet.bullet import BulletBase
from config import Config as CFG

class EnemyY3(EnemyBase):
    
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
               
        # hp, score, speed, surface を上書き
        self.score = 120
        self.hp    = 1000
        self.speed = 3
        
        self.surfaces = [pg.image.load(f"assets/enemy/y3_{i + 1}.png") for i in range(2)]
        self.surfaces = [pg.transform.scale(surface, (self.h, self.w)) for surface in self.surfaces]
    
    
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
        self.shot_cycle -= 1
        
        # 弾の発射処理，enemy_bulletsに弾のインスタンスをappendすれば弾が発射される
        if self.shot_cycle == 0:
            enemy_bullets.append(BulletE1(self.rect.center[0], self.rect.bottom, 10, 5))
            enemy_bullets.append(BulletE1(self.rect.center[0]+50, self.rect.bottom+50, 10, 5))
            enemy_bullets.append(BulletE1(self.rect.center[0]+100, self.rect.bottom+100, 10, 5))

            enemy_bullets.append(BulletE1(self.rect.center[0], self.rect.bottom, -10, 5))
            enemy_bullets.append(BulletE1(self.rect.center[0]+50, self.rect.bottom+50, -10, 5))
            enemy_bullets.append(BulletE1(self.rect.center[0]+100, self.rect.bottom+100, -10, 5))
            self.shot_cycle = 80

        return super().update(enemy_bullets, player_bullets)
        
        