import pygame
import sys  # noqa: F401
from pygame.math import Vector2 as vector  # noqa: F401
from MySprites import Sprite
from MyPlayer import Player
from GameSettings import TILE_SIZE


class Level:
    def __init__(self, tmx_map) -> None:
        self.display = pygame.display.get_surface()

        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name("Terain").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.all_sprites, self.collision_sprites),
            )

        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "Player":
                Player((obj.x, obj.y), surf, self.all_sprites, self.collision_sprites)

    def run(self, dt):
        self.all_sprites.update(dt)
        self.display.fill("gray")
        self.all_sprites.draw(self.display)
