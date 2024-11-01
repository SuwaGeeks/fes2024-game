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
        
        self.shot_cycle = 0
        self.god_time   = 0
        
        self.score = 0
        self.level = CFG.player_default_level
        self.hp    = CFG.player_default_hp
        self.mp    = CFG.player_default_mp
        
        self.surface = pg.image.load('assets/player/player1.png')
        self.surface = pg.transform.scale(self.surface, (self.w, self.h))
        self.rect    = pg.rect.Rect(self.x, self.y, self.w, self.h)
        
        
    def update(
        self, 
        enemy_bullets: list[BulletBase],
        player_bullets: list[BulletBase],
    ) -> None:
        """プレイヤーの更新処理

        Parameters
        ----------
        enemy_bullets : list[BulletBase]
            敵が発射した弾のリスト
        player_bullets : list[BulletBase]
            プレイヤーが発射した弾のリスト
        """
         
        # 各カウンタを進める
        if self.shot_cycle > 0:
            self.shot_cycle -= 1
        
        if self.god_time > 0:
            self.god_time -= 1
        
        
        key = pg.key.get_pressed()
        joy = pg.joystick.Joystick(0)
        
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
            
        self.rect.y += joy.get_axis(1) * CFG.player_speed
        self.rect.x += joy.get_axis(0) * CFG.player_speed
            
        # 画面外に出ないように
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > CFG.screen_w:
            self.rect.right = CFG.screen_w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom >= CFG.screen_h:
            self.rect.bottom = CFG.screen_h
        
        # 弾の発射処理 
        if self.shot_cycle == 0 and (key[CFG.key_map['shot']] or joy.get_button(CFG.pad_map['shot'])):
            self._shot(player_bullets)
            self.shot_cycle = CFG.player_shot_cycle
            
        # 当たり判定
        for bullet in enemy_bullets:
            
            x_p, y_p = self.rect.center
            
            # 理不尽さ回避のため自機の当たり判定は中心 1px のみ
            # if bullet.rect.collidepoint(x_p, y_p) and self.god_time == 0:
            if bullet.rect.colliderect(self.rect) and self.god_time == 0:
                self.hp -= 1
                self.god_time = CFG.player_god_time
                
    
    
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
        if self.god_time > 0:
            # 無敵時間はチカチカさせる
            blink_per_sec = 4
            if self.god_time % (CFG.fps/blink_per_sec)  < CFG.fps/blink_per_sec/2:
                screen.blit(self.surface, self.rect)
        else:
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