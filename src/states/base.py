import pygame as pg


# estado base do jogo, unica função relevante é a change_state
class BaseState:
    def get_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def change_state(self, state):
        # muda o estado atual do jogo
        self.main.current_state = state
        if state == "game":
            # faz uma transição
            pg.mouse.set_visible(False)
            self.main.states["game"].transition_alpha = 255
            self.main.states["game"].transitioning = True
        else:
            pg.mouse.set_visible(True)
