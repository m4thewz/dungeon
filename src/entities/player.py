import pygame as pg
from utils import *
from src.entities.base import Entity
import math
SCALE = lambda x: PLAYER_WIDTH * x / 16

class Player(Entity):
    def __init__(self, game):
        super().__init__("player.png", TILE_SIZE, TILE_SIZE * 1.5, (WIDTH // 2, HEIGHT // 2))
        self.game = game
        self.weapon_sprite = pg.transform.scale(pg.image.load("assets/weapons/gun.png").convert_alpha(), (SCALE(23), SCALE(8)))
        self.weapon_image = self.weapon_sprite
        self.weapon_rect = self.weapon_image.get_rect()

    def update(self):
        self.basic_update()
        self.movement(pg.key.get_pressed())
        self.rotate_weapon()

    def rotate_weapon(self):
        player_pos, mouse_pos = self.rect.center, pg.mouse.get_pos()
        dx, dy =  mouse_pos[0] - player_pos[0], mouse_pos[1] - player_pos[1] # distancia x e y entre o mouse e o centro do jogador
        angle = math.degrees(math.atan2(-dy, dx)) # função matematica que retorna o angulo entre dois pontos (no caso o mouse e o jogador)
        center_diff = (SCALE(2), -SCALE(2)) if self.direction else (-SCALE(4), -SCALE(2))  # posição da arma
        origin = (self.rect.centerx - center_diff[0], self.rect.centery - center_diff[1]) # ponto de origem do eixo da arma

        # posiciona o retangulo da arma em seu eixo de origem 
        weapon_rect = self.weapon_sprite.get_rect(topleft=origin) if self.direction else self.weapon_sprite.get_rect(bottomleft=origin)
        # cria um vetor e entao o rotaciona
        pivot = pg.math.Vector2(origin) - weapon_rect.center
        offset = pivot.rotate(-angle)
        # rotaciona a imagem da arma e a posiciona com base no eixo de origem
        self.weapon_image = pg.transform.rotozoom(self.weapon_sprite, angle, 1)
        self.weapon_rect = self.weapon_image.get_rect(center=(origin[0] - offset.x, origin[1] - offset.y))

    def draw(self, surface):
        self.draw_shadow(surface, (0, 0, self.rect.width / 2, self.rect.height / 8))
        surface.blit(self.image, self.rect)
        surface.blit(self.weapon_image, self.weapon_rect)

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
            self.weapon_sprite = pg.transform.flip(self.weapon_sprite, False, True)
            self.direction = distance > 0
