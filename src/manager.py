import pygame as pg
from src.player.player import Player
from src.enemy.enemy_b1 import EnemyB1
from src.enemy.enemy import EnemyBase
from src.bullet.bullet import BulletBase

from config import Config as CFG

class GameManager():
    """ゲーム全体を管理するクラス
    
    """
    
    def __init__(self, screen_w: int, screen_h: int) -> None:
        """ゲームマネージャーの作成

        Parameters
        ----------
        screen_w : int
            windowの横解像度
        screen_h : int
            windowの縦解像度
        """
        pg.init()
        self.screen = pg.display.set_mode((screen_w, screen_h))
        
        self.ui = None
        self.player = Player(screen_w/2 - 48/2, screen_h*0.8, 48, 48)
        
        self.score = 0
        self.player_bullets: list[BulletBase] = []
        self.enemy_bullets: list[BulletBase] = []
        self.enemies: list[EnemyBase] = []
        self.boss = None
        
        self.enemies.append(EnemyB1(100, 100))
    
    
    def update(self) -> None:
        """各コンポーネントの更新処理
        """
        
        # プレイヤーの更新
        self.player.update(self.player_bullets)
        
        # 弾の更新
        for bullet in self.player_bullets:
            bullet.update()
        for bullet in self.enemy_bullets:
            bullet.update()
        
        # 画面外またはヒットした弾を削除
        is_alive = [bullet.is_alive for bullet in self.player_bullets]
        self.player_bullets = [bullet for bullet, flag in zip(self.player_bullets, is_alive) if flag]
        
        # 雑魚敵の更新
        enemy_rets = [enemy.update(self.player_bullets) for enemy in self.enemies]
        is_alive = [x == 0 for x in enemy_rets]
        self.enemies = [enemy for enemy, flag in zip(self.enemies, is_alive) if flag]
        self.score += sum([max(x, 0) for x in enemy_rets])
        
        pg.display.update()
        
    
    def blit(self) -> None:
        """各コンポーネントの描画処理
        """
        self.screen.fill(pg.Color("BLACK")) 
        
        for bullet in self.player_bullets:
            bullet.blit(self.screen)
        for bullet in self.enemy_bullets:
            bullet.blit(self.screen)
        
        for enemy in self.enemies:
            enemy.blit(self.screen)
            
        self.player.blit(self.screen)
        
    
    def delay(self) -> None:
        """描画待ち処理
        """
        pg.time.Clock().tick(60)
    
    
    def is_continue(self) -> bool:
        """ゲームが終了するか

        Returns
        -------
        bool
            ゲームの続行フラグ
        """
        
        # windowの[x]ボタンで終了
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return False
            
        # ゲームに割り当てられた終了ボタンで終了
        key = pg.key.get_pressed()
        if key[CFG.key_map['exit']]:
            pg.quit()
            return False
            
        return True