from src.states.base import BaseState
from utils import *
import pygame as pg
credits = """
Dev: Matheus Vitor
Designers: Matheus Vitor and Maria Rita

Inspiration game: The Binding of Isaac
Inspiration map: @0x72 (itch.io)
Inspiration character: @penzilla (itch.io)
Gun by @vladpenn (itch.io)
Life bar by @adwitr (itch.io)

"""


class CreditState (BaseState):
    def __init__(self, screen, main):
        self.screen = screen
        self.main = main

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.change_state("menu")

    def draw(self):
        font = pg.font.Font(None, 36)
        lines = credits.strip().split('\n')

        for i, line in enumerate(lines):
            text = font.render(line, True, COLOR)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, 100 + i * 40))
            self.screen.blit(text, text_rect)
