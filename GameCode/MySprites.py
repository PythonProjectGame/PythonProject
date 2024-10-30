import pygame
import sys  # noqa: F401
from pygame.math import Vector2 as vector  # noqa: F401
from GameSettings import TILE_SIZE


class Sprite(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple,
        surf: pygame.Surface = pygame.Surface((TILE_SIZE, TILE_SIZE)),
        groups: [pygame.sprite.Group] = None,
    ):
        super().__init__(groups)

        self.image = surf
        self.image.fill("White")

        # Rects
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()


class MovingSprite(Sprite):
    def __init__(self, groups, start_pos, end_pos, move_dir, speed):
        surf = pygame.Surface((TILE_SIZE * 4, TILE_SIZE))
        super().__init__(start_pos, surf, groups)
        if move_dir == "x":
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos

        # Movement
        self.moving = True
        self.speed = speed
        self.move_dir = move_dir
        self.direction = vector(1, 0) if move_dir == "x" else vector(0, 1)
        
    def check_borders(self):
        if self.move_dir == "x":
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_pos[0]
            elif self.rect.left <= self.start_pos[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_pos[0]
        if self.move_dir == "y":
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]
            elif self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_pos[1]
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt
        self.check_borders()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: [pygame.sprite.Group], wallSprites):
        super().__init__(groups)

        self.image = pygame.Surface((10, 10))
        self.image.fill("Black")

        self.rect = self.image.get_frect(center=pos)
        self.old_rect = self.rect.copy()

        self.wallSprites = wallSprites

        self.direction_vector = vector(0, 0)

        self.speed = 1000

    def direction(self, start: [int, int]):
        x, y = pygame.mouse.get_pos()
        self.direction_vector = vector(x - start[0], y - start[1]).normalize()

    def move(self, dt):
        self.rect.topleft += self.direction_vector * self.speed * dt

    def collision(self):
        if pygame.sprite.spritecollideany(self, self.wallSprites):
            self.kill()

    def update(self, dt: float):
        self.move(dt)
        self.collision()
