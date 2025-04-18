import pygame
from pygame.math import Vector2 as vector
from math import sin, cos, radians
from random import randint
import json


class Sprite(pygame.sprite.Sprite):

    # Getting Game Settings
    with open("GameCode/GameSettings.json", "r") as f:
        x = f.read()
        settings = json.loads(x)

    def __init__(
        self,
        pos: tuple,
        surf: pygame.Surface = pygame.Surface(
            (settings["TILE_SIZE"], settings["TILE_SIZE"])
        ),
        groups: [pygame.sprite.Group] = None,
        z: int = settings["Z_LAYERS"]["main"],
    ):
        super().__init__(groups)

        self.image = surf

        # Rects
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.hit_rect = self.rect.inflate(-10, -10)

        self.z = z


class AnimatedSprite(Sprite):

    # Getting Game Settings
    with open("GameCode/GameSettings.json", "r") as f:
        x = f.read()
        settings = json.loads(x)

    def __init__(
        self,
        pos,
        frames,
        groups,
        z=settings["Z_LAYERS"]["main"],
        animation_speed=settings["ANIMATION_SPEED"],
    ):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed
        self.hit_rect = self.rect.inflate(-29, -29)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)


class ParticleEffectSprite(AnimatedSprite):

    # Getting Game Settings

    def __init__(self, pos, frames, groups):
        with open("GameCode/GameSettings.json", "r") as f:
            x = f.read()
            self.settings = json.loads(x)
        super().__init__(pos, frames, groups, self.settings["Z_LAYERS"]["fg"])

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
            del self


class Item(AnimatedSprite):
    def __init__(self, item_type, pos, frames, groups, data):
        super().__init__(pos, frames, groups)
        self.item_type = item_type
        self.data = data

    def activate(self):
        match self.item_type:
            case "gold":
                self.data.coins += 5
            case "silver":
                self.data.coins += 1
            case "diamond":
                self.data.coins += 20
            case "skull":
                self.data.coins += 50
            case "potion":
                self.data.health += 1


class MovingSprite(AnimatedSprite):
    def __init__(self, frames, groups, start_pos, end_pos, move_dir, speed):
        super().__init__(start_pos, frames, groups)
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
        self.hit_rect = self.rect.inflate(-10, -10)
        self.rect.topleft += self.direction * self.speed * dt
        self.check_borders()

        self.animate(dt)


class Spike(Sprite):

    with open("GameCode/GameSettings.json", "r") as f:
        x = f.read()
        settings = json.loads(x)

    def __init__(
        self,
        pos,
        surf,
        groups,
        radius,
        speed,
        start_angle,
        end_angle,
        z=settings["Z_LAYERS"]["main"],
    ):
        self.center = pos
        self.radius = radius
        self.speed = speed
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.angle = self.start_angle
        self.direction = 1
        self.full_circle = True if self.end_angle == -1 else False

        # Trig
        y = self.center[1] + sin(radians(self.angle)) * self.radius
        x = self.center[0] + cos(radians(self.angle)) * self.radius

        super().__init__((x, y), surf, groups, z)

    def update(self, dt):
        self.angle += self.direction * self.speed * dt

        if not self.full_circle:
            if self.angle > self.end_angle:
                self.direction = -1
            if self.angle < self.start_angle:
                self.direction = 1

        y = self.center[1] + sin(radians(self.angle)) * self.radius
        x = self.center[0] + cos(radians(self.angle)) * self.radius

        self.rect.center = (x, y)
        self.hit_rect = self.rect.inflate(-10, -10)


class Cloud(Sprite):

    with open("GameCode/GameSettings.json", "r") as f:
        x = f.read()
        settings = json.loads(x)

    def __init__(self, pos, surf, groups, z=settings["Z_LAYERS"]["clouds"]):
        super().__init__(pos, surf, groups, z)
        self.speed = randint(30, 120)
        self.direction = -1
        self.rect.bottomleft = pos

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

        if self.rect.right <= 0:
            self.kill()
            del self
