import pygame as pg
from pygame.locals import *
import random
import math
from typing import Union
from src.bomb.bomb import Bomb
from src.player.player import Player
from src import enemy as Enemy
from src.bullet import BulletBase
from src.ui.ui import UI
from src.ui.title import Title
from src.ui.score_board import ScoreBoard

from src import boss

from config import Config as CFG
from .macro import *

class GameManager():
    """ゲーム全体を管理するクラス
    
    """
    
    def __init__(self, init_screen: bool = True) -> None:
        """ゲームマネージャーの作成

        Parameters
        ----------
        init_screen : bool
            windowの初期化を行うかどうか
        """
        
        if init_screen:
            pg.init()
            if CFG.use_gamepad:
                self.joystick = pg.joystick.Joystick(0)
                self.joystick.init()
            pg.display.set_caption("ぴゅんぴゅん2")

            if CFG.is_fullscreen:
                self.screen = pg.display.set_mode((CFG.screen_w, CFG.screen_h), FULLSCREEN)
            else:
                self.screen = pg.display.set_mode((CFG.screen_w, CFG.screen_h))
    
        self.player = Player(CFG.screen_w/2 - 48/2, CFG.screen_h*0.8, 48, 48)
        self.bomb = Bomb()
        
        self.step = STEP_TITLE
        self.is_step_up = False
        
        self.title = Title()
        self.ui = UI()
        self.score_board = None
        
        self.player_bullets: list[BulletBase] = []
        self.enemy_bullets: list[BulletBase] = []
        
        self.enemies: list[Enemy.EnemyBase] = []
        self.boss: Union[boss.BossBase, None] = None
        
        self.stage = 1
        self.pg_event = pg.event.get()
        
        # ボス出現までの時間
        self.enemy_cycle = 0
        self.sec_to_boss = [60, 60, 60, 60, 60]
    
    
    def update(self) -> None:
        """各コンポーネントの更新処理
        """
        
        self.pg_event = pg.event.get()
        
        if self.is_step_up:
            self.step += 1
            self.is_step_up = False
        
        if self.step == STEP_TITLE:
            self._update_title()
        elif self.step == STEP_PLAY:
            self._update_play()
        elif self.step == STEP_SCORE:
            self._update_score()
        
        
    
    def blit(self) -> None:
        """各コンポーネントの描画処理
        """
        if self.step == STEP_TITLE:
            self._blit_title()
        elif self.step == STEP_PLAY:
            self._blit_play()
        elif self.step == STEP_SCORE:
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
        
        if self.step == STEP_SCORE:
            if self.score_board.is_continue:
                self.__init__(init_screen=False)
        
        # windowの[x]ボタンで終了
        for event in self.pg_event:
            if event.type == pg.QUIT:
                pg.quit()
                return False
            
        # ゲームに割り当てられた終了ボタンで終了
        is_pressed_pad = False
        if CFG.use_gamepad:
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
        
        # プレイヤーの更新
        self.player.update(self.enemy_bullets ,self.player_bullets)
        
        if self.player.use_bomb():
            self.bomb.bomb(self.player)
        self.bomb.update(self.enemies, self.boss)
        
        # 弾の更新
        for bullet in self.player_bullets:
            bullet.update()
        for bullet in self.enemy_bullets:
            bullet.update()
                
        if self.boss is None:
            # 雑魚敵フェーズ
            
            # 適当に敵をすぽーんさせる
            if self.enemy_cycle < sum(self.sec_to_boss[:self.stage]) * CFG.fps:
                # 雑魚敵と遊ぶ時間は雑魚敵を発生させる
                self.enemy_cycle += 1
                r = random.random()
                is_spawn = random.random() <= (math.sqrt(self.player.level) / CFG.fps)
                if self.stage == 1 and is_spawn:
                    if  r <= 0.4:
                        self.enemies.append(Enemy.EnemyB1())
                    elif r <= 0.8:
                        self.enemies.append(Enemy.EnemyR2())
                    elif r <= 1.0:
                        self.enemies.append(Enemy.EnemyY3())

                if self.stage == 2 and is_spawn:
                    if  r <= 0.4:
                        self.enemies.append(Enemy.EnemyY2())
                    elif r <= 0.8:
                        self.enemies.append(Enemy.EnemyR1())
                    elif r <= 1.0:
                        self.enemies.append(Enemy.EnemyG2())

                if self.stage == 3 and is_spawn:
                    if  r <= 0.4:
                        self.enemies.append(Enemy.EnemyB2())
                    elif r <= 0.8:
                        self.enemies.append(Enemy.EnemyG1())
                    elif r <= 1.0:
                        self.enemies.append(Enemy.EnemyR3())

                if self.stage == 4 and is_spawn:
                    if  r <= 0.4:
                        self.enemies.append(Enemy.EnemyY1())
                    elif r <= 0.8:
                        self.enemies.append(Enemy.EnemyG2())
                    elif r <= 1.0:
                        self.enemies.append(Enemy.EnemyB3())

                if self.stage == 5 and is_spawn:
                    if  r <= 0.4:
                        self.enemies.append(Enemy.EnemyR2())
                    elif r <= 0.8:
                        self.enemies.append(Enemy.EnemyB2())
                    elif r <= 1.0:
                        self.enemies.append(Enemy.EnemyG3())
                    
            else:
                # 雑魚敵を撤退させる
                for enemy in self.enemies:
                    enemy.ttl = 0
        
        
            # 雑魚敵の更新
            enemy_rets = [enemy.update(self.enemy_bullets, self.player_bullets) for enemy in self.enemies]
            is_alive = [x == 0 for x in enemy_rets]
            self.enemies = [enemy for enemy, flag in zip(self.enemies, is_alive) if flag]
            self.player.score += sum([max(x, 0) for x in enemy_rets])
            
            # ボスの発生条件を満たして雑魚敵が撤退すればボスを生成
            if len(self.enemies) == 0 and self.enemy_cycle == sum(self.sec_to_boss[:self.stage]) * CFG.fps:
                if self.stage == 1:
                    self.boss = boss.Boss1()
                elif self.stage == 2:
                    self.boss = boss.Boss2()
                elif self.stage == 3:
                    self.boss = boss.Boss3()
                elif self.stage == 4:
                    self.boss = boss.Boss4()
                elif self.stage == 5:
                    self.boss = boss.Boss5()
            
        else:
            # ボス戦
            self.boss.update(self.enemy_bullets, self.player_bullets, self.player)
            # ボス撃破
            if not self.boss.is_alive:
                self.player.score += self.boss.score
                self.boss = None
                self.player.hp = min(5, self.player.hp+1)
                self.stage += 1
        
        # 画面外またはヒットした弾を削除
        is_alive = [bullet.is_alive for bullet in self.player_bullets]
        self.player_bullets = [bullet for bullet, flag in zip(self.player_bullets, is_alive) if flag]
        
        is_alive = [bullet.is_alive for bullet in self.enemy_bullets]
        self.enemy_bullets = [bullet for bullet, flag in zip(self.enemy_bullets, is_alive) if flag]
        
        # UIの更新
        self.ui.update(self.player, boss=self.boss)
        
        # クリア/ゲームオーバー処理
        if self.stage > 5 or self.player.hp == 0:
            
            score = self.player.score
            is_clear = self.player.hp > 0
            
            self.score_board = ScoreBoard(score, is_clear)
            self.is_step_up = True
    
    
    def _update_score(self):
        self.score_board.update(self.pg_event)
    
    
    def _blit_title(self):
        self.screen.fill(pg.Color("BLACK")) 
        self.title.blit(self.screen)
    
    
    def _blit_play(self):
        
        self.screen.fill(pg.Color("BLACK")) 
        
        
        for bullet in self.player_bullets:
            bullet.blit(self.screen)
        for bullet in self.enemy_bullets:
            bullet.blit(self.screen)
        
        for enemy in self.enemies:
            enemy.blit(self.screen)
            
        if self.boss is not None:
            self.boss.blit(self.screen)
            
        self.bomb.blit(self.screen)
            
        self.player.blit(self.screen)
        
        self.ui.blit(self.screen)
        
    
    def _blit_score(self):
        self.screen.fill(pg.Color("BLACK")) 
        self.score_board.blit(self.screen)