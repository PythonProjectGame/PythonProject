import pygame
import sys  # noqa: F401
from pygame.math import Vector2 as vector
from GameSettings import TILE_SIZE


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple,
        surf,
        groups: [pygame.sprite.Group],
        collision_sprites: [pygame.sprite.Sprite],
    ) -> None:
        super().__init__(groups)

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill("red")

        # Rects
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        # Movement values
        self.direction = vector()
        self.speed = 400
        self.gravity = 1300

        # Collisions
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        self.direction.x = (
            input_vector.normalize().x if input_vector.x else input_vector.x
        )

        if keys[pygame.K_SPACE]:
            self.direction.y = -500

    def move(self, dt: float) -> None:
        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("Horizontal")

        # Vertical
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision("Vertical")

    def collision(self, axis: str) -> None:
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == "Horizontal":
                    # Left
                    if all(
                        [
                            self.rect.left <= sprite.rect.right,
                            self.old_rect.left >= sprite.old_rect.right,
                        ]
                    ):
                        self.rect.left = sprite.rect.right

                    # Right
                    if all(
                        [
                            self.rect.right >= sprite.rect.left,
                            self.old_rect.right <= sprite.old_rect.left,
                        ]
                    ):
                        self.rect.right = sprite.rect.left

                else:  # Vertical
                    # Top
                    if all(
                        [
                            self.rect.top <= sprite.rect.bottom,
                            self.old_rect.top >= sprite.old_rect.bottom,
                        ]
                    ):
                        self.rect.top = sprite.rect.bottom

                    # Bottom
                    if all(
                        [
                            self.rect.bottom >= sprite.rect.top,
                            self.old_rect.bottom <= sprite.old_rect.top,
                        ]
                    ):
                        self.rect.bottom = sprite.rect.top

                    self.direction.y = 0

    def update(self, dt: float) -> None:
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
