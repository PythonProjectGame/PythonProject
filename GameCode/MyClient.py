import pygame
import sys

# sys.path.append("../PythonProject")
# import MyNetwork
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2 as vector  # noqa: F401
from os.path import join
from MyLevel import Level
from GameSettings import WIN_WIDTH, WIN_HEIGHT
from MySupport import import_folder, import_sub_folders

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT), #pygame.FULLSCREEN
        )
        pygame.display.set_caption("Sound Assassin")
        self.clock = pygame.time.Clock()
        self.importAssets()

        self.tmx_maps = {0: load_pygame(join("Levels", "tmx", "omni.tmx"))}

        self.cur_stage = Level(self.tmx_maps[0], self.level_frames)
    
    def importAssets(self):
        self.level_frames = {
            "helicopter": import_folder("Levels", "Graphics", "Level", "helicopter"),
            "saw": import_folder("Levels", "Enemies", "saw", "animation"),
            "floor_spike": import_folder("Levels", "Enemies", "floor_spike"),
            "palms": import_sub_folders("Levels", "Graphics", "Level","palms"),
            "big_chain": import_folder("Levels", "Graphics", "Level", "BG", "big_chain"),
            "small_chain": import_folder("Levels", "Graphics", "Level", "BG", "small_chain"),
            "candle": import_folder("Levels", "Graphics", "Level", "BG", "candle"),
            "candle_light": import_folder("Levels", "Graphics", "Level", "BG", "candle_light"),
            "player": import_sub_folders("Levels", "Graphics", "Player")
        }

    def run(self) -> None:
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.cur_stage.run(dt)
            pygame.display.update()


game = Game()
game.run()
