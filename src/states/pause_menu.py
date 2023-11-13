import pygame as pg
from utils import *
from src.states.base import BaseState

class PauseMenuState (BaseState):
    def __init__(self, screen, main):
        self.screen = screen
        self.main = main
        self.font = pg.font.Font(None, 52)
    
    def get_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.change_state("game")
    
    def draw(self):
        self.screen.blit(self.font.render("Jogo Pausado", True, (255, 255, 255)), (WIDTH // 2, HEIGHT //2))