import pygame as pg

from src.manager import GameManager
from config import Config as CFG

if __name__ == '__main__':
    
    
    app = GameManager()
    
    while app.is_continue():
        app.update()
        app.blit()
        app.delay()