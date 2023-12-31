import pygame as pg
from utils import *
from src.entities.base import Entity
import math

# retorna uma escala com base  no tamanho do jogador
def SCALE(x): return PLAYER_WIDTH * x / 16


class Player(Entity):
    # inicia a classe do jogador e define variaveis importantes
    def __init__(self, game):
        super().__init__("player.png", TILE_SIZE, TILE_SIZE * 1.5, (WIDTH // 2, HEIGHT // 2))
        self.game = game
        self.weapon_sprite = pg.transform.scale(pg.image.load("assets/weapons/gun.png").convert_alpha(), (SCALE(23), SCALE(8)))
        self.weapon_image = self.weapon_sprite
        self.weapon_rect = self.weapon_image.get_rect()
        self.bullets = []
        self.hp = 10
        self.direction = 1  # 0: esquerda, 1: direita

    def update(self):
        # se o jogador tiver mais de 0 de hp, atualzia o jogador e sua arma, caso contrario encerra o jogo
        if self.hp > 0:
            self.basic_update()
            self.movement(pg.key.get_pressed())
            self.rotate_weapon()
            [bullet.update() for bullet in self.bullets]
        else:
            self.game.change_state("game_over")

    def rotate_weapon(self):
        dx, dy = OFFSET(self.rect.center, pg.mouse.get_pos())  # distancia x e y entre o mouse e o centro do jogador
        angle = math.degrees(math.atan2(-dy, dx))  # função matematica que retorna o angulo entre dois pontos (no caso o mouse e o jogador)
        center_diff = (SCALE(2), -SCALE(2)) if self.direction else (-SCALE(4), -SCALE(2))  # posição da arma
        origin = (self.rect.centerx - center_diff[0], self.rect.centery - center_diff[1])  # ponto de origem do eixo da arma

        # posiciona o retangulo da arma em seu eixo de origem
        weapon_rect = self.weapon_sprite.get_rect(topleft=origin) if self.direction else self.weapon_sprite.get_rect(bottomleft=origin)
        # cria um vetor e entao o rotaciona
        pivot = pg.math.Vector2(origin) - weapon_rect.center
        offset = pivot.rotate(-angle)
        # rotaciona a imagem da arma e a posiciona com base no eixo de origem
        self.weapon_image = pg.transform.rotozoom(self.weapon_sprite, angle, 1)
        self.weapon_rect = self.weapon_image.get_rect(center=(origin[0] - offset.x, origin[1] - offset.y))

    def draw(self, surface):
        # desenha o jogador, sua sombra, sua arma e tambem as balas presentes na tela
        self.draw_shadow(surface, (0, 0, self.rect.width / 2, self.rect.height / 8))
        surface.blit(self.image, self.rect)
        surface.blit(self.weapon_image, self.weapon_rect)
        [surface.blit(bullet.image, bullet.rect) for bullet in self.bullets]

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.bullets.append(Bullet(self)) # atira
        elif event.type == 77: # evento personalizado, ativado quando o jogador sofre dano. Deixa ele vermelho temporariamente
            self.image = pg.transform.scale(pg.image.load("assets/characters/player.png").convert_alpha(), (TILE_SIZE, TILE_SIZE * 1.5))
            if not self.direction:
                self.image = pg.transform.flip(self.image, True, False)
            pg.time.set_timer(77, 0)  # desliga o evento de ID 77

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
            # verifica se a sala esta aberta (se nao tem nenhum inimigo)
            if not self.game.world_manager.current_room.enemy_list:
                hitbox = door.hitbox.move((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2)  # posiciona a parede no local certo para fazer a colisao
                if any(hitbox.collidepoint(point) for point in collide_points):
                    self.velocity = [0, 0]
                    self.game.world_manager.change_current_room(door.direction)

        for wall in self.game.wall_list:
            hitbox = wall.hitbox.move((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2)  # posiciona a parede no local certo para fazer a colisao
            if any(hitbox.collidepoint(point) for point in collide_points):
                self.velocity = [0, 0]

    def update_direction(self):
        # atualiza a direção da imagem do jogador com base na direção do mouse
        distance = pg.mouse.get_pos()[0] - self.rect.x
        if distance <= 0 and self.direction != 0 or distance > 0 and self.direction != 1:
            self.image = pg.transform.flip(self.image, True, False)
            self.weapon_sprite = pg.transform.flip(self.weapon_sprite, False, True)
            self.direction = distance > 0


# classe das balas
class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        # define o angulo da bala, sua imagem ja rotacionada e sua velocidade
        pg.sprite.Sprite.__init__(self)
        dx, dy = OFFSET(player.rect.center, pg.mouse.get_pos())

        # apos obter a distsancia do mouse e do jogador, define a imagem (ja rotacionada com base no angulo)
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

        # se colidir com uma parede ou inimigo, a remove da lista de balas presentes
        for wall in self.player.game.wall_list:
            hitbox = wall.hitbox.move((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2)  # posiciona a parede no local certo para fazer a colisao
            if pg.Rect.colliderect(hitbox, self.rect):
                self.player.bullets.pop(self.player.bullets.index(self))
                return

        for enemy in self.player.game.world_manager.current_room.enemy_list:
            if self.rect.colliderect(enemy.hitbox):
                self.player.bullets.pop(self.player.bullets.index(self))
                enemy.hp -= 1
                return
