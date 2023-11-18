import pygame as pg
from utils import *
from src.entities.base import Entity
import random
from math import hypot

enemies_options = {
    1: {
        "speed": 4.7,
        "hp": 1
    },
    2: {
        "speed": 3.7,
        "hp": 2
    },
    3: {
        "speed": 3.7,
        "hp": 2
    },
    4: {
        "speed": 3,
        "hp": 6
    },
    5: {
        "speed": 3,
        "hp": 5
    },
    6: {
        "speed": 3,
        "hp": 5
    }
}


def draw_health_bar(surface, pos, size, border_color, back_color, health_color, progress):
    pg.draw.rect(surface, back_color, (*pos, *size))
    pg.draw.rect(surface, border_color, (*pos, *size), 1)
    inner_pos = (pos[0] + 1, pos[1] + 1)
    inner_size = ((size[0] - 2) * progress, size[1] - 2)
    rect = (round(inner_pos[0]), round(inner_pos[1]), round(inner_size[0]), round(inner_size[1]))
    pg.draw.rect(surface, health_color, rect)


class Enemy(Entity):
    def __init__(self, name, room, game):
        Entity.__init__(self, f"enemies/{name}.png", TILE_SIZE, TILE_SIZE)
        self.speed = enemies_options[name]["speed"]
        self.hp = self.max_hp = enemies_options[name]["hp"]
        self.direction = 1
        self.room = room
        self.game = game
        self.spawn()

    def spawn(self):
        start_x, start_y = (WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2
        wall_size = TILE_SIZE * 3  # tamanho da parede (pra nao spawnar inimigo dentro das paredes)
        self.rect.x = random.randint(start_x + wall_size, start_x + MAP_WIDTH - wall_size)
        self.rect.y = random.randint(start_y + wall_size, start_y + MAP_HEIGHT - wall_size)

    def draw_health(self, surface):
        if self.hp < self.max_hp:
            health_rect = pg.Rect(0, 0, 30, 8)
            health_rect.midbottom = self.rect.centerx, self.hitbox.top - 5
            draw_health_bar(surface, health_rect.topleft, health_rect.size, (1, 0, 0), (255, 0, 0), (0, 255, 0), self.hp / self.max_hp)

    def draw(self, surface):
        self.draw_shadow(surface, (0, 0, self.hitbox.width / 1.8, self.rect.height / 8))
        surface.blit(self.image, self.rect)
        self.draw_health(surface)

    def update(self):
        if self.hp <= 0:
            self.room.enemy_list.pop(self.room.enemy_list.index(self))
            # vai abrir as portas da sala
            if not self.room.enemy_list:
                self.game.world_manager.draw_current_room()
        else:
            player = self.game.player
            # pega a distancia entre o inimigo e o jogador
            dx, dy = OFFSET(self.rect.center, player.rect.center)
            distance = hypot(dx, dy)

            # se o inimigo acertou o jogador
            if self.hitbox.colliderect(player.hitbox):
                self.room.enemy_list.pop(self.room.enemy_list.index(self))
                player.hp -= 1
                if player.hp > 0:
                    player.image = pg.transform.scale(pg.image.load("assets/characters/player_hurt.png").convert_alpha(), (TILE_SIZE, TILE_SIZE * 1.5))
                    # define um evento de ID 77 pra ser executado a cada 2 segundos (pra fazer a imagem do jogador voltar ao normal)
                    pg.time.set_timer(77, 2000)
                else:
                    # desliga o evento
                    pg.time.set_timer(77, 0)

            if distance > 0:
                self.rect.x += dx * self.speed / distance
                self.rect.y += dy * self.speed / distance
        self.basic_update()

    def update_direction(self):
        dx = OFFSET(self.rect.center, self.game.player.rect.center)[0]
        if dx <= 0 and self.direction != 0 or dx > 0 and self.direction != 1:
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = dx > 0
