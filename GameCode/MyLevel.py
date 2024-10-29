import pygame
import sys  # noqa: F401
from pygame.math import Vector2 as vector  # noqa: F401
from MySprites import Sprite, MovingSprite
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
        # Tiles
        for x, y, surf in tmx_map.get_layer_by_name("Terain").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                groups=(self.all_sprites, self.collision_sprites),
            )

        # Objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "Player":
                Player((obj.x, obj.y), surf, self.all_sprites, self.collision_sprites)

        # Moving Objects
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == "helicopter":
                # Calculating movement direction
                if obj.width > obj.height:  # Horizontal
                    move_dir = "x"
                    start_pos = ((obj.x)/2, (obj.y + obj.height / 2)/2)
                    end_pos = ((obj.x + obj.width)/2, (obj.y + obj.height / 2)/2)
                else:  # Vertical
                    move_dir = "y"
                    start_pos = ((obj.x + obj.width / 2)/2, (obj.y)/2)
                    end_pos = ((obj.x + obj.width / 2)/2, (obj.y + obj.height)/2)
                speed = obj.properties["speed"]
                MovingSprite((self.all_sprites, self.collision_sprites), start_pos, end_pos, move_dir, speed)

    def run(self, dt):
        self.all_sprites.update(dt)
        self.display.fill("gray")
        self.all_sprites.draw(self.display)
