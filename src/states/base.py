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