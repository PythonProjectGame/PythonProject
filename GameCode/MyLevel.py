import pygame
import sys  # noqa: F401
from pygame.math import Vector2 as vector  # noqa: F401
from MySprites import Sprite, MovingSprite
from MyPlayer import Player
from GameSettings import TILE_SIZE


class Level:
    def __init__(self, tmx_map) -> None:
        self.display = pygame.display.get_surface()
        
        self.aspect_ratio = 32/TILE_SIZE

        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.semicollision_sprites = pygame.sprite.Group()

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
                Player(
                    (obj.x, obj.y),
                    surf,
                    self.all_sprites,
                    self.collision_sprites,
                    self.semicollision_sprites,
                )

        # Moving Objects
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == "helicopter":
                # Calculating movement direction
                if obj.width > obj.height:  # Horizontal
                    move_dir = "x"
                    start_pos = ((obj.x) / self.aspect_ratio, (obj.y + obj.height / 2) / self.aspect_ratio)
                    end_pos = ((obj.x + obj.width) / self.aspect_ratio, (obj.y + obj.height / 2) / self.aspect_ratio)
                else:  # Vertical
                    move_dir = "y"
                    start_pos = ((obj.x + obj.width / 2) / self.aspect_ratio, (obj.y) / self.aspect_ratio)
                    end_pos = ((obj.x + obj.width / 2) / self.aspect_ratio, (obj.y + obj.height) / self.aspect_ratio)
                speed = obj.properties["speed"]
                MovingSprite(
                    (self.all_sprites, self.semicollision_sprites),
                    start_pos,
                    end_pos,
                    move_dir,
                    speed,
                )

    def run(self, dt):
        self.all_sprites.update(dt)
        self.display.fill("gray")
        self.all_sprites.draw(self.display)
