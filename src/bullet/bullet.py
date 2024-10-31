import pygame as pg
from config import Config as CFG

class BulletBase(pg.sprite.Sprite):
    
    
    def __init__(
        self,
        x: int,
        y: int,
        v_x: int,
        v_y: int,
        w: int,
        h: int
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
        super().__init__()
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v_x = v_x
        self.v_y = v_y
        
        self.surface = None
        self.damage  = None
        
        self.is_alive = True
        self.rect = pg.rect.Rect(self.x, self.y, self.w, self.h)
        
        
    def update(self):
        """弾の更新処理
        """
        is_out_of_screen = self.rect.left < 0 or \
                            self.rect.right > CFG.screen_w or \
                            self.rect.top < 0 or \
                            self.rect.bottom >= CFG.screen_h
                            
        if is_out_of_screen:
            self.is_alive = False
    
    
    def blit(
        self, 
        screen: pg.Surface
    ) -> None:
        """弾の描画処理

        Parameters
        ----------
        screen : pg.Surface
            スクリーンのオブジェクト
        """
        
        screen.blit(self.surface, self.rect)