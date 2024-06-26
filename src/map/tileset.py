import pygame as pg
from utils import *
tileset = None


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_name: str, x: int, y: int, image=None):
        pg.sprite.Sprite.__init__(self)
        self.type = tile_name
        self.image = image if image else tileset[tile_name]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hitbox = GET_MASK_RECT(self.image, *self.rect.topleft)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Tileset:
    def generate_map(self, surface, width: int, height: int, game):
        self.generate_tilesets()
        # TODO: add floor tilesets
        self.map_width = map_width = width // TILE_SIZE
        self.map_height = map_height = height // TILE_SIZE

        # matrix of map, every  element represents one image
        minimap = [["floor" for _ in range(map_width)] for _ in range(map_height)]

        # dict with tilisets infos
        self.map = {
            (row_index, col_index): tileset_index for row_index, row in enumerate(minimap) for col_index, tileset_index in enumerate(row)
        }
        # horizontal walls
        for pos in range(2, map_width - 2):
            self.map[1, pos] = "wall_top"
            self.map[map_height - 2, pos] = "wall_bottom"

        # vertical walls
        for pos in range(2, map_height - 2):
            self.map[pos, 1] = "wall_left"
            self.map[pos, (map_width - 2)] = "wall_right"

        # diagonal walls
        self.map[1, 1] = "wall_diagonal_upper_left"
        self.map[map_height - 2, 1] = "wall_diagonal_bottom_left"
        self.map[1, map_width - 2] = "wall_diagonal_upper_right"
        self.map[map_height - 2, map_width - 2] = "wall_diagonal_bottom_right"

        # horizontal borders
        self.map[0, 1] = "border_horizontal_start_top"
        self.map[map_height - 1, 1] = "border_horizontal_start_bottom"

        for pos in range(2, map_width - 2):
            self.map[0, pos] = "border_horizontal_middle_top"
            self.map[map_height - 1, pos] = "border_horizontal_middle_bottom"

        self.map[0, map_width - 2] = "border_horizontal_end_top"
        self.map[map_height - 1, map_width - 2] = "border_horizontal_end_bottom"

        # vertical borders
        self.map[1, 0] = "border_vertical_start_left"
        self.map[1, map_width - 1] = "border_vertical_start_right"

        for pos in range(2, map_height - 2):
            self.map[pos, 0] = "border_vertical_middle_left"
            self.map[pos, map_width - 1] = "border_vertical_middle_right"

        self.map[map_height - 2, 0] = "border_vertical_end_left"
        self.map[map_height - 2, map_width - 1] = "border_vertical_end_right"

        # diagonal borders
        self.map[0, 0] = "border_diagonal_upper_left"
        self.map[map_height - 1, 0] = "border_diagonal_bottom_left"
        self.map[0, map_width - 1] = "border_diagonal_upper_right"
        self.map[map_height - 1, map_width - 1] = "border_diagonal_bottom_right"

        for pos in self.map:
            tile_name = self.map[pos]
            tile = Tile(tile_name, pos[1] * TILE_SIZE, pos[0] * TILE_SIZE)
            if tile_name.startswith("wall"):
                game.wall_list.append(tile)
            tile.draw(surface)
            self.map[pos] = tile

        for x in range(2, map_width - 2):
            Tile("shadow_horizontal_top", x * TILE_SIZE, 2 * TILE_SIZE).draw(surface)
            Tile("shadow_horizontal_bottom", x * TILE_SIZE, (map_height - 3) * TILE_SIZE).draw(surface)
        for y in range(2, map_height - 2):
            Tile("shadow_vertical_left", 2 * TILE_SIZE, y * TILE_SIZE).draw(surface)
            Tile("shadow_vertical_right", (map_width - 3) * TILE_SIZE, y * TILE_SIZE).draw(surface)

    def generate_tilesets(self):
        global tileset
        border = self.load_resized_tile("assets/map/wall_border_diagonal.png")
        border_horizontal = [self.load_resized_tile(f"assets/map/wall_border_horizontal_{image}.png") for image in ["start", "middle", "end"]]
        border_vertical = [self.load_resized_tile(f"assets/map/wall_border_vertical_{image}.png") for image in ["start", "middle", "end"]]
        wall = self.load_resized_tile("assets/map/wall.png")
        wall_diagonal = self.load_resized_tile("assets/map/wall_diagonal.png")

        tileset = self.tileset = {
            "border_diagonal_upper_left": border,
            "border_diagonal_upper_right": pg.transform.rotate(border, -90),
            "border_diagonal_bottom_left": pg.transform.rotate(border, 90),
            "border_diagonal_bottom_right": pg.transform.rotate(border, 180),
            "border_horizontal_start_top": border_horizontal[0],
            "border_horizontal_middle_top": border_horizontal[1],
            "border_horizontal_end_top": border_horizontal[2],
            "border_horizontal_start_bottom": pg.transform.rotate(border_horizontal[0], 180),
            "border_horizontal_middle_bottom": pg.transform.rotate(border_horizontal[1], 180),
            "border_horizontal_end_bottom": pg.transform.rotate(border_horizontal[2], 180),
            "border_vertical_start_left": border_vertical[0],
            "border_vertical_middle_left": border_vertical[1],
            "border_vertical_end_left": border_vertical[2],
            "border_vertical_start_right": pg.transform.rotate(border_vertical[0], 180),
            "border_vertical_middle_right": pg.transform.rotate(border_vertical[1], 180),
            "border_vertical_end_right": pg.transform.rotate(border_vertical[2], 180),
            "wall_top": wall,
            "wall_bottom": pg.transform.flip(wall, False, True),
            "wall_left": pg.transform.rotate(wall, 90),
            "wall_right": pg.transform.rotate(wall, -90),
            "wall_diagonal_upper_left": wall_diagonal,
            "wall_diagonal_upper_right": pg.transform.rotate(wall_diagonal, -90),
            "wall_diagonal_bottom_left": pg.transform.rotate(wall_diagonal, 90),
            "wall_diagonal_bottom_right": pg.transform.rotate(wall_diagonal, 180),
            "floor": self.load_resized_tile("assets/map/floor.png"),
            "shadow_vertical_right": self.load_resized_tile("assets/map/floor_shadow_vertical.png"),
            "shadow_vertical_left": self.load_resized_tile("assets/map/floor_shadow_vertical_left.png"),
            "shadow_horizontal_bottom": self.load_resized_tile("assets/map/floor_shadow_horizontal.png"),
            "shadow_horizontal_top": self.load_resized_tile("assets/map/floor_shadow_horizontal_top.png")
        }

    def load_resized_tile(self, image):
        return pg.transform.scale(pg.image.load(image).convert_alpha(), (TILE_SIZE, TILE_SIZE))
