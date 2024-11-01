import pygame as pg
from ..player.player import Player

class UI(pg.sprite.Sprite):
    
    def __init__(self) -> None:
        self.font_status = pg.font.SysFont(None, 36)
    
    def update(self, player: Player):
        self.score_text = self.font_status.render(f'Score: {player.score}', True, pg.Color('WHITE'))
        self.lv_text = self.font_status.render(f'Lv: {player.level}', True, pg.Color('WHITE'))
        self.hp_text = self.font_status.render(f'HP: {player.hp}', True, pg.Color('WHITE'))
        self.mp_text = self.font_status.render(f'MP: {player.mp}', True, pg.Color('WHITE'))
        
    
    def blit(self, screen: pg.Surface) -> None:
        screen.blit(self.score_text, (10, 10 + 40 * 0))
        screen.blit(self.lv_text, (10, 10 + 40 * 1))
        screen.blit(self.hp_text, (10, 10 + 40 * 2))
        screen.blit(self.mp_text, (10, 10 + 40 * 3))