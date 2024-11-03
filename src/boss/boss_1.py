import pygame as pg
from config import Config as CFG
from ..bullet.bullet import Bullet
from .boss import BossBase

class Boss1(BossBase):
    
    def __init__(self, w = 48, h = 48):
        """ボスを作成

        Parameters
        ----------
        w : int
            ボスの横幅
        h : int
            ボスの高さ
        """
        super().__init__(w, h)
        
        self.shot_cycle = 0
        
        # 以下のパラメータをオーバライド
        self.hp_max = 10000
        self.score  = 10000
        self.speeds = [5, 5, 8]
        
        
        self.surfaces = [pg.image.load(f"assets/boss/1_{i + 1}.png") for i in range(2)]
        self.surfaces = [pg.transform.scale(surface, (self.h, self.w)) for surface in self.surfaces]
        
        
    def _update_1(
        self, 
        enemy_bullets: list[Bullet.BulletBase],
        player_bullets: list[Bullet.BulletBase],
    ) -> None:
        """ボスの更新処理(第1形態)
        オーバーライドして動作を実装

        Parameters
        ----------
        enemy_bullets : list[Bullet.BulletBase]
            敵が発射した弾のリスト
        player_bullets : list[Bullet.BulletBase]
            プレイヤーが発射した弾のリスト
        """
        if self.shot_cycle > 0:
            self.shot_cycle -= 1
        
        if self.shot_cycle == 0:
            x, y = self.rect.center[0], self.rect.bottom,
            enemy_bullets.append(Bullet.BulletE2(x, y, 10, 10))
            enemy_bullets.append(Bullet.BulletE2(x, y, 0, 10))
            enemy_bullets.append(Bullet.BulletE2(x, y, -10, 10))
            self.shot_cycle = 0.5 * CFG.fps
    
    
    def _update_2(
        self, 
        enemy_bullets: list[Bullet.BulletBase],
        player_bullets: list[Bullet.BulletBase],
    ) -> None:
        """ボスの更新処理(第1形態)
        オーバーライドして動作を実装
        
        Parameters
        ----------
        enemy_bullets : list[Bullet.BulletBase]
            敵が発射した弾のリスト
        player_bullets : list[Bullet.BulletBase]
            プレイヤーが発射した弾のリスト
        """
        if self.shot_cycle > 0:
            self.shot_cycle -= 1
        
        if self.shot_cycle == int(0.5 * CFG.fps / 2):
            x, y = self.rect.center[0], self.rect.bottom,
            enemy_bullets.append(Bullet.BulletE3(x, y, 5, 10))
            enemy_bullets.append(Bullet.BulletE3(x, y, -5, 10))
            
        if self.shot_cycle == 0:
            x, y = self.rect.center[0], self.rect.bottom,
            enemy_bullets.append(Bullet.BulletE2(x, y, 10, 10))
            enemy_bullets.append(Bullet.BulletE2(x, y, 0, 10))
            enemy_bullets.append(Bullet.BulletE2(x, y, -10, 10))
            self.shot_cycle = 0.5 * CFG.fps
    
    
    def _update_3(
        self, 
        enemy_bullets: list[Bullet.BulletBase],
        player_bullets: list[Bullet.BulletBase],
    ) -> None:
        """ボスの更新処理(第1形態)
        オーバーライドして動作を実装

        Parameters
        ----------
        enemy_bullets : list[Bullet.BulletBase]
            敵が発射した弾のリスト
        player_bullets : list[BulletBase]
            プレイヤーが発射した弾のリスト
        """
        if self.shot_cycle > 0:
            self.shot_cycle -= 1
        
        if self.shot_cycle == int(0.5 * CFG.fps / 2):
            x, y = self.rect.center[0], self.rect.bottom,
            enemy_bullets.append(Bullet.BulletE3(x, y, 5, 10))
            enemy_bullets.append(Bullet.BulletE3(x, y, -5, 10))
            
        if self.shot_cycle == 0:
            x, y = self.rect.center[0], self.rect.bottom,
            enemy_bullets.append(Bullet.BulletE2(x, y, 10, 10))
            enemy_bullets.append(Bullet.BulletE2(x, y, 0, 10))
            enemy_bullets.append(Bullet.BulletE2(x, y, -10, 10))
            self.shot_cycle = 0.5 * CFG.fps