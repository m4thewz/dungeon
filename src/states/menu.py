import pygame as pg
from utils import *
from src.states.base import BaseState
from src.menu import Menu

# tela inicial do jogo
class MenuState (BaseState):
    def __init__(self, screen, main):
        self.screen = screen
        self.main = main
        self.title = pg.transform.scale(pg.image.load("assets/title.png").convert_alpha(), TITLE_RES)

        functions = [lambda: self.main.new_game(), lambda: 0, lambda: self.main.exit()]
        self.menu = Menu(["Novo Jogo", "Créditos", "Sair"], functions, (WIDTH / 2, HEIGHT / 2), 75, center=True)

    def get_event(self, event):
        self.menu.get_event(event)

    def draw(self):
        self.screen.blit(self.title, ((WIDTH - TITLE_RES[0]) / 2, 0.03 * HEIGHT))  # 3% da tela
        self.menu.draw(self.screen)
