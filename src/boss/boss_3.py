import pygame as pg
from config import Config as CFG
import math
from .. import bullet as Bullet
from .boss import BossBase

class Boss3(BossBase):
    
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
        self.hp_max = 30000
        self.score  = 30000
        self.speeds = [5, 5, 8]
        
        self.surfaces = [pg.image.load(f"assets/boss/3_{i + 1}.png") for i in range(2)]
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
            self.shot_cycle -= 6
            
        if self.shot_cycle % 18 == 0:
            speed = 10
            rad = math.radians(self.shot_cycle)
            x, y = self.rect.center[0], self.rect.bottom,
            v_x, v_y = math.cos(rad), math.sin(rad)
            enemy_bullets.append(Bullet.BulletE2(x, y, v_x*speed, abs(v_y*speed)))
            
        if self.shot_cycle % 120 == 0:
            x, y = self.rect.center[0], self.rect.bottom,
            enemy_bullets.append(Bullet.BulletE1(x, y, 10, 10))
            enemy_bullets.append(Bullet.BulletE1(x, y, 0, 10))
            enemy_bullets.append(Bullet.BulletE1(x, y, -10, 10))
            
        if self.shot_cycle == 0:
            self.shot_cycle = 360 * CFG.fps
    
    
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
            self.shot_cycle -= 6
            
        if self.shot_cycle % 18 == 0:
            speed = 10
            rad = math.radians(self.shot_cycle)
            x, y = self.rect.center[0], self.rect.bottom,
            v_x_1, v_y_1 = math.cos(rad+10), math.sin(rad+10)
            v_x_2, v_y_2 = math.cos(-rad), math.sin(-rad)
            enemy_bullets.append(Bullet.BulletE2(x, y, v_x_1*speed, abs(v_y_1*speed)))
            enemy_bullets.append(Bullet.BulletE3(x, y, v_x_2*speed, abs(v_y_2*speed)))
            
            
        if self.shot_cycle % 120 == 0:
            x, y = self.rect.center[0], self.rect.bottom,
            enemy_bullets.append(Bullet.BulletE1(x, y, 10, 10))
            enemy_bullets.append(Bullet.BulletE1(x, y, 0, 10))
            enemy_bullets.append(Bullet.BulletE1(x, y, -10, 10))
            
        if self.shot_cycle == 0:
            self.shot_cycle = 360 * CFG.fps
    
    
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
        player_bullets : list[Bullet.BulletBase]
            プレイヤーが発射した弾のリスト
        """
        if self.shot_cycle > 0:
            self.shot_cycle -= 6
            
        if self.shot_cycle % 9 == 0:
            speed = 10
            rad = math.radians(self.shot_cycle)
            x, y = self.rect.center[0], self.rect.bottom,
            v_x_1, v_y_1 = math.cos(rad+10), math.sin(rad+10)
            v_x_2, v_y_2 = math.cos(-rad), math.sin(-rad)
            enemy_bullets.append(Bullet.BulletE2(x, y, v_x_1*speed, abs(v_y_1*speed)))
            enemy_bullets.append(Bullet.BulletE3(x, y, v_x_2*speed, abs(v_y_2*speed)))
            
            
        if self.shot_cycle % 60 == 0:
            x, y = self.rect.center[0], self.rect.bottom,
            enemy_bullets.append(Bullet.BulletE1(x, y, 10, 10))
            enemy_bullets.append(Bullet.BulletE1(x, y, 0, 10))
            enemy_bullets.append(Bullet.BulletE1(x, y, -10, 10))
            
        if self.shot_cycle == 0:
            self.shot_cycle = 360 * CFG.fps