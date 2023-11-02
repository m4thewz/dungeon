# Essa clase contem todas informações essencias das salas
import pygame as pg
from utils import *

from src.map.tileset import generate_tilesets


class Tile(pg.sprite.Sprite):
    # cria um retangulo para cada imagem do mapa, util pra as colisões
    def __init__(self, tile_name: str, x: int, y: int, image=None):
        pg.sprite.Sprite.__init__(self)
        self.type = tile_name
        self.image = image if image else tileset[tile_name]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


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
        image = pg.transform.rotate(tileset["door"], angle)
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
        self.wall_list = []
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

    def generate_map(self, width: int, height: int):
        global tileset
        self.tileset = tileset = generate_tilesets()

        # mais tarde adicionar mais tilesets pra randomizar o chao.
        self.map_width = map_width = width // TILE_SIZE
        self.map_height = map_height = height // TILE_SIZE

        minimap = [["floor" for _ in range(map_width)] for _ in range(map_height)]

        # Um dicionario que contem as informações de cada tileset
        self.map = {
            (row_index, col_index): tileset_index for row_index, row in enumerate(minimap) for col_index, tileset_index in enumerate(row)
        }
        # Define as paredes horizontais
        for pos in range(2, map_width - 2):
            self.map[1, pos] = "wall_top"
            self.map[map_height - 2, pos] = "wall_bottom"

        # Define as paredes verticais
        for pos in range(2, map_height - 2):
            self.map[pos, 1] = "wall_left"
            self.map[pos, (map_width - 2)] = "wall_right"

        # Define as paredes diagonais
        # X = posição da penultima ou segunda célula da linha, Y = posição da penultima ou segunda célula da coluna
        self.map[1, 1] = "wall_diagonal_upper_left"
        self.map[map_height - 2, 1] = "wall_diagonal_bottom_left"
        self.map[1, map_width - 2] = "wall_diagonal_upper_right"
        self.map[map_height - 2, map_width - 2] = "wall_diagonal_bottom_right"

        # Define bordas horizontais

        # Define as primeiras bordas das primeiras e ultimas linhas
        # X = posição da primeira célula da linha, Y = posição da ultima ou primeira célula da coluna
        self.map[0, 1] = "border_horizontal_start_top"
        self.map[map_height - 1, 1] = "border_horizontal_start_bottom"

        for pos in range(2, map_width - 2):
            self.map[0, pos] = "border_horizontal_middle_top"
            self.map[map_height - 1, pos] = "border_horizontal_middle_bottom"

        # Define as últimas bordas das primeiras e ultimas linhas
        # X = posição da última célula da linha, Y = posição da ultima ou primeira célula da coluna

        self.map[0, map_width - 2] = "border_horizontal_end_top"
        self.map[map_height - 1, map_width - 2] = "border_horizontal_end_bottom"

        # Define bordas verticais; aqui X e Y tem os mesmos valores, porém invertidos (X = y, Y = x)
        self.map[1, 0] = "border_vertical_start_left"
        self.map[1, map_width - 1] = "border_vertical_start_right"

        for pos in range(2, map_height - 2):
            self.map[pos, 0] = "border_vertical_middle_left"
            self.map[pos, map_width - 1] = "border_vertical_middle_right"

        self.map[map_height - 2, 0] = "border_vertical_end_left"
        self.map[map_height - 2, map_width - 1] = "border_vertical_end_right"

        # Define as bordas diagonais dos 4 cantos
        # X = posição da primeira ou última célula da linha, Y = posição da primeira ou última célula da coluna
        self.map[0, 0] = "border_diagonal_upper_left"
        self.map[map_height - 1, 0] = "border_diagonal_bottom_left"
        self.map[0, map_width - 1] = "border_diagonal_upper_right"
        self.map[map_height - 1, map_width - 1] = "border_diagonal_bottom_right"

        # adiciona a image das portas numa lista
        self.doors_rect = [Door(direction) for direction in self.doors]

    def draw_map(self, surface):
        # É preciso notar que o mapa é uma coluna, que consite em várias linhas e colunas, e tendo cada célula uma imagem a ser exibida
        for pos in self.map:
            tile_name = self.map[pos]
            tile = Tile(tile_name, pos[1] * TILE_SIZE, pos[0] * TILE_SIZE)
            if tile_name.startswith("wall"):
                self.wall_list.append(tile)
            tile.draw(surface)
            self.map[pos] = tile

        # desenha as portas
        [door.draw(surface) for door in self.doors_rect]

    def __repr__(self):
        return f"({self.x}, {self.y}, '{self.type}')"

    def __str__(self):
        return self.__repr__()
