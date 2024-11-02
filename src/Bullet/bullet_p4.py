import pygame as pg
from config import Config as CFG
from .bullet import BulletBase

class BulletP4(BulletBase):
    
    def __init__(
        self,
        x: int,
        y: int,
        v_x: int,
        v_y: int,
        w: int = 12,
        h: int= 36
    ) -> None:
        """弾を生成

        Parameters
        ----------
        x : int
            初期x座標
        y : int
            初期y座標
        v_x : int
            x軸方向の速度
        v_y : int
            y軸方向の速度
        w : int
            横幅
        h : int
            縦幅
        """
        super().__init__(x, y, v_x, v_y, w, h)
        
        pg.mixer.Sound("assets/sounds/shot.mp3").play()
        
        # surface, damage をオーバライド
        self.damage  = 5
        self.surface = pg.image.load('assets/bullet/p4_bullet.png')
        self.surface = pg.transform.scale(self.surface, (self.w, self.h))
    
    
    def update(self):
        """弾の更新処理
        """
        super().update()
        
        # 移動処理を書く
        self.rect.x += self.v_x
        self.rect.y += self.v_y
        
        