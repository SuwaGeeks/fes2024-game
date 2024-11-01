import pygame as pg
import random
from src.player.player import Player
from src.enemy.enemy_b1 import EnemyB1
from src.enemy.enemy import EnemyBase
from src.bullet.bullet import BulletBase
from src.ui.ui import UI
from src.ui.title import Title

from config import Config as CFG
from .macro import *

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
        self.joystick = pg.joystick.Joystick(0)
        self.joystick.init()
        pg.display.set_caption("ぴゅんぴゅん2")

        self.screen = pg.display.set_mode((screen_w, screen_h))
    
        self.player = Player(screen_w/2 - 48/2, screen_h*0.8, 48, 48)
        
        self.step = STEP_TITLE
        self.is_step_up = False
        
        self.title = Title()
        self.ui = UI()
        
        self.player_bullets: list[BulletBase] = []
        self.enemy_bullets: list[BulletBase] = []
        self.enemies: list[EnemyBase] = []
        self.boss = None
    
    
    def update(self) -> None:
        """各コンポーネントの更新処理
        """
        
        if self.is_step_up:
            self.step += 1
            self.is_step_up = False
        
        if self.step == STEP_TITLE:
            self._update_title()
        elif self.step == STEP_PLAY:
            self._update_play()
        elif self.step == STEP_TITLE:
            self._update_score()
        
        
    
    def blit(self) -> None:
        """各コンポーネントの描画処理
        """
        if self.step == STEP_TITLE:
            self._blit_title()
        elif self.step == STEP_PLAY:
            self._blit_play()
        elif self.step == STEP_TITLE:
            self._blit_score()
        
        pg.display.flip()
        
    
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
        is_pressed_pad = self.joystick.get_button(CFG.pad_map['exit'])
        is_pressed_key = pg.key.get_pressed()[CFG.key_map['exit']]
        if is_pressed_key or is_pressed_pad:
            pg.quit()
            return False
            
        return True
    
    
    def _update_title(self):
        self.title.update()
        self.is_step_up = self.title.is_continue
    
    def _update_play(self):
                # 適当な敵のスポーン
        if random.random() > 0.995:
            x = random.randint(0, CFG.screen_h / 2)
            y = random.randint(0, CFG.screen_w - 48)
            self.enemies.append(EnemyB1(x, y))
            
        
        # プレイヤーの更新
        self.player.update(self.enemy_bullets ,self.player_bullets)
        
        # 弾の更新
        for bullet in self.player_bullets:
            bullet.update()
        for bullet in self.enemy_bullets:
            bullet.update()
    
        # 雑魚敵の更新
        enemy_rets = [enemy.update(self.enemy_bullets, self.player_bullets) for enemy in self.enemies]
        is_alive = [x == 0 for x in enemy_rets]
        self.enemies = [enemy for enemy, flag in zip(self.enemies, is_alive) if flag]
        self.player.score += sum([max(x, 0) for x in enemy_rets])
        
        # 画面外またはヒットした弾を削除
        is_alive = [bullet.is_alive for bullet in self.player_bullets]
        self.player_bullets = [bullet for bullet, flag in zip(self.player_bullets, is_alive) if flag]
        
        is_alive = [bullet.is_alive for bullet in self.enemy_bullets]
        self.enemy_bullets = [bullet for bullet, flag in zip(self.enemy_bullets, is_alive) if flag]
        
        # UIの更新
        self.ui.update(self.player)
    
    
    def _update_score(self):
        pass
    
    
    def _blit_title(self):
        self.title.blit(self.screen)
    
    
    def _blit_play(self):
        
        self.screen.fill(pg.Color("BLACK")) 
        
        for bullet in self.player_bullets:
            bullet.blit(self.screen)
        for bullet in self.enemy_bullets:
            bullet.blit(self.screen)
        
        for enemy in self.enemies:
            enemy.blit(self.screen)
            
        self.player.blit(self.screen)
        
        self.ui.blit(self.screen)
        
    
    def _blit_score(self):
        pass