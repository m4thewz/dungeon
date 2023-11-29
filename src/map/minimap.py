import pygame as pg
from utils import *


class Minimap:
    room_width, room_height = room_dimensions = MINIMAP_ROOM_SIZE # tamanho de cada sala
    color = (173, 173, 173) # cor do minimapa

    def __init__(self):
        # sala atual e sua posição
        self.current_room = None
        self.current_x, self.current_y = None, None
        self.rooms = [] # total de salas
        self.visited_rooms = [] # salas q ja foram visitadas

    def visit_room(self, room): # se ainda nao foi visitada, adiciona na lista de salas visitadas
        if [room.x, room.y] not in self.visited_rooms:
            self.visited_rooms.append([room.x, room.y])

    def set_current_room(self, room): # atualiza a sala atual
        self.visit_room(room)
        if self.current_room is not room:
            self.current_room = room

    def draw(self, surface): # desenha todas as salas
        current_x, current_y = self.current_room.x * self.room_width + self.current_room.x * MINIMAP_GAP, self.current_room.y * self.room_height + self.current_room.y * MINIMAP_GAP
        for room in self.visited_rooms:
            x, y = room[0], room[1]
            x, y = x * self.room_width + x * MINIMAP_GAP, y * self.room_height + y * MINIMAP_GAP
            pg.draw.rect(surface, self.color, (x, y, *self.room_dimensions), 4)
        # desenha a surface com todas as salas
        pg.draw.rect(surface, self.color, (current_x, current_y, *self.room_dimensions))
