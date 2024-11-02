import pygame as pg
import math
import random
from config import Config as CFG
from ..Bullet.bullet import BulletBase

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
        
        self.hp     = 0
        self.hp_max = None
        self.score  = None
        self.speeds = []
        
        self.dist_x, self.dist_y = self._random_pos_to_move()
        
        self.rings_r = [0, 0, 0]
        
        self.rect = pg.rect.Rect(self.x, self.y, self.w, self.h)
        
        # アニメーションのリスト
        self.surfaces:list[pg.Surface] = []
        self.anime_cycle = 0


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
        self.anime_cycle += 1
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
                # リングをふくらませる
                self.rings_r[self.step-1] += 1
                if self.rings_r[self.step-1] >= self.w * (1.1 ** self.step):
                    # リングが膨らみきれば攻撃フェーズへ
                    self.is_moving = False
                    self.hp        = self.hp_max
        else:
            
            # 移動
            x = self.dist_x - self.rect.x
            y = self.dist_y - self.rect.y
            norm = math.sqrt(x**2 + y**2)
            
            if norm > 5:
                self.rect.x += (x / norm) * self.speeds[self.step-1]
                self.rect.y += (y / norm) * self.speeds[self.step-1]
            else:
                self.dist_x, self.dist_y = self._random_pos_to_move()
            
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
        # リングの描画
        for r in self.rings_r:
            pg.draw.circle(screen, '#00bfff', self.rect.center, r, 2)
        # screen.blit(self.surface, self.rect)
        
        x = CFG.fps / 2
        y = self.anime_cycle % x
        if y <= x / 2:
           screen.blit(self.surfaces[0],self.rect)
        else:
            screen.blit(self.surfaces[1],self.rect)
        
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
    
    
    def _random_pos_to_move(self) -> tuple[int, int]:
        """移動領域の座標を生成

        Returns
        -------
        tuple[int, int]
            移動領域の座標 `(x, y)`
        """
        x = random.randint(0, int(CFG.screen_w - self.w))
        y = random.randint(0, int(CFG.screen_h / 4))
        return x, y