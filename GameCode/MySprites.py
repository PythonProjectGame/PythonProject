import pygame
import sys  # noqa: F401
from pygame.math import Vector2 as vector  # noqa: F401
from GameSettings import TILE_SIZE, Z_LAYERS, ANIMATION_SPEED


class Sprite(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple,
        surf: pygame.Surface = pygame.Surface((TILE_SIZE, TILE_SIZE)),
        groups: [pygame.sprite.Group] = None,
        z: int = Z_LAYERS["main"],
    ):
        super().__init__(groups)

        self.image = surf

        # Rects
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        self.z = z


class AnimatedSprite(Sprite):
    def __init__(
        self, pos, frames, groups, z=Z_LAYERS["main"], animation_speed=ANIMATION_SPEED
    ):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed
    
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        
        
    def update(self, dt):
        self.animate(dt)


class MovingSprite(Sprite):
    def __init__(self, groups, start_pos, end_pos, move_dir, speed):
        surf = pygame.Surface((TILE_SIZE * 4, TILE_SIZE))
        super().__init__(start_pos, surf, groups)
        self.image.fill("white")
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
