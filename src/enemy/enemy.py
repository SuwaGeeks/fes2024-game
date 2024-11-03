import pygame as pg
import random
import math
from typing import Union
from config import Config as CFG
from ..bullet.bullet import bullet as BulletBase

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
        
        
        self.ttl = CFG.enemy_ttl
        self.dist_x, self.dist_y = self._random_pos_to_move()
        
        self.score   = None
        self.hp      = None
        self.speed   = None
        
        self.rect = pg.rect.Rect(self.x, self.y, self.w, self.h)
    
        # アニメーションのリスト
        self.surfaces:list[pg.Surface] = []

        self.anime_cycle = 0
    
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
        
        self.anime_cycle += 1
        self.ttl -= 1
        
        # 移動処理
        # - (dist_x, dist_y) に speed で進む
        # - 到達すれば新しい (dist_x, dist_y) を設定
        x = self.dist_x - self.rect.x
        y = self.dist_y - self.rect.y
        norm = math.sqrt(x**2 + y**2)
        
        if norm > 5:
            self.rect.x += (x / norm) * self.speed
            self.rect.y += (y / norm) * self.speed
        else:
            self.dist_x, self.dist_y = self._random_pos_to_move()
            
            
        # タイムオーバの敵は画面外にフェードアウト
        if self.ttl < 0:
            self.dist_x, self.dist_y = self._random_pos_to_despawn() 
        
        # プレイヤーに撃破された
        for bullet in player_bullets:
            
            if self.rect.colliderect(bullet):
                self.hp -= bullet.damage
                bullet.is_alive = False
                
        if self.hp <= 0:
            pg.mixer.Sound("assets/sounds/e_break.mp3").play()
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
        x = CFG.fps / 2
        y = self.anime_cycle % x
        if y <= x / 2:
           screen.blit(self.surfaces[0],self.rect)
        else:
            screen.blit(self.surfaces[1],self.rect)
        
    
    def random_pos_to_spawn(self) -> tuple[int, int]:
        """スポーン領域の座標を生成

        Returns
        -------
        tuple[int, int]
            スポーン領域の座標 `(x, y)`
        """
        
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
        """移動領域の座標を生成

        Returns
        -------
        tuple[int, int]
            移動領域の座標 `(x, y)`
        """
        x = random.randint(0, int(CFG.screen_w - self.w))
        y = random.randint(0, int(CFG.spawn_area_bottom))
        return x, y
    
    
    def _random_pos_to_despawn(self) -> tuple[int, int]:
        """デスポーン領域の座標を生成

        Returns
        -------
        tuple[int, int]
            デスポーン領域の座標 `(x, y)`
        """
        x = -999 if self.rect.x < CFG.screen_w / 2 else 999
        y = self.rect.x
        return x, y