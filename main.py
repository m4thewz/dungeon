import pygame as pg
import sys
from utils import *
from src.map.world_generator import World
from src.map.tileset import Tileset
from src.map.minimap import Minimap
from src.entities.player import Player

minimap_width = WIDTH // 2
minimap_height = HEIGHT // 2


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
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

    def transition(self, From: int = 255, To: int = 0, change: int = -10):
        alpha = self.transition_alpha
        if (From <= alpha and alpha <= To) or (To <= alpha and alpha <= From):
            self.transition_alpha += change
        else:
            self.transitioning = False
        self.transition_surface.set_alpha(self.transition_alpha)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    print(self.world_manager)
            else:
                self.player.get_event(event)

    def update(self):
        pg.display.set_caption(f'Dungeon Invader - {self.clock.get_fps() :.1f} FPS')
        if self.transitioning:
            self.transition()
        self.player.update()
        self.clock.tick(60)

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.minimap_surface.fill(BACKGROUND)
        self.screen.blit(self.base_map_surface, ((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2))
        self.screen.blit(self.room_surface, ((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2))
        self.player.draw(self.screen)
        if self.transitioning:
            self.screen.blit(self.transition_surface, ((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2))

        self.minimap.draw(self.minimap_surface)
        self.screen.blit(self.minimap_surface, (WIDTH - (MINIMAP_ROOM_SIZE[0] + MINIMAP_GAP) * 5, MINIMAP_GAP))

    def run(self):
        while True:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    Game().run()
