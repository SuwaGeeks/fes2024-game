import pygame as pg
from ..player.player import Player
from config import Config as CFG

from typing import Union

class UI(pg.sprite.Sprite):
    
    def __init__(self) -> None:
        """プレイ中のUIを作成
        """
        
        self.font_size = CFG.ui_frame_bottom_width / 3
        self.row1 = CFG.bottom_limit
        self.row2 = self.row1 + CFG.ui_frame_bottom_width / 3
        self.row3 = self.row2 + CFG.ui_frame_bottom_width / 3
        
        self.font_status = pg.font.SysFont(None, 36)
        
        self.HP_surface = pg.image.load('assets/ui/life.png')
        self.MP_surface = pg.image.load('assets/ui/bomb.png')
        
        # アイコンサイズをフォントサイズと揃える
        self.HP_surface = pg.transform.scale(self.HP_surface, (self.font_size, self.font_size))
        self.MP_surface = pg.transform.scale(self.MP_surface, (self.font_size, self.font_size))
        
        # Lv, HP, MP の文字
        self.lv_text = self.font_status.render('Lv', True, pg.Color('BLACK'))
        self.hp_text = self.font_status.render('HP', True, pg.Color('BLACK'))
        self.mp_text = self.font_status.render('MP', True, pg.Color('BLACK'))
        
        # 1p/2p のステータス
        self.hp_1p, self.hp_2p = None, None
        self.mp_1p, self.mp_2p = None, None
        self.lv_1p, self.lv_2p = None, None
        
    
    def update(
        self, 
        player_1: Player,
        player_2: Union[Player, None] = None
    ) -> None:
        """プレイ中のUIを更新

        Parameters
        ----------
        player_1 : Player
            1P のインスタンス
        player_2 : Union[Player | None], optional
            2P のインスタンス, by default None
        """
        self.score_text_1p = self.font_status.render(f'SCORE: {player_1.score}', True, pg.Color('WHITE'))
        self.hp_1p = max(0, player_1.hp)
        self.mp_1p = max(0, player_1.mp)
        self.lv_1p = max(0, player_1.level)
        
        if player_2 is not None:
            self.score_text_2p = self.font_status.render(f'{player_1.score}', True, pg.Color('WHITE'))
            self.hp_2p = max(0, player_2.hp)
            self.mp_2p = max(0, player_2.mp)
            self.lv_2p = max(0, player_2.level)
        
        
    
    def blit(self, screen: pg.Surface) -> None:
        """UIの描画処理

        Parameters
        ----------
        screen : pg.Surface
            スクリーンオブジェクト
        """
        
        # フレーム
        pg.draw.rect(screen, '#d3d3d3', (0, 0, CFG.screen_w, CFG.screen_h), CFG.ui_frame_width)
        pg.draw.rect(screen, '#d3d3d3', (0, CFG.screen_h - CFG.ui_frame_bottom_width, CFG.screen_w, CFG.screen_h))
        
        # ステータス(1P)
        x_start = 20
        
        screen.blit(self.score_text_1p, (CFG.left_limit+5, CFG.top_limit+5))
        # HP
        screen.blit(self.hp_text, (x_start, self.row1 + 5))
        for i in range(self.hp_1p):
            screen.blit(self.HP_surface, (self.font_size * (i+2), self.row1))
        # MP
        screen.blit(self.mp_text, (x_start, self.row2 + 5))
        for i in range(self.mp_1p):
            screen.blit(self.MP_surface, (self.font_size * (i+2), self.row2))
        # レベル
        screen.blit(self.lv_text, (x_start, self.row3 + 5))
        for i in range(self.lv_1p):
            screen.blit(self.Lv_surface, (self.font_size * (i+2), self.row3))
            
        # ステータス(2P)
        if self.hp_2p is not None:
            x_start = CFG.screen_w - self.font_size - 20
            screen.blit(self.score_text_2p, (CFG.right_limit - self.score_text_2p.get_width() - CFG.ui_frame_width, CFG.top_limit+5))
            
            # HP
            screen.blit(self.hp_text, (x_start, self.row1 + 5))
            for i in range(self.hp_2p):
                screen.blit(self.HP_surface, (x_start - self.font_size * (i+2), self.row1))
            # MP
            screen.blit(self.mp_text, (x_start, self.row2 + 5))
            for i in range(self.mp_2p):
                screen.blit(self.MP_surface, (x_start - self.font_size * (i+2), self.row2))
            # レベル
            screen.blit(self.lv_text, (x_start, self.row3 + 5))
            for i in range(self.lv_2p):
                screen.blit(self.Lv_surface, (x_start - self.font_size * (i+2), self.row3))