import pygame as pg
from utils import *


class Entity(pg.sprite.Sprite):
    def __init__(self, image: str, width: int, height: int, position: tuple = (0, 0), hp: int = 10):
        pg.sprite.Sprite.__init__(self)
        self.hp = hp
        self.image = pg.transform.scale(pg.image.load(f"assets/characters/{image}").convert_alpha(), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.hitbox = GET_MASK_RECT(self.image, *self.rect.topleft)
        self.velocity = [0, 0] 
        self.direction = 1  # left, right = 0, 1

    def update_hitbox(self):
        self.hitbox = GET_MASK_RECT(self.image, *self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom

    def basic_update(self):
        self.update_hitbox()
        self.rect.move_ip(*self.velocity)
        self.hitbox.move_ip(*self.velocity)
        self.update_direction()

    def update_direction(self):
        pass

    def movement(self):
        pass

    def draw(self, surface):
        self.draw_shadow(surface, (0, 0, self.rect.width / 2, self.rect.height / 8))
        surface.blit(self.image, self.rect)

    def draw_shadow(self, surface, size, dimension=50, vertical_shift=-6, horizontal_shift=0):
        ellipse = pg.Surface((dimension, dimension), pg.SRCALPHA).convert_alpha()
        pg.draw.ellipse(ellipse, (0, 0, 0, 50), size)
        ellipse = pg.transform.scale(ellipse, (2 * dimension, 2 * dimension))
        position = [self.hitbox.bottomleft[0] + horizontal_shift, self.hitbox.bottomleft[1] + vertical_shift]
        surface.blit(ellipse, position)
