import pygame as pg
from utils import *

def load_resized_tile(image):
    return pg.transform.scale(pg.image.load(image).convert_alpha(), (TILE_SIZE, TILE_SIZE))

def generate_tilesets():
    # Defino as imagens que serão utilizas
    # border_horizontal e border_vertical são uma lista de 3 texturas (start, middle, end)
    border = load_resized_tile("assets/map/wall_border_diagonal.png")
    border_horizontal = [load_resized_tile(f"assets/map/wall_border_horizontal_{image}.png") for image in ["start", "middle", "end"]]
    border_vertical = [load_resized_tile(f"assets/map/wall_border_vertical_{image}.png") for image in ["start", "middle", "end"]]
    wall = load_resized_tile("assets/map/wall.png")
    wall_diagonal = load_resized_tile("assets/map/wall_diagonal.png")
    return {
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
        "floor": load_resized_tile("assets/map/floor.png"),
        "door": pg.transform.scale(pg.image.load("assets/map/door.png").convert_alpha(), (TILE_SIZE * 4, TILE_SIZE * 2))
    }