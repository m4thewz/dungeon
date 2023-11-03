import pygame as pg
from utils import *
from src.entities.base import Entity
import math


class Player(Entity):
    def __init__(self, game):
        super().__init__("player.png", TILE_SIZE, TILE_SIZE * 1.5, (WIDTH // 2, HEIGHT // 2))
        self.game = game

    def update(self):
        self.basic_update()
        self.movement(pg.key.get_pressed())

    def get_event(self, event):
        pass

    def movement(self, keys):
        keys_pressed = 0
        dy, dx = 0, 0  # distancia a ser alterada na posição

        # (tecla AWSD, tecla setinha, mudança no X, mudança no Y)
        directions = [(pg.K_w, pg.K_UP, 0, -PLAYER_SPEED), (pg.K_a, pg.K_LEFT, -PLAYER_SPEED, 0), (pg.K_s, pg.K_DOWN, 0, PLAYER_SPEED), (pg.K_d, pg.K_RIGHT, PLAYER_SPEED, 0)]

        for key, direction_key, x, y in directions:
            if keys[key] or keys[direction_key]:  # se for pressionado uma tecla AWSD ou uma das setinhas
                keys_pressed += 1
                dx += x
                dy += y

        # quando é realizado o movimento diagonal, ao somar na posição o DX e DY, ele nao vai ter movido exatamente a distancia requerida
        # mas sim a raiz de DX² + DY² (pitagoras)
        # pra concertar isso é so multiplicar DX e DY por 1 / raiz de 2 (formula de correção de vetor)
        if keys_pressed == 2:
            dx *= 1 / math.sqrt(2)
            dy *= 1 / math.sqrt(2)

        self.velocity = [dx, dy]

        # cria uma rect de teste para verificar aonde o jogador ficaria ao se mover
        test_rect = self.hitbox.move(dx, dy)
        collide_points = (test_rect.midbottom, test_rect.bottomleft, test_rect.bottomright)

        for door in self.game.world_manager.current_room.doors_rect:
            hitbox = door.hitbox.move((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2)  # posiciona a parede no local certo para fazer a colisao
            if any(hitbox.collidepoint(point) for point in collide_points):
                self.velocity = [0, 0]
                self.game.world_manager.change_current_room(door.direction)

        for wall in self.game.wall_list:
            hitbox = wall.hitbox.move((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2)  # posiciona a parede no local certo para fazer a colisao
            if any(hitbox.collidepoint(point) for point in collide_points):
                self.velocity = [0, 0]

    def update_direction(self):
        distance = pg.mouse.get_pos()[0] - self.rect.x
        if distance <= 0 and self.direction != 0 or distance > 0 and self.direction != 1:
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = distance > 0
