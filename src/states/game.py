import pygame as pg
from utils import *
from src.states.base import BaseState
from src.map.world_generator import World
from src.map.tileset import Tileset
from src.map.minimap import Minimap
from src.entities.player import Player

minimap_width = WIDTH // 2
minimap_height = HEIGHT // 2


class GameState (BaseState):
    def __init__(self, screen, main):
        self.screen = screen
        self.main = main
        self.world_manager = World(5, 5, 10, self)
        self.wall_list = []  # lista dos retangulos da porta (pra colisão

        # todas as "camadas" do mapa
        self.base_map_surface = pg.Surface(MAP_RES).convert()
        self.room_surface = pg.Surface(MAP_RES, pg.SRCALPHA).convert_alpha()
        self.transition_surface = pg.Surface(MAP_RES).convert_alpha()
        self.minimap_surface = pg.Surface(MINIMAP_SIZE).convert_alpha()

        self.base_map_surface.fill(BACKGROUND)
        self.room_surface.fill(BACKGROUND)
        self.minimap_surface.fill(BACKGROUND)
        self.transition_surface.fill(BACKGROUND)
        self.transition_alpha = 255
        self.transitioning = True
        Tileset().generate_map(self.base_map_surface, *MAP_RES, self)

        self.player = Player(self)
        self.minimap = Minimap()
        self.minimap.set_current_room(self.world_manager.current_room)
        self.world_manager.draw_current_room()
        pg.mouse.set_visible(False)
        self.cursor_image = pg.transform.scale(pg.image.load("assets/cursor.png").convert_alpha(), (16, 16))
        self.cursor_rect = self.cursor_image.get_rect(center=pg.mouse.get_pos())

    def transition(self, From: int = 255, To: int = 0, change: int = -10):
        alpha = self.transition_alpha
        if (From <= alpha and alpha <= To) or (To <= alpha and alpha <= From):
            self.transition_alpha += change
        else:
            self.transitioning = False
        self.transition_surface.set_alpha(self.transition_alpha)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                print(self.world_manager)
            elif event.key in [pg.K_ESCAPE, pg.K_RETURN, pg.K_KP_ENTER, pg.K_PAUSE]:
                self.change_state("pause_menu")
        else:
            self.player.get_event(event)

    def update(self):
        if self.transitioning:
            self.transition()
        self.player.update()
        self.cursor_rect.center = pg.mouse.get_pos()

    def draw(self):
        self.minimap_surface.fill(BACKGROUND)
        self.screen.blit(self.base_map_surface, ((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2))
        self.screen.blit(self.room_surface, ((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2))
        self.player.draw(self.screen)
        if self.transitioning:
            self.screen.blit(self.transition_surface, ((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2))

        self.minimap.draw(self.minimap_surface)
        self.screen.blit(self.minimap_surface, (WIDTH - (MINIMAP_ROOM_SIZE[0] + MINIMAP_GAP) * 5, MINIMAP_GAP))

        self.screen.blit(self.cursor_image, self.cursor_rect)
