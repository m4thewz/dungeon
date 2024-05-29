import pygame as pg
from utils import *
from src.states.base import BaseState
from src.menu import Menu


class GameOverState (BaseState):
    def __init__(self, screen, main):
        self.screen = screen
        self.main = main
        self.font = pg.font.Font("assets/Blockhead.otf", 124)

        functions = [lambda: self.main.new_game(), lambda: self.main.exit()]
        self.menu = Menu(["New Game", "Exit"], functions, (WIDTH / 2, HEIGHT / 2), 75, center=True)

    def get_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.change_state("game")
        else:
            self.menu.get_event(event)

    def draw(self):
        title = self.font.render("Game Over", True, COLOR)
        self.screen.blit(title, ((WIDTH - title.get_width()) / 2, 0.03 * HEIGHT))
        self.menu.draw(self.screen)
