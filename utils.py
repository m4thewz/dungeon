import pygame as pg

# variaveis e funções globais aqui
RES = WIDTH, HEIGHT = 1450, 900
MAP_RES = MAP_WIDTH, MAP_HEIGHT = 1200, 700
TILE_SIZE = 50
MINIMAP_GAP = 5
MINIMAP_ROOM_SIZE = 35, 20
MINIMAP_SIZE = (MINIMAP_GAP + MINIMAP_ROOM_SIZE[0]) * 5, (MINIMAP_GAP + MINIMAP_ROOM_SIZE[1]) * 5
BACKGROUND = (00, 00, 00)

PLAYER_SPEED = 10


def get_mask_rect(surf, top=0, left=0):
    mask = pg.mask.from_surface(surf)
    rect_list = mask.get_bounding_rects()
    if rect_list:
        mask_rect = rect_list[0].unionall(rect_list)
        mask_rect.move_ip(top, left)
        return mask_rect
