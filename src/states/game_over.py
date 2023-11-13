import pygame as pg
from src.states.base import BaseState

class GameOverState (BaseState):
    def __init__(self, screen, main):
        self.screen = screen