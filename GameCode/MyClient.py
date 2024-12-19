import sys
from os.path import join

import pygame
from Debug import debug
from GameData import Data
from GameSettings import *
from MyLevel import Level
from MySupport import (
    import_folder,
    import_folder_dict,
    import_image,
    import_sub_folders,
)
from MyUi import UI
from pytmx.util_pygame import load_pygame


class Game:
    """
    The main class for the game.
    """

    def __init__(self):
        """
        Initialize the game.

        This includes setting up Pygame, creating the window, setting the caption,
        and creating the clock. It also imports all the assets for the game,
        creates the UI, loads the data, loads the Tiled map, and creates the
        current level.
        """
        # Initialize Pygame
        pygame.init()

        # Create the window
        self.display = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT),  # pygame.FULLSCREEN
        )

        # Set the caption
        pygame.display.set_caption("Sound Assassin")

        # Create the clock
        self.clock = pygame.time.Clock()

        # Import all the assets
        self.importAssets()

        # Create the UI
        self.ui = UI(self.font, self.ui_frames)

        # Load the data
        self.data = Data(self.ui)

        # Load the Tiled map
        self.tmx_maps = {0: load_pygame(join("Levels", "tmx", "omni.tmx"))}

        # Create the current level
        self.cur_stage = Level(self.tmx_maps[0], self.level_frames, self.data)

    def importAssets(self):
        """
        Import all the assets for the game.

        The assets are grouped into level frames, UI frames, and the font.
        """
        # Level frames
        self.level_frames = {
            # Enemies
            "helicopter": import_folder("Levels", "Graphics", "Level", "helicopter"),
            "saw": import_folder("Levels", "Enemies", "saw", "animation"),
            "saw_chain": import_image("Levels", "Enemies", "saw", "saw_chain"),
            "floor_spike": import_folder("Levels", "Enemies", "floor_spike"),
            # Background
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
            # Player
            "player": import_sub_folders("Levels", "Graphics", "Player"),
            # Items
            "spike": import_image("Levels", "Enemies", "ball_spike", "spiked ball"),
            "spike_chain": import_image(
                "Levels", "Enemies", "ball_spike", "spiked chain"
            ),
            "tooth": import_folder("Levels", "Enemies", "Tooth", "run"),
            "shell": import_sub_folders("Levels", "Enemies", "Shell"),
            "pearl": import_image("Levels", "Enemies", "pearl", "pearl"),
            "items": import_sub_folders("Levels", "Graphics", "Items"),
            # Particle
            "particle": import_folder("Levels", "Graphics", "particle"),
            # Flag
            "flag": import_folder("Levels", "Graphics", "Level", "flag"),
            # Background tiles
            "bg_tiles": import_folder_dict(
                "Levels", "Graphics", "Level", "BG", "Tiles"
            ),
            # Sky
            "cloud_large": import_image(
                "Levels", "Graphics", "Level", "BG", "Sky", "large_cloud"
            ),
            "cloud_small": import_folder(
                "Levels", "Graphics", "Level", "BG", "Sky", "small_clouds"
            ),
        }
        # Font
        self.font = pygame.font.Font(
            join("Levels", "Graphics", "UI", "runescape_uf.ttf"), 40
        )
        # UI frames
        self.ui_frames = {
            "heart": import_folder("Levels", "Graphics", "UI", "heart"),
            "coin": import_image("Levels", "Graphics", "UI", "coin"),
        }

    def run(self) -> None:
        """
        The main loop of the game.

        This is the main entry point for the game. It contains the main loop
        which handles events, updates, and rendering.
        """
        while True:
            # Get the delta time (dt) in seconds
            dt = self.clock.tick() / 1000

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit the game if the user closes the window
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Quit the game if the user presses the escape key
                        pygame.quit()
                        sys.exit()

            # Update the current level
            self.cur_stage.run(dt)

            # Update the UI
            self.ui.update(dt)

            # Render the current frame
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
