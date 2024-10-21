import pygame
import sys  # noqa: F401
from pygame.math import Vector2 as vector  # noqa: F401
from GameSettings import TILE_SIZE


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, surf, groups: [pygame.sprite.Group]):
        super().__init__(groups)

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill("White")

        # Rects
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
