import pygame as pg


class BaseState:
    def get_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def change_state(self, state):
        self.main.current_state = state
        if state == "game":
            # transition
            pg.mouse.set_visible(False)
            self.main.states["game"].transition_alpha = 255
            self.main.states["game"].transitioning = True
        else:
            pg.mouse.set_visible(True)
