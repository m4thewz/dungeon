import pygame as pg
from utils import *
from src.states.base import BaseState
from src.map.world_generator import World
from src.map.tileset import Tileset
from src.map.minimap import Minimap
from src.entities.player import Player


class GameState (BaseState):
    def __init__(self, screen, main):
        self.screen = screen
        self.main = main
        self.world_manager = World(5, 5, 10, self)
        self.wall_list = []

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

        # base map
        Tileset().generate_map(self.base_map_surface, *MAP_RES, self)

        self.player = Player(self)
        self.minimap = Minimap()

        self.minimap.set_current_room(self.world_manager.current_room)
        self.world_manager.draw_current_room()

        self.world_manager.generate_enemies()

        # custom cursor
        self.cursor_image = pg.transform.scale(pg.image.load("assets/cursor.png").convert_alpha(), (16, 16))
        self.cursor_rect = self.cursor_image.get_rect(center=pg.mouse.get_pos())

        # life bar
        self.lifebar_image = pg.transform.scale_by(pg.image.load("assets/hp/base.png"), LIFEBAR_SCALE).convert_alpha()
        self.life_image = pg.transform.scale_by(pg.image.load("assets/hp/full.png"), LIFEBAR_SCALE).convert_alpha()

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
            elif event.key == pg.K_c:
                print(self.world_manager.current_room.enemy_list)
            elif event.key in [pg.K_ESCAPE, pg.K_RETURN, pg.K_KP_ENTER, pg.K_PAUSE]:
                self.change_state("pause_menu")
        else:
            self.player.get_event(event)

    def update(self):
        self.player.update()
        self.cursor_rect.center = pg.mouse.get_pos()
        if self.transitioning:
            self.transition()
        else:
            [enemy.update() for enemy in self.world_manager.current_room.enemy_list]

    def draw(self):
        # draw base room and doors
        self.screen.blit(self.base_map_surface, ((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2))
        self.screen.blit(self.room_surface, ((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2))

        [enemy.draw(self.screen) for enemy in self.world_manager.current_room.enemy_list]
        self.player.draw(self.screen)

        # transition layer
        if self.transitioning:
            self.screen.blit(self.transition_surface, ((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2))

        # desenha o minimapa
        self.minimap_surface.fill(BACKGROUND)
        self.minimap.draw(self.minimap_surface)
        self.screen.blit(self.minimap_surface, (WIDTH - (MINIMAP_ROOM_SIZE[0] + MINIMAP_GAP) * 5, MINIMAP_GAP))

        # UI
        self.draw_hp(self.screen)
        self.screen.blit(pg.font.Font("assets/Blockhead.otf", 32).render(f"{self.main.clock.get_fps() :.1f} FPS", True, COLOR), (15, 125))

        water_mark = pg.font.Font(None, 16).render("Matheus Vitor, 1º INFO - IFSP JCR", True, COLOR)

        self.screen.blit(water_mark, (WIDTH - water_mark.get_width() - 5, HEIGHT - water_mark.get_height() - 5))

        self.screen.blit(self.cursor_image, self.cursor_rect)

    def draw_hp(self, surface):
        lifebar_pos = (15, 25)
        start_x, start_y = 23 * LIFEBAR_SCALE + lifebar_pos[0], 9 * LIFEBAR_SCALE + lifebar_pos[1]
        surface.blit(self.lifebar_image, lifebar_pos)

        for index in range(self.player.hp):
            x = start_x + index * self.life_image.get_width() + index * LIFEBAR_SCALE
            surface.blit(self.life_image, (x, start_y))
