# Essa clase contem todas informações essencias das salas
import pygame as pg
from utils import *

from src.map.tileset import Tile


class Door(Tile):
    def __init__(self, direction: str, open: bool = False):
        width, height = MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE
        centerx, centery = ((width - 4) // 2) * TILE_SIZE, ((height - 3) // 2) * TILE_SIZE

        match direction:
            case "up":
                angle = 0
                x, y = centerx, 0
            case "down":
                x, y = centerx, (height - 3) * TILE_SIZE
                angle = 180
            case "left":
                x, y = 0, centery
                angle = 90
            case "right":
                x, y = (width - 3) * TILE_SIZE, centery
                angle = -90
        image_location = "door_opened" if open else "door_closed"
        image = pg.transform.rotate(pg.transform.scale(pg.image.load(f"assets/map/{image_location}.png").convert_alpha(), (TILE_SIZE * 4, TILE_SIZE * 3)), angle)
        super().__init__(image_location, x, y, image)
        self.image_opened = pg.transform.rotate(pg.transform.scale(pg.image.load("assets/map/door_opened.png").convert_alpha(), (TILE_SIZE * 4, TILE_SIZE * 3)), angle)
        self.direction = direction

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Room:
    def __init__(self, x: int, y: int, type: str = "normal_room"):
        self.x = x
        self.y = y
        self.type = type
        self.discovered = False
        self.map = {}
        self.doors = []  # list with doors direction
        self.doors_rect = []
        self.neighbours = []
        self.enemy_list = []

    def add_doors(self):
        # add a door in direction of neighbours
        for neighbour in self.neighbours:
            distance_x = self.x - neighbour[0]
            distance_y = self.y - neighbour[1]

            if distance_x == 1:
                self.doors.append("left")
            if distance_x == -1:
                self.doors.append("right")
            if distance_y == 1:
                self.doors.append("up")
            if distance_y == -1:
                self.doors.append("down")

    def draw_doors(self, surface):
        open = True if not self.enemy_list else False
        self.doors_rect = [Door(direction, open) for direction in self.doors]
        [door.draw(surface) for door in self.doors_rect]

        if self.type == "start_room":
            image = pg.transform.scale_by(pg.image.load("assets/keys.png"), 1.5).convert_alpha()
            x = (surface.get_width() - image.get_width()) / 2
            y = (surface.get_height() - image.get_height()) / 2

            surface.blit(image, (x, y))

    def __repr__(self):
        return f"({self.x}, {self.y}, '{self.type}')"

    def __str__(self):
        return self.__repr__()
