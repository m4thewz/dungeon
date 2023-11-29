from src.states.base import BaseState
from utils import *
import pygame as pg
credits = """
Programador: Matheus Vitor
Designers: Matheus Vitor e Maria Rita

Inspiração de jogo: The Binding of Isaac
Inspiração mapa: @0x72 (itch.io)
Inspiração personagem: @penzilla (itch.io)
Arma por @vladpenn (itch.io)
Barra de vida por @adwitr (itch.io)


Agradecimentos especiais a Sostenes Pereira e Eduardo Marmo, dois professores incríveis.
"""


# tela para os créditos
class CreditState (BaseState):
    def __init__(self, screen, main):
        self.screen = screen
        self.main = main

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.change_state("menu")

    def draw(self):
        font = pg.font.Font(None, 36)
        # divide cada linha e a desenha
        lines = credits.strip().split('\n')
        for i, line in enumerate(lines):
            text = font.render(line, True, COLOR)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, 100 + i * 40))
            self.screen.blit(text, text_rect)
