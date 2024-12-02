import pygame
import sys
from pytmx.util_pygame import load_pygame
from os.path import join
from MyLevel import Level
from GameSettings import WIN_WIDTH, WIN_HEIGHT
from MySupport import (
    import_folder,
    import_sub_folders,
    import_image,
    import_folder_dict,
)
from GameData import Data
from Debug import debug  # Noqa: F401
from MyUi import UI


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT),  # pygame.FULLSCREEN
        )
        pygame.display.set_caption("Sound Assassin")
        self.clock = pygame.time.Clock()
        self.importAssets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.tmx_maps = {0: load_pygame(join("Levels", "tmx", "omni.tmx"))}
        self.cur_stage = Level(self.tmx_maps[0], self.level_frames, self.data)

    def importAssets(self):
        self.level_frames = {
            "helicopter": import_folder("Levels", "Graphics", "Level", "helicopter"),
            "saw": import_folder("Levels", "Enemies", "saw", "animation"),
            "saw_chain": import_image("Levels", "Enemies", "saw", "saw_chain"),
            "floor_spike": import_folder("Levels", "Enemies", "floor_spike"),
            "palms": import_sub_folders("Levels", "Graphics", "Level", "palms"),
            "big_chain": import_folder(
                "Levels", "Graphics", "Level", "BG", "big_chain"
            ),
            "small_chain": import_folder(
                "Levels", "Graphics", "Level", "BG", "small_chain"
            ),
            "candle": import_folder("Levels", "Graphics", "Level", "BG", "candle"),
            "candle_light": import_folder(
                "Levels", "Graphics", "Level", "BG", "candle_light"
            ),
            "player": import_sub_folders("Levels", "Graphics", "Player"),
            "spike": import_image("Levels", "Enemies", "ball_spike", "spiked ball"),
            "spike_chain": import_image(
                "Levels", "Enemies", "ball_spike", "spiked chain"
            ),
            "tooth": import_folder("Levels", "Enemies", "Tooth", "run"),
            "shell": import_sub_folders("Levels", "Enemies", "Shell"),
            "pearl": import_image("Levels", "Enemies", "pearl", "pearl"),
            "items": import_sub_folders("Levels", "Graphics", "Items"),
            "particle": import_folder("Levels", "Graphics", "particle"),
            "flag": import_folder("Levels", "Graphics", "Level", "flag"),
            "bg_tiles": import_folder_dict(
                "Levels", "Graphics", "Level", "BG", "Tiles"
            ),
            "cloud_large": import_image(
                "Levels", "Graphics", "Level", "BG", "Sky", "large_cloud"
            ),
            "cloud_small": import_folder(
                "Levels", "Graphics", "Level", "BG", "Sky", "small_clouds"
            ),
        }
        self.font = pygame.font.Font(
            join("Levels", "Graphics", "UI", "runescape_uf.ttf"), 40
        )
        self.ui_frames = {
            "heart": import_folder("Levels", "Graphics", "UI", "heart"),
            "coin": import_image("Levels", "Graphics", "UI", "coin"),
        }

    def run(self) -> None:
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.cur_stage.run(dt)
            self.ui.update(dt)
            pygame.display.update()


game = Game()
game.run()
