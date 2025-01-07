import pygame
from pygame import Vector2 as vector
from random import randint, choice
import json
from MySprites import Sprite, Cloud
from MyTimer import Timer


class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, clouds, horizon_line, bg_tile=None, top_limit=0):
        super().__init__()

        # Getting Game Settings
        with open("GameCode/GameSettings.json", "r") as f:
            x = f.read()
            self.settings = json.loads(x)

        self.display = pygame.display.get_surface()
        self.offset = vector()
        self.width = width * self.settings["TILE_SIZE"]
        self.height = height * self.settings["TILE_SIZE"]
        self.win_size = (self.width, self.height)
        self.borders = {
            "left": 0,
            "right": -self.width + self.settings["WIN_WIDTH"],
            "top": top_limit,
            "bottom": -self.height + self.settings["WIN_HEIGHT"],
        }
        self.sky = not bg_tile
        self.horizon_line = horizon_line

        if bg_tile:
            for col in range(int(width / 2)):
                for row in range(-int(top_limit / TILE_SIZE) - 1, int(height / 2)):
                    x, y = col * 64, row * 64
                    Sprite((x, y), bg_tile, self, -1)
        else:
            self.large_cloud = clouds["large"]
            self.small_clouds = clouds["small"]
            self.cloud_direction = -1

            # Large Cloud
            self.large_cloud_speed = 50
            self.large_cloud_x = 0
            self.large_cloud_tiles = int(self.width / self.large_cloud.get_width()) + 2
            self.large_cloud_width, self.large_cloud_height = (
                self.large_cloud.get_size()
            )

            # Small Clouds
            self.new_cloud = Timer(2500, self.createCloud, True)
            self.new_cloud.activate()

            for cloud in range(10):
                pos = (
                    randint(0, self.width),
                    randint(self.borders["top"], self.horizon_line),
                )
                surf = choice(self.small_clouds)
                Cloud(pos, surf, self)

    def cameraConstaint(self):
        # Horizontal
        self.offset.x = (
            self.offset.x
            if self.offset.x < self.borders["left"]
            else self.borders["left"]
        )
        self.offset.x = (
            self.offset.x
            if self.offset.x > self.borders["right"]
            else self.borders["right"]
        )
        # Vertical
        self.offset.y = (
            self.offset.y
            if self.offset.y < self.borders["top"]
            else self.borders["top"]
        )
        self.offset.y = (
            self.offset.y
            if self.offset.y > self.borders["bottom"]
            else self.borders["bottom"]
        )

    def updateBorders(self):
        self.win_size = pygame.display.get_window_size()
        self.borders["right"] = -self.width + self.win_size[0]
        self.borders["bottom"] = -self.height + self.win_size[1]

    def drawSky(self):
        self.display.fill("#ddc6a1")
        horizon_pos = self.horizon_line + self.offset.y

        sea_rect = pygame.FRect(
            (0, horizon_pos), (self.win_size[0], self.win_size[1] - horizon_pos)
        )
        pygame.draw.rect(self.display, "#92a9ce", sea_rect)

        pygame.draw.line(
            self.display,
            "#f5f1de",
            (0, horizon_pos),
            (self.win_size[0], horizon_pos),
            4,
        )

    def drawLargeCloud(self, dt):
        self.large_cloud_x += self.large_cloud_speed * self.cloud_direction * dt
        if self.large_cloud_x <= -self.large_cloud_width:
            self.large_cloud_x = 0
        for cloud in range(self.large_cloud_tiles):
            x = self.large_cloud_x + cloud * self.large_cloud_width + self.offset.x
            y = self.horizon_line - self.large_cloud_height - 100 + self.offset.y
            self.display.blit(self.large_cloud, (x, y))

    def createCloud(self):
        pos = (
            randint(self.width, self.width + 200),
            randint(
                -self.borders["top"], max(0, int(self.horizon_line + self.offset.y))
            ),
        )
        surf = choice(self.small_clouds)
        Cloud(pos, surf, self)

    def draw(self, target_pos, dt):
        self.updateBorders()
        self.offset.x = -(target_pos[0] - self.win_size[0] / 2)
        self.offset.y = -(target_pos[1] - self.win_size[1] / 2)
        self.cameraConstaint()

        if self.sky:
            self.new_cloud.update()
            self.drawSky()
            self.drawLargeCloud(dt)

        for sprite in sorted(self, key=lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display.blit(sprite.image, offset_pos)
