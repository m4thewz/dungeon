# Essa clase contem todas informações essencias das salas
import pygame as pg
from utils import *

from src.map.tileset import Tile


# adiciona alguns parametros adicionais da class Tile para as portas
class Door(Tile):
    def __init__(self, direction: str):
        width, height = MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE
        centerx, centery = ((width - 4) // 2) * TILE_SIZE, ((height - 3) // 2) * TILE_SIZE
        # define o angulo e a posição da porta com base na direção
        match direction:
            case "up":
                angle = 0
                x, y = centerx, 0
            case "down":
                x, y = centerx, (height - 2) * TILE_SIZE
                angle = 180
            case "left":
                x, y = 0, centery
                angle = 90
            case "right":
                x, y = (width - 2) * TILE_SIZE, centery
                angle = -90
        image = pg.transform.rotate(pg.transform.scale(pg.image.load("assets/map/door.png").convert_alpha(), (TILE_SIZE * 4, TILE_SIZE * 2)), angle)
        super().__init__("door", x, y, image)
        self.openned = False
        self.direction = direction
        self.angle = angle

    def draw(self, surface):
        if not self.openned:  # *mais tarde tem q fazer porta aberta e nao deixar trocar de porta se a porta tiver fechada
            surface.blit(self.image, (self.rect.x, self.rect.y))


class Room:
    def __init__(self, x: int, y: int, type: str = "normal_room"):
        self.x = x
        self.y = y
        self.type = type
        self.discovered = False  # jogador ja entrou na sala
        self.map = {}
        self.doors = []  # lista com apenas as direções das portas
        self.doors_rect = []  # lista com os sprites das portas
        self.neighbours = []  # salas vizinhas
        self.enemy_list = []

    def add_doors(self):
        # pega a direção dos vizinhos e adiciona (pra porta)
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
        self.doors_rect = [Door(direction) for direction in self.doors]
        [door.draw(surface) for door in self.doors_rect]

    def __repr__(self):
        return f"({self.x}, {self.y}, '{self.type}')"

    def __str__(self):
        return self.__repr__()
