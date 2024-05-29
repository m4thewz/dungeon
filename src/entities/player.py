import pygame as pg
from utils import *
from src.entities.base import Entity
import math

def SCALE(x): return PLAYER_WIDTH * x / 16


class Player(Entity):
    def __init__(self, game):
        super().__init__("player.png", TILE_SIZE, TILE_SIZE * 1.5, (WIDTH // 2, HEIGHT // 2))
        self.game = game
        self.weapon_sprite = pg.transform.scale(pg.image.load("assets/weapons/gun.png").convert_alpha(), (SCALE(23), SCALE(8)))
        self.weapon_image = self.weapon_sprite
        self.weapon_rect = self.weapon_image.get_rect()
        self.bullets = []
        self.hp = 10
        self.direction = 1

    def update(self):
        if self.hp > 0:
            self.basic_update()
            self.movement(pg.key.get_pressed())
            self.rotate_weapon()
            [bullet.update() for bullet in self.bullets]
        else:
            self.game.change_state("game_over")

    def rotate_weapon(self):
        dx, dy = OFFSET(self.rect.center, pg.mouse.get_pos())  # distance x and y between player and mouse
        angle = math.degrees(math.atan2(-dy, dx))  # return the angle between mouse and player
        center_diff = (SCALE(2), -SCALE(2)) if self.direction else (-SCALE(4), -SCALE(2))  # gun position
        origin = (self.rect.centerx - center_diff[0], self.rect.centery - center_diff[1])  # origin point of gun axle
        weapon_rect = self.weapon_sprite.get_rect(topleft=origin) if self.direction else self.weapon_sprite.get_rect(bottomleft=origin)

        # generate a vector and then spin it
        pivot = pg.math.Vector2(origin) - weapon_rect.center
        offset = pivot.rotate(-angle)
        
        self.weapon_image = pg.transform.rotozoom(self.weapon_sprite, angle, 1)
        self.weapon_rect = self.weapon_image.get_rect(center=(origin[0] - offset.x, origin[1] - offset.y))

    def draw(self, surface):
        self.draw_shadow(surface, (0, 0, self.rect.width / 2, self.rect.height / 8))
        surface.blit(self.image, self.rect)
        surface.blit(self.weapon_image, self.weapon_rect)
        [surface.blit(bullet.image, bullet.rect) for bullet in self.bullets]

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.bullets.append(Bullet(self)) # shoot
        elif event.type == 77: # event activated when the player takes damage (turn player red)
            self.image = pg.transform.scale(pg.image.load("assets/characters/player.png").convert_alpha(), (TILE_SIZE, TILE_SIZE * 1.5))
            if not self.direction:
                self.image = pg.transform.flip(self.image, True, False)
            pg.time.set_timer(77, 0)  # turns off the event 77

    def movement(self, keys):
        keys_pressed = 0
        dy, dx = 0, 0

        # (AWSD kes, directions keys, X change, Y change)
        directions = [(pg.K_w, pg.K_UP, 0, -PLAYER_SPEED), (pg.K_a, pg.K_LEFT, -PLAYER_SPEED, 0), (pg.K_s, pg.K_DOWN, 0, PLAYER_SPEED), (pg.K_d, pg.K_RIGHT, PLAYER_SPEED, 0)]

        for key, direction_key, x, y in directions:
            if keys[key] or keys[direction_key]:
                keys_pressed += 1
                dx += x
                dy += y

        if keys_pressed == 2:
            dx *= 1 / math.sqrt(2)
            dy *= 1 / math.sqrt(2)

        self.velocity = [dx, dy]

        # rect test to test player position when moving
        test_rect = self.hitbox.move(dx, dy)
        collide_points = (test_rect.midbottom, test_rect.bottomleft, test_rect.bottomright)

        for door in self.game.world_manager.current_room.doors_rect:
            if not self.game.world_manager.current_room.enemy_list:
                hitbox = door.hitbox.move((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2)  # right place to collision
                if any(hitbox.collidepoint(point) for point in collide_points):
                    self.velocity = [0, 0]
                    self.game.world_manager.change_current_room(door.direction)

        for wall in self.game.wall_list:
            hitbox = wall.hitbox.move((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2)
            if any(hitbox.collidepoint(point) for point in collide_points):
                self.velocity = [0, 0]

    def update_direction(self):
        distance = pg.mouse.get_pos()[0] - self.rect.x
        if distance <= 0 and self.direction != 0 or distance > 0 and self.direction != 1:
            self.image = pg.transform.flip(self.image, True, False)
            self.weapon_sprite = pg.transform.flip(self.weapon_sprite, False, True)
            self.direction = distance > 0


class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        dx, dy = OFFSET(player.rect.center, pg.mouse.get_pos())

        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load("assets/weapons/bullet.png").convert_alpha(), BULLET_SIZE), math.degrees(math.atan2(-dy, dx)))
        self.rect = self.image.get_rect(center=(player.weapon_rect.centerx, player.weapon_rect.centery))
        self.speed = BULLET_SPEED
        self.angle = math.atan2(dy, dx)
        self.player = player

        self.rect.centerx += math.cos(self.angle) * (player.weapon_image.get_width() // 2 + 3)
        self.rect.centery += math.sin(self.angle) * (player.weapon_image.get_width() // 2 + 3)

    def update(self):
        # atualiza sua direção
        self.rect.centerx += math.cos(self.angle) * self.speed
        self.rect.centery += math.sin(self.angle) * self.speed

        for wall in self.player.game.wall_list:
            hitbox = wall.hitbox.move((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2)
            if pg.Rect.colliderect(hitbox, self.rect):
                self.player.bullets.pop(self.player.bullets.index(self))
                return

        for enemy in self.player.game.world_manager.current_room.enemy_list:
            if self.rect.colliderect(enemy.hitbox):
                self.player.bullets.pop(self.player.bullets.index(self))
                enemy.hp -= 1
                return
