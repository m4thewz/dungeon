import pygame as pg
from utils import *
from src.states.base import BaseState
from src.menu import Menu

class MenuState (BaseState):
    def __init__(self, screen, main):
        self.screen = screen
        self.main = main
        self.title = pg.transform.scale(pg.image.load("assets/title.png").convert_alpha(), TITLE_RES)

        functions = [lambda: self.main.new_game(), lambda: self.change_state("credits"), lambda: self.main.exit()]
        self.menu = Menu(["New Game", "Credits", "Exit"], functions, (WIDTH / 2, HEIGHT / 2), 75, center=True)

    def get_event(self, event):
        self.menu.get_event(event)

    def draw(self):
        self.screen.blit(self.title, ((WIDTH - TITLE_RES[0]) / 2, 0.03 * HEIGHT))  # 3% of screen
        self.menu.draw(self.screen)
