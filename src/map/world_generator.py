import random
from src.map.room import Room
from utils import *
from random import randint
from src.entities.enemy import Enemy
# Essa classe é responsável pela geração do mundo do jogo. Define onde cada sala ira aparecer e também suas propriedades


class World:
    def __init__(self, width: int, height: int, max_rooms: int, game):
        self.game = game
        # width (colunas) e height (linhas) sao a grade de células (salas)
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.world = [[None for _ in range(width)] for _ in range(height)]  # cria uma grade de salas, por padrao todas estao vazias
        self.directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Cima, Baixo, Esquerda, Direita (x, y)
        self.current_room = None

        self.generate_map()

    def is_valid(self, x: int, y: int):
        # verifica se as cordenadas x e y tão dentro dos limites do mundo
        return 0 <= x < self.width and 0 <= y < self.height

    def generate_map(self):
        room_counter = 0  # contador de salas geradas
        x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        stack = [(x, y)]  # 'fila' de salas que devem ser criadas, contendo sua posição x e y (começa com uma celula aleatoria)

        while stack and room_counter < self.max_rooms:
            x, y = stack[-1]  # pega a última sala adicionada

            valid_directions = []  # celulas que cumprem as condições para serem adicionadas
            for plus_x, plus_y in self.directions:
                new_x, new_y = x + plus_x, y + plus_y
                if self.is_valid(new_x, new_y) and self.world[new_y][new_x] is None:  # verifica se há uma celula livre nessa direção
                    valid_directions.append((plus_x, plus_y))

            if not valid_directions:  # se for um 'beco sem saida', ele apaga a ultima sala da lista pra achar outra direção possivel
                stack.pop()
            else:
                # se tiver pelo menos uma direção valida, cria uma nova sala
                plus_x, plus_y = random.choice(valid_directions)  # escolhe uma direção valida aleatoria
                new_x, new_y = x + plus_x, y + plus_y

                room = self.world[new_y][new_x] = Room(new_x, new_y)
                stack.append((new_x, new_y))

                # define a sala inicial e final
                if room_counter == 0:
                    room.type = "boss_room"
                elif room_counter == self.max_rooms - 1:
                    room.type = "start_room"

                self.current_room = room

                room_counter += 1
        self.add_neighbors()

    def add_neighbors(self):
        # adiciona todos os vizinhos de todas as salas
        for row in self.world:
            for room in row:
                if isinstance(room, Room):
                    x, y = room.x, room.y
                    for direction_x, direction_y in self.directions:
                        new_x, new_y = x + direction_x, y + direction_y
                        if self.is_valid(new_x, new_y) and isinstance(self.world[new_y][new_x], Room):
                            room.neighbours.append([new_x, new_y])
                    room.add_doors()

    def draw_current_room(self):
        self.game.room_surface.fill((0, 0, 0, 0))
        print(self.current_room.enemy_list)
        self.current_room.draw_doors(self.game.room_surface)

    def change_current_room(self, direction: str):
        player_rect = self.game.player.rect

        # coordenadas uteis pra posicionar o jogador proximo a porta
        start_x, start_y = (WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2
        centerx, centery = start_x + (MAP_WIDTH - player_rect.width) / 2, start_y + (MAP_HEIGHT - player_rect.height) / 2

        # posição do vizinho da sala atual
        neighbour_x, neighbour_y = self.current_room.x, self.current_room.y

        # altera a sala e a posição do jogador com base na direção da proxima sala
        match direction:
            case "up":
                neighbour_y += -1
                new_player_pos = (centerx, start_y + MAP_HEIGHT - TILE_SIZE * 2.5 - player_rect.height)
            case "down":
                neighbour_y += 1
                new_player_pos = (centerx, start_y + player_rect.height)
            case "left":
                neighbour_x += -1
                new_player_pos = (start_x + MAP_WIDTH - TILE_SIZE * 2.5 - player_rect.width, centery)
            case "right":
                neighbour_x += 1
                new_player_pos = (start_x + TILE_SIZE * 1.5 + player_rect.width, centery)

        # altera a sala atual e a desenha, depois deixa o jogador proximo a porta que entrou
        self.current_room = self.world[neighbour_y][neighbour_x]
        self.game.minimap.set_current_room(self.current_room)
        self.draw_current_room()
        self.game.player.rect.x = new_player_pos[0]
        self.game.player.rect.y = new_player_pos[1]
        self.game.player.bullets = []  # remove todas as balas da sala anterior

        self.game.transition_alpha = 255
        self.game.transitioning = True

    def generate_enemies(self):
        for row in self.world:
            for room in row:
                if isinstance(room, Room) and room.type == "normal_room":
                    room.enemy_list = [Enemy(randint(1, 6), room, self.game) for _ in range(randint(4, 12))]

    def __str__(self):  # mostra no terminal o mapa
        world_str = ""
        for row in self.world:
            for room in row:
                if isinstance(room, Room):
                    if room.x == self.current_room.x and room.y == self.current_room.y:
                        world_str += "X "
                    elif room.type == 'start_room':
                        world_str += "S "
                    elif room.type == 'boss_room':
                        world_str += "B "
                    else:
                        world_str += "1 "
                else:
                    world_str += "0 "
            world_str += "\n"
        return world_str

    def __repr__(self):
        return str(self.world)
