import pygame as pg
from utils import *


class Minimap:
    room_width, room_height = room_dimensions = MINIMAP_ROOM_SIZE
    color = (173, 173, 173)

    def __init__(self):
        self.current_room = None
        self.current_x, self.current_y = None, None
        self.rooms = []
        self.visited_rooms = []

    def visit_room(self, room):
        if [room.x, room.y] not in self.visited_rooms:
            self.visited_rooms.append([room.x, room.y])

    def set_current_room(self, room):
        self.visit_room(room)
        if self.current_room is not room:
            self.current_room = room

    def draw(self, surface):
        current_x, current_y = self.current_room.x * self.room_width + self.current_room.x * MINIMAP_GAP, self.current_room.y * self.room_height + self.current_room.y * MINIMAP_GAP
        for room in self.visited_rooms:
            x, y = room[0], room[1]
            x, y = x * self.room_width + x * MINIMAP_GAP, y * self.room_height + y * MINIMAP_GAP
            pg.draw.rect(surface, self.color, (x, y, *self.room_dimensions), 4)
        pg.draw.rect(surface, self.color, (current_x, current_y, *self.room_dimensions))
