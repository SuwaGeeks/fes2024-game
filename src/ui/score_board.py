import os
import csv
import pygame as pg
from pathlib import Path
from config import Config as CFG

class ScoreBoard(pg.sprite.Sprite):
    
    def __init__(
            self, 
            score: int, 
            is_clear: bool
        ) -> None:
        super().__init__()
        
        self.font_size = 36
        self.font = pg.font.SysFont(None, self.font_size)
        
        self.x_rank = 55
        self.x_score = 150
        self.x_name = 300
        self.x_is_clear = 470
        
        self.score = score
        self.is_clear = is_clear
        self.has_name = False
        self.name = ""
        
        self.n_tops = 18
        self.top_scores  = None
        
        
    def update(self, event):
        
        # 名前の入力
        if not self.has_name:
            for e in event:
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_BACKSPACE:
                        # BackSpace
                        self.name = self.name[:-1]
                    elif e.key == pg.K_RETURN:
                        # Enter
                        self.has_name = True
                        self.top_scores = self._init_top_score()
                    elif len(self.name) < CFG.user_name_max_len:
                        self.name += e.unicode
            
            
    
    
    def blit(self, screen: pg.Surface) -> None:
        """UIの描画処理

        Parameters
        ----------
        screen : pg.Surface
            スクリーンオブジェクト
        """
        if not self.has_name:
            
            
            instruction_surface = self.font.render('Clear!!' if self.is_clear else 'Game over...', True, 'WHITE')
            screen.blit(instruction_surface, (50, 100))
            text_surface = self.font.render(self.name, True, 'WHITE')
            pg.draw.line(screen, '#FFFFFF', (50, 230), (300, 230), width=2)
            screen.blit(text_surface, (50, 200))
            instruction_surface = self.font.render('Type your name and press enter to coutiune.', True, 'WHITE')
            screen.blit(instruction_surface, (50, 300))
        else:
            margin_top = 100
            margin_x = 50
            
            # ヘッダ
            text_rank     = self.font.render(f'Rank', True, pg.Color('WHITE'))
            text_score    = self.font.render(f'Score', True, pg.Color('WHITE'))
            text_name     = self.font.render(f'Name', True, pg.Color('WHITE'))
            text_is_clear = self.font.render(f'Clear', True, pg.Color('WHITE'))
            # text_datetime = self.font.render(f'Datetime', True, pg.Color('WHITE'))

            screen.blit(text_rank, (self.x_rank, margin_top - self.font_size))
            screen.blit(text_score, (self.x_score, margin_top - self.font_size))
            screen.blit(text_name, (self.x_name, margin_top - self.font_size))
            screen.blit(text_is_clear, (self.x_is_clear, margin_top - self.font_size))
            
            for idx, (score, timestamp, name, is_clear) in enumerate(self.top_scores):
                
                line_start = (margin_x, self.font_size*idx+margin_top-10)
                line_end = (CFG.screen_w-margin_x, self.font_size*idx+margin_top-10)
                
                pg.draw.line(screen, '#FFFFFF', line_start, line_end, width=2)
                
                text_rank     = self.font.render(f'#{int(idx+1):02d}', True, pg.Color('WHITE'))
                text_score    = self.font.render(f'{int(score):12d}', True, pg.Color('WHITE'))
                text_name     = self.font.render(f'{name}', True, pg.Color('WHITE'))
                text_is_clear = self.font.render('o' if is_clear=='True' else 'x', True, pg.Color('WHITE'))
                
                y_texts = self.font_size*idx+margin_top
                screen.blit(text_rank, (self.x_rank, y_texts))
                screen.blit(text_score, (self.x_score, y_texts))
                screen.blit(text_name, (self.x_name, y_texts))
                screen.blit(text_is_clear, (self.x_is_clear, y_texts))
                
        
    def _init_top_score(self):
        
        top_scores  = None
        
        if CFG.use_server:
            # TODO: サーバとの通信の実装
            pass
        
        if self.top_scores is None:
            
            timestamp = 0
            
            # ファイルが存在しない場合は作成する
            self.csv_path = Path(CFG.csv_path)
            if not self.csv_path.exists():
                self.csv_path.touch()
                
            # 追記
            with open(self.csv_path, 'a') as f:
                writer = csv.writer(f)
                writer.writerow([self.score, timestamp, self.name, self.is_clear]) 
                
            # スコアを追加して読み取る
            with open(self.csv_path) as f:
                reader = csv.reader(f)
                scores = [row for row in reader]
                    
            
            top_scores = scores[: min(len(scores), self.n_tops)]
            
        return sorted(top_scores, reverse=True)