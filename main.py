import pygame as pg
import sys
from utils import *
from src.states.menu import MenuState
from src.states.pause_menu import PauseMenuState
from src.states.game import GameState
from src.states.game_over import GameOverState

# classe responsavel por inicializar o jogo
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        pg.display.set_caption('Mystery Rooms')
        self.clock = pg.time.Clock()
        # estados do jogo
        self.states = {
            "menu": MenuState(self.screen, self),
            "pause_menu": PauseMenuState(self.screen, self),
            "game": GameState(self.screen, self),
            "game_over": GameOverState(self.screen, self)
        }
        self.current_state = "menu"

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit()
            else:
                # passa o evento pro estado atual
                self.states[self.current_state].get_event(event)

    def update(self):
        # atualiza o estado atual
        self.states[self.current_state].update()
        self.clock.tick(60) #60 fps

    def draw(self):
        # desenha o estado atual
        self.screen.fill(BACKGROUND)
        self.states[self.current_state].draw()

    def new_game(self):
        # inicializa um novo jogo (apenas cria uma nova classe para a substituir na lista de estados)
        self.states["game"] = GameState(self.screen, self)
        self.current_state = "game"
        pg.mouse.set_visible(False)

    def exit(self): # fecha o jogo
        pg.quit()
        sys.exit()

    def run(self):
        # loop responsavel por ficar atualizando o jogo
        while True:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    Game().run()
