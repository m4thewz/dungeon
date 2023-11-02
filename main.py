import pygame as pg
import sys
from utils import *
from src.map.world_generator import World
from src.entities.player import Player

minimap_width = WIDTH // 2
minimap_height = HEIGHT // 2


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()

        self.world_manager = World(5, 5, 10, self)
        self.map_surface = pg.Surface(MAP_RES)
        self.map_surface.fill(BACKGROUND)
        self.player = Player(self)
        self.world_manager.draw_current_room()

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
        self.clock.tick(60)
        self.player.update()

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.screen.blit(self.map_surface, ((WIDTH - MAP_WIDTH) / 2, (HEIGHT - MAP_HEIGHT) / 2))
        self.player.draw(self.screen)

    def run(self):
        while True:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    Game().run()
