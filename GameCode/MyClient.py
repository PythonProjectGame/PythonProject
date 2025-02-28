import sys
from os.path import join
import cProfile

import pygame
import json
from Debug import debug
from GameData import Data
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

        # Getting Game Settings
        with open("GameCode/GameSettings.json", "r") as f:
            x = f.read()
            self.settings = json.loads(x)

        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()

        # Create the window
        self.display = pygame.display.set_mode(
            (self.settings["WIN_WIDTH"], self.settings["WIN_HEIGHT"])
        )

        # Set the caption
        pygame.display.set_caption("Pirate Cove")

        # Create the clock
        self.clock = pygame.time.Clock()

        # Import all the assets
        self.importAssets()

        # Create the UI
        self.ui = UI(self.font, self.ui_frames)

        # Load the data
        self.data = Data(self.ui)

        # Load the Tiled map
        self.tmx_maps = {
            0: load_pygame(join("Levels", "tmx", "1.tmx")),
            1: load_pygame(join("Levels", "tmx", "2.tmx")),
            2: load_pygame(join("Levels", "tmx", "3.tmx")),
            3: load_pygame(join("Levels", "tmx", "4.tmx")),
            4: load_pygame(join("Levels", "tmx", "5.tmx")),
            5: load_pygame(join("Levels", "tmx", "6.tmx")),
            "omni": load_pygame(join("Levels", "tmx", "omni.tmx")),
        }

        # Create the current level
        self.cur_stage = Level(
            self.tmx_maps[self.settings["LEVEL_CHOICE"]],
            self.level_frames,
            self.audio,
            self.data,
        )
        pygame.mixer.music.set_volume(
            0.3
            * self.settings["SOUND"]["SOUND_VOLUME"]
            * self.settings["SOUND"]["MUSIC_VOLUME"]
        )
        pygame.mixer.music.play(-1)

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

        self.audio = {
            "coin": pygame.mixer.Sound(join("Levels", "Audio", "coin.wav")),
            "jump": pygame.mixer.Sound(join("Levels", "Audio", "jump.wav")),
            "attack": pygame.mixer.Sound(join("Levels", "Audio", "attack.wav")),
            "hit": pygame.mixer.Sound(join("Levels", "Audio", "hit.wav")),
            "damage": pygame.mixer.Sound(join("Levels", "Audio", "damage.wav")),
            "pearl": pygame.mixer.Sound(join("Levels", "Audio", "pearl.wav")),
            "win": pygame.mixer.Sound(join("Levels", "Audio", "win.wav")),
            "lose": pygame.mixer.Sound(join("Levels", "Audio", "lose.wav")),
            "level_unlock": pygame.mixer.Sound(
                join("Levels", "Audio", "level_unlock.wav")
            ),
        }

        self.bg_audio = {
            "pixel-song-20": join("Levels", "Audio", "pixel-song-20.mp3"),
            "pixel-song-21": join("Levels", "Audio", "pixel-song-21.mp3"),
            "sometimes-i": join("Levels", "Audio", "sometimes-i.mp3"),
            "starlight_city": join("Levels", "Audio", "starlight_city.mp3"),
        }

        pygame.mixer.music.load(
            self.bg_audio[self.settings["BG_MUSIC"][self.settings["SONG_CHOICE"]]]
        )

    def switch_stage(self, stage: int) -> None:
        pass

    def check_game_over(self) -> None:
        if self.data.dead:
            # Quit the game if the player is dead
            pygame.mixer.music.stop()
            lose = self.audio["lose"]
            lose.set_volume(
                1
                * self.settings["SOUND"]["SOUND_VOLUME"]
                * self.settings["SOUND"]["MUSIC_VOLUME"]
            )
            lose.play()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

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

            self.check_game_over()

            # Update the current level
            self.cur_stage.run(dt)

            # Update the UI
            self.ui.update(dt)

            # Render the current frame
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    cProfile.run('game.run()', sort='ncalls')
