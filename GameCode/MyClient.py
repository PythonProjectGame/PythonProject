import pygame
import sys
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2 as vector  # noqa: F401
from MyLevel import Level
from GameSettings import WIN_WIDTH, WIN_HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Sound Assassin")
        self.clock = pygame.time.Clock()

        self.tmx_maps = {
            0: load_pygame(
                "/home/Aiden/ComputerScience/VS/PythonProject/Levels/tmx/omni.tmx"
            )
        }
        print(self.tmx_maps)

        self.cur_stage = Level(self.tmx_maps[0])

    def run(self) -> None:
        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.cur_stage.run(dt)
            pygame.display.update()


game = Game()
game.run()
