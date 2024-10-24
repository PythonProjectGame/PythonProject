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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, surf, groups: [pygame.sprite.Group], wallSprites):
        super().__init__(groups)

        self.image = pygame.Surface((10, 10))
        self.image.fill("Black")

        self.rect = self.image.get_frect(center=pos)
        self.old_rect = self.rect.copy()
        
        self.wallSprites = wallSprites
        
        self.direction_vector = vector(0,0)

        self.speed = 500

    def direction(self, start: [int, int]):
        x, y = pygame.mouse.get_pos()
        self.direction_vector = vector(
            x - start[0], y - start[1]
        ).normalize()
        
    def move(self, dt):
        self.rect.topleft += self.direction_vector *  self.speed *dt

    def collision(self):
        if pygame.sprite.spritecollideany(self, self.wallSprites):
            self.kill()
    
    def update(self, dt: float):
        self.move(dt)
        self.collision()
