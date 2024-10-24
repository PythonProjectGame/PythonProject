import pygame
import sys  # noqa: F401
from pygame.math import Vector2 as vector
from GameSettings import TILE_SIZE
from MySprites import Bullet
from MyTimer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple,
        surf,
        groups: [pygame.sprite.Group],
        collision_sprites: [pygame.sprite.Sprite],
    ) -> None:
        super().__init__(groups)

        self.groups = groups

        self.image = pygame.Surface((TILE_SIZE-2, TILE_SIZE-2))
        self.image.fill("red")

        # Rects
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        # Movement values
        self.direction = vector()
        self.speed = 300
        self.gravity = 1300
        self.jump = False
        self.jump_height = 400

        # Collisions
        self.collision_sprites = collision_sprites
        self.on_surface = {"floor": False, "left": False, "right": False}

        # Timer
        self.timers = {
            "wall jump": Timer(100),
            "fire rate": Timer(100),
            "wall slide block": Timer(250),
        }

        # Weapon values
        self.next_bullet = pygame.time.get_ticks()
        self.fire_rate = 100

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

        if not self.timers["wall jump"].active:
            if keys[pygame.K_RIGHT] | keys[pygame.K_d]:
                input_vector.x += 1
            if keys[pygame.K_LEFT] | keys[pygame.K_a]:
                input_vector.x -= 1
            self.direction.x = (
                input_vector.normalize().x if input_vector.x else input_vector.x
            )

        if keys[pygame.K_SPACE]:
            self.jump = True

        if keys[pygame.K_LSHIFT]:
            self.speed = 10
        else:
            self.speed = 300

        if pygame.mouse.get_pressed()[0] and not self.timers["fire rate"].active:
            self.timers["fire rate"].activate()
            bullet = Bullet(
                (self.rect.centerx, self.rect.centery),
                "Surf",
                (self.groups),
                self.collision_sprites,
            )
            bullet.direction((self.rect.centerx, self.rect.centery))

    def move(self, dt: float) -> None:
        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("Horizontal")

        # Vertical
        if (
            not self.on_surface["floor"]
            and any((self.on_surface["left"], self.on_surface["right"]))
            and not self.timers["wall slide block"].active
        ):
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt

        self.collision("Vertical")

        if self.jump:
            if self.on_surface["floor"]:
                self.direction.y = -self.jump_height
                self.timers["wall slide block"].activate()
            elif (
                any((self.on_surface["left"], self.on_surface["right"]))
                and not self.timers["wall slide block"].active
            ):
                self.timers["wall jump"].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface["left"] else -1
            self.jump = False

    # Checks contacts between all surfaces
    def checkContact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        left_rect = pygame.Rect(
            self.rect.topleft + vector(-2, self.rect.height / 4),
            (2, self.rect.height / 2),
        )
        right_rect = pygame.Rect(
            self.rect.topright + vector(0, self.rect.height / 4),
            (2, self.rect.height / 2),
        )
        collision_rects = [sprite.rect for sprite in self.collision_sprites]

        self.on_surface["floor"] = (
            True if floor_rect.collidelist(collision_rects) >= 0 else False
        )
        self.on_surface["left"] = (
            True if left_rect.collidelist(collision_rects) >= 0 else False
        )
        self.on_surface["right"] = (
            True if right_rect.collidelist(collision_rects) >= 0 else False
        )

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

    def updateTimers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt: float) -> None:
        self.old_rect = self.rect.copy()
        self.updateTimers()
        self.input()
        self.move(dt)
        self.checkContact()
