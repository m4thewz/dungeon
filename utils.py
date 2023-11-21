import pygame as pg

# variaveis e funções globais aqui
RES = WIDTH, HEIGHT = 1450, 900
MAP_RES = MAP_WIDTH, MAP_HEIGHT = 1200, 700
TILE_SIZE = 50
TITLE_RES = ((0.5 * WIDTH, 0.3 * HEIGHT))  # 60% e 40% do tamanho da tela

MINIMAP_GAP = 5
MINIMAP_ROOM_SIZE = 35, 20
MINIMAP_SIZE = (MINIMAP_GAP + MINIMAP_ROOM_SIZE[0]) * 5, (MINIMAP_GAP + MINIMAP_ROOM_SIZE[1]) * 5

BACKGROUND = (00, 00, 00)
COLOR = (250, 250, 250)

PLAYER_SPEED = 10
PLAYER_WIDTH = TILE_SIZE

BULLET_SPEED = 13
BULLET_SIZE = (16, 8)


# funções globais

def GET_MASK_RECT(surf, top=0, left=0):
    mask = pg.mask.from_surface(surf)
    rect_list = mask.get_bounding_rects()
    if rect_list:
        mask_rect = rect_list[0].unionall(rect_list)
        mask_rect.move_ip(top, left)
        return mask_rect


def OFFSET(rect1, rect2): return (rect2[0] - rect1[0], rect2[1] - rect1[1])
