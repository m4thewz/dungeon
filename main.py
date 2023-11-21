import pygame as pg
import sys
from utils import *
from src.states.menu import MenuState
from src.states.pause_menu import PauseMenuState
from src.states.game import GameState
from src.states.game_over import GameOverState


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
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
                self.states[self.current_state].get_event(event)

    def update(self):
        pg.display.set_caption(f'Dungeon Invader - {self.clock.get_fps() :.1f} FPS')
        self.states[self.current_state].update()
        self.clock.tick(60)

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.states[self.current_state].draw()

    def new_game(self):
        self.states["game"] = GameState(self.screen, self)
        self.current_state = "game"
        pg.mouse.set_visible(False)

    def exit(self):
        pg.quit()
        sys.exit()

    def run(self):
        while True:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    Game().run()
