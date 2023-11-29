import pygame as pg
from utils import *

# menu que exibe opções e um seletor
class Menu:
    def __init__(self, options: list | tuple, functions: list | tuple, pos: list | tuple, font_size: int = 30, gap: int = 5, center: bool = False):
        dot_size = font_size / 2
        self.dot = pg.transform.scale(pg.image.load("assets/menu_pointer.png").convert_alpha(), (0.568 * dot_size, dot_size))
        self.font = pg.font.Font("assets/Blockhead.otf", font_size)
        self.options = options
        self.functions = functions
        self.active_option = 0  # indice da opção atual
        self.gap = gap
        self.font_size = font_size
        if center:
            # verifica qual caracter tem mais caracteres e pega seu tamanho
            menu_width = self.font.size(max(self.options, key=len))[0] + self.dot.get_width() + 10
            # pega o centro (x) da tela pra ser exibido o menu
            self.pos = ((WIDTH - menu_width) / 2, pos[1])
            print(self.pos, pos)
        else:
            self.pos = pos

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and self.active_option > 0:
                self.active_option -= 1
            elif event.key == pg.K_DOWN and self.active_option < len(self.options) - 1:
                self.active_option += 1
            elif event.key in [pg.K_SPACE, pg.K_RETURN]:
                self.functions[self.active_option]()

    def draw(self, screen):
        start_x, start_y = self.pos
        for index, text in enumerate(self.options):
            text_render = self.font.render(text, True, COLOR)
            screen.blit(text_render, (start_x + self.dot.get_width() + 10, start_y + index * self.font_size + self.gap))

        screen.blit(self.dot, (start_x, start_y + self.font_size / 3 + self.active_option * self.font_size + self.gap))
