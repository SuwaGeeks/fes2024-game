import pygame as pg
import math
from config import Config as CFG
from ..bullet.bullet import BulletBase

class BossBase(pg.sprite.Sprite):
    
    def __init__(self, w, h):
        """ボスを作成

        Parameters
        ----------
        x : Union[int, None]
            ボスの初期x座標. 指定しないと画面外からフェードイン
        y : Union[int, None]
            ボスの初期y座標. 指定しないと画面外からフェードイン
        w : int
            ボスの横幅
        h : int
            ボスの高さ
        """
        super().__init__()
        
        # とりあえず中心にリスポーン
        self.x = CFG.screen_w /2 - w/2
        self.y = 0
        self.w = w
        self.h = h
        self.step = 1
        
        self.is_moving = True
        self.is_alive  = True
        
        self.hp     = None
        self.hp_max = None
        self.score  = None
        
        self.rect = pg.rect.Rect(self.x, self.y, self.w, self.h)
        
    def update(
        self, 
        enemy_bullets: list[BulletBase],
        player_bullets: list[BulletBase],
    ) -> None:
        """雑魚敵の更新処理

        Parameters
        ----------
        enemy_bullets : list[BulletBase]
            敵が発射した弾のリスト
        player_bullets : list[BulletBase]
            プレイヤーが発射した弾のリスト
        """
        if self.is_moving:
            # 中心に移動する（攻撃は通らない）
            speed = 3
            dx = CFG.screen_w/2 - self.w/2 - self.rect.x
            dy = CFG.bottom_limit / 2 - self.rect.y
            norm = math.sqrt(dx**2 + dy**2)
            
            if norm > 5:
                self.rect.x += (dx / norm) * speed
                self.rect.y += (dy / norm) * speed
            else:
                # 移動が完了
                self.is_moving = False
                self.hp        = self.hp_max
        else:
            # 攻撃
            if self.step == 1:
                self._update_1(enemy_bullets, player_bullets)
            elif self.step == 2:
                self._update_2(enemy_bullets, player_bullets)
            elif self.step == 3:
                self._update_3(enemy_bullets, player_bullets)
                
            # 当たり判定
            for bullet in player_bullets:
                if self.rect.colliderect(bullet):
                    bullet.is_alive = False
                    self.hp -= bullet.damage
                    
                    # 撃破
                    if self.hp <= 0:
                        self.is_moving = True
                        pg.mixer.Sound("assets/sounds/e_break.mp3").play()
                        
                        if self.step == 3:
                            self.is_alive = False
                        else:
                            self.step += 1
            
    
    def blit(
            self, 
            screen: pg.Surface
        ) -> None:
        """ボスを画面を描画する

        Parameters
        ----------
        screen : pg.Surface
            スクリーンのオブジェクト
        """
        screen.blit(self.surface, self.rect)
        
        
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
        raise NotImplementedError
    
    
    def _update_2(
        self, 
        enemy_bullets: list[BulletBase],
        player_bullets: list[BulletBase],
    ) -> None:
        """ボスの更新処理(第2形態)
        オーバーライドして動作を実装
        
        Parameters
        ----------
        enemy_bullets : list[BulletBase]
            敵が発射した弾のリスト
        player_bullets : list[BulletBase]
            プレイヤーが発射した弾のリスト
        """
        raise NotImplementedError
    
    
    def _update_3(
        self, 
        enemy_bullets: list[BulletBase],
        player_bullets: list[BulletBase],
    ) -> None:
        """ボスの更新処理(第3形態)
        オーバーライドして動作を実装

        Parameters
        ----------
        enemy_bullets : list[BulletBase]
            敵が発射した弾のリスト
        player_bullets : list[BulletBase]
            プレイヤーが発射した弾のリスト
        """
        raise NotImplementedError