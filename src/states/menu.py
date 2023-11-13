import pygame as pg
from src.states.base import BaseState

class MenuState (BaseState):
    def __init__(self, screen, main):
        self.screen = screen