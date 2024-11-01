import pygame as pg

from src.manager import GameManager
from config import Config as CFG

if __name__ == '__main__':
    
    
    game_manager = GameManager(CFG.screen_w, CFG.screen_h)
    
    while game_manager.is_continue():
        game_manager.update()
        game_manager.blit()
        game_manager.delay()