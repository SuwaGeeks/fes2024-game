import pygame as pg
from config import Config as CFG
from ..Bullet.bullet import BulletBase
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
        self.hp_max = 10
        self.score  = 10000
        
        self.surface = pg.image.load('assets/boss/1_1.png')
        self.surface = pg.transform.scale(self.surface, (self.w, self.h))
        
        
    def _update_1(
        self, 
        enemy_bullets: list[BulletBase],
        player_bullets: list[BulletBase],
    ) -> None:
        """ボスの更新処理(第1形態)
        オーバーライドして動作を実装

        Parameters
        ----------
        enemy_bullets : list[BulletBase]
            敵が発射した弾のリスト
        player_bullets : list[BulletBase]
            プレイヤーが発射した弾のリスト
        """
        self.rect.x += 5
        self.rect.x %= CFG.screen_w
    
    
    def _update_2(
        self, 
        enemy_bullets: list[BulletBase],
        player_bullets: list[BulletBase],
    ) -> None:
        """ボスの更新処理(第1形態)
        オーバーライドして動作を実装
        
        Parameters
        ----------
        enemy_bullets : list[BulletBase]
            敵が発射した弾のリスト
        player_bullets : list[BulletBase]
            プレイヤーが発射した弾のリスト
        """
        self.rect.x += 15
        self.rect.x %= CFG.screen_w
    
    
    def _update_3(
        self, 
        enemy_bullets: list[BulletBase],
        player_bullets: list[BulletBase],
    ) -> None:
        """ボスの更新処理(第1形態)
        オーバーライドして動作を実装

        Parameters
        ----------
        enemy_bullets : list[BulletBase]
            敵が発射した弾のリスト
        player_bullets : list[BulletBase]
            プレイヤーが発射した弾のリスト
        """
        self.rect.x += 25
        self.rect.x %= CFG.screen_w