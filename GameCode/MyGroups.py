import pygame
from pygame import Vector2 as vector
from GameSettings import WIN_WIDTH, WIN_HEIGHT, TILE_SIZE
from MySprites import Sprite


class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, clouds, horizon_line, bg_tile=None, top_limit=0):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.offset = vector()
        self.width = width * TILE_SIZE
        self.height = height * TILE_SIZE
        self.borders = {
            "left": 0,
            "right": -self.width + WIN_WIDTH,
            "top": top_limit,
            "bottom": -self.height + WIN_HEIGHT,
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
            self.small_couds = clouds["small"]

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
        
        sea_rect = pygame.FRect((0, horizon_pos), (self.win_size[0], self.win_size[1] - horizon_pos))
        pygame.draw.rect(self.display, "#92a9ce", sea_rect)
        
        pygame.draw.line(self.display, "#f5f1de", (0, horizon_pos), (self.win_size[0], horizon_pos), 4)

    def draw(self, target_pos):
        self.updateBorders()
        self.offset.x = -(target_pos[0] - self.win_size[0] / 2)
        self.offset.y = -(target_pos[1] - self.win_size[1] / 2)
        self.cameraConstaint()

        if self.sky:
            self.drawSky()

        for sprite in sorted(self, key=lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display.blit(sprite.image, offset_pos)
