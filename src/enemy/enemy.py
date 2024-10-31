import pygame as pg
from config import Config as CFG

class EnemyBase(pg.sprite.Sprite):
    
    ttl = CFG.enemy_ttl
    
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int
    ) -> None:
        """雑魚敵を作成

        Parameters
        ----------
        x : int
            雑魚敵の初期x座標
        y : int
            雑魚敵の初期y座標
        w : int
            雑魚敵の横幅
        h : int
            雑魚敵の高さ
        """
        super().__init__()
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.rect.Rect(self.x, self.y, self.w, self.h)
        
        self.score   = None
        self.hp      = None
        self.surface = None
        
        
    def update(
            self, 
            bullets: list[pg.Surface]
        ) -> int:
        """雑魚敵の更新処理

        Parameters
        ----------
        bullets : : list[pg.Surface]
            自機が発射した弾のリスト

        Returns
        -------
        int
            - 撃破: スコア
            - 消滅: -1
            - それ以外: 0
        """
        
        # プレイヤーに撃破された
        is_hit = any([self.rect.colliderect(bullet) for bullet in bullets])
        if is_hit:
            return self.score
        
        
        # 画面外かタイムアウトで消滅
        self.ttl -= 1
        is_time_over = self.ttl < 0
        is_out_of_screen = self.rect.left < 0 or \
                            self.rect.right > CFG.screen_w or \
                            self.rect.top < 0 or \
                            self.rect.bottom >= CFG.screen_h
                            
        if is_time_over or is_out_of_screen:
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