import pygame as pg
import random
from typing import Union
from config import Config as CFG
from ..bullet.bullet import BulletBase

class EnemyBase(pg.sprite.Sprite):
    
    def __init__(
        self,
        x: Union[int, None],
        y: Union[int, None],
        w: int,
        h: int
    ) -> None:
        """雑魚敵を作成

        Parameters
        ----------
        x : Union[int, None]
            雑魚敵の初期x座標. 指定しないと画面外からフェードイン
        y : Union[int, None]
            雑魚敵の初期y座標. 指定しないと画面外からフェードイン
        w : int
            雑魚敵の横幅
        h : int
            雑魚敵の高さ
        """
        super().__init__()
        
        # random_pos_to_spawn() で参照するため先に定義
        self.w, self.h = w, h
        
        if x is None or y is None:
            # 初期位置を画面外に設定
            self.x, self.y = self.random_pos_to_spawn()
        else:
            self.x, self.y = x, y
            
        self.rect = pg.rect.Rect(self.x, self.y, self.w, self.h)
        
        self.score   = None
        self.hp      = None
        self.surface = None
        
        
    def update(
        self, 
        enemy_bullets: list[BulletBase],
        player_bullets: list[BulletBase],
    ) -> int:
        """雑魚敵の更新処理

        Parameters
        ----------
        enemy_bullets : list[BulletBase]
            敵が発射した弾のリスト
        player_bullets : list[BulletBase]
            プレイヤーが発射した弾のリスト

        Returns
        -------
        int
            - 撃破: スコア
            - 消滅: -1
            - それ以外: 0
        """
        
        # プレイヤーに撃破された
        for bullet in player_bullets:
            if self.rect.colliderect(bullet):
                bullet.is_alive = False
                return self.score
            
        # 行動範囲外で消滅
        is_out_of_screen = self.rect.left < -CFG.spawn_area_width or \
                            self.rect.right > CFG.screen_w + CFG.spawn_area_width or \
                            self.rect.top < -CFG.spawn_area_width or \
                            self.rect.bottom >= CFG.screen_h + CFG.spawn_area_width
                            
        if is_out_of_screen:
            return -1
    
        return 0
    
    
    def blit(
            self, 
            screen: pg.Surface
        ) -> None:
        """雑魚敵を画面を描画する

        Parameters
        ----------
        screen : pg.Surface
            スクリーンのオブジェクト
        """
        
        screen.blit(self.surface, self.rect)
        
    
    def random_pos_to_spawn(self) -> tuple[int, int]:
        
        r = random.random()
        if r < 0.3:
            # 画面上でスポーン(30%)
            x = random.randint(0, int(CFG.screen_w - self.w))
            y = -CFG.spawn_area_width
        else:
            # 画面脇でスポーン(70%)
            x = -CFG.spawn_area_width if random.random() < 0.5 else (CFG.screen_w + CFG.spawn_area_width - self.w)
            y = random.randint(0, CFG.spawn_area_bottom)
        return x, y
    
    
    def _random_pos_to_move(self) -> tuple[int, int]:
        x = random.randint(0, int(CFG.screen_w - self.w))
        y = random.randint(0, int(CFG.spawn_area_bottom))
        return x, y
    
    
    def _random_pos_to_despawn(self) -> tuple[int, int]:
        x = -999 if self.rect.x < CFG.screen_w / 2 else 999
        y = self.rect.x
        return x, y