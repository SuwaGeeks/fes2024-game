import pygame as pg
from config import Config as CFG
from ..bullet.bullet import BulletBase
from ..bullet.bullet_p1 import BulletP1

class Player(pg.sprite.Sprite):

    
    def __init__(
            self,
            x: int = int(CFG.screen_w / 2 - 48 / 2),
            y: int = int(CFG.screen_h * 0.8), 
            w: int = 48, 
            h: int = 48, 
        ):
        """プレイヤーを作成

        Parameters
        ----------
        x : int
            プレイヤーの初期x座標
        y : int
            プレイヤーの初期x座標
        w : int
            プレイヤーの幅[px]
        h : int
            プレイヤーの高さ[px]
        """
        super().__init__()
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.shot_cycle = CFG.player_shot_cycle
        
        self.level = CFG.player_default_level
        self.hp = CFG.player_default_hp
        self.mp = CFG.player_default_mp
        
        self.surface = pg.image.load('assets/player/player1.png')
        self.surface = pg.transform.scale(self.surface, (self.w, self.h))
        self.rect    = pg.rect.Rect(self.x, self.y, self.w, self.h)
        
        
    def update(self, bullet_list: list[BulletBase]) -> None:
        """プレイヤーの更新処理
        """
         
        if self.shot_cycle > 0:
            self.shot_cycle -= 1
        
        key = pg.key.get_pressed()
        
        # 弾の発射処理 
        if self.shot_cycle == 0 and key[CFG.key_map['shot']]:
            self._shot(bullet_list)
            self.shot_cycle = CFG.player_shot_cycle
        
        # 移動処理
        # TODO: 斜め移動のスピード調整
        if key[CFG.key_map['up']]:
            self.rect.y -= CFG.player_speed
        if key[CFG.key_map['down']]:
            self.rect.y += CFG.player_speed
        if key[CFG.key_map['right']]:
            self.rect.x += CFG.player_speed
        if key[CFG.key_map['left']]:
            self.rect.x -= CFG.player_speed
            
        # 画面外に出ないように
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > CFG.screen_w:
            self.rect.right = CFG.screen_w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom >= CFG.screen_h:
            self.rect.bottom = CFG.screen_h
        
    
    
    def blit(
            self, 
            screen: pg.Surface
        ) -> None:
        """Playerを画面を描画する

        Parameters
        ----------
        screen : pg.Surface
            スクリーンのオブジェクト
        """
        screen.blit(self.surface, self.rect)
        
        
    def _shot(self, bullet_list: list[BulletBase]) -> None:
        """プレイヤーの射出
        レベルによって弾の種類が変化するのでメソッドにした

        Parameters
        ----------
        bullet_list : list[BulletBase]
            プレイヤーの排出した弾のリスト
        """
        
        player_center = self.rect.center[0]
        
        if self.level > 0:
            bullet_list.append(BulletP1(player_center, self.rect.top, 0, -20))