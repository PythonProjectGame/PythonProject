import pygame
from pygame import Vector2 as vector
from random import uniform
from MySprites import Sprite, AnimatedSprite, MovingSprite
from MyPlayer import Player
from GameSettings import TILE_SIZE, Z_LAYERS, ANIMATION_SPEED
from MyGroups import AllSprites


class Level:
    def __init__(self, tmx_map, level_frames) -> None:
        self.display = pygame.display.get_surface()

        # Sprite Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semicollision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        # Tiles

        for layer in ["BG", "Terrain", "FG", "Platforms"]:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]

                if layer == "Terrain":
                    groups.append(self.collision_sprites)
                if layer == "Platforms":
                    groups.append(self.semicollision_sprites)

                match layer:
                    case "BG":
                        z = Z_LAYERS["bg tiles"]
                    case "FG":
                        z = Z_LAYERS["fg"]
                    case _:
                        z = Z_LAYERS["main"]

                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        for obj in tmx_map.get_layer_by_name("BG Details"):
            if obj.name == "static":
                Sprite(
                    (obj.x, obj.y),
                    obj.image,
                    self.all_sprites,
                    z=Z_LAYERS["bg details"],
                )
            else:
                AnimatedSprite(
                    (obj.x, obj.y),
                    level_frames[obj.name],
                    self.all_sprites,
                    Z_LAYERS["bg details"],
                )
                if obj.name == "candle":
                    AnimatedSprite(
                        (obj.x, obj.y) + vector(-20, -20),
                        level_frames["candle_light"],
                        self.all_sprites,
                        Z_LAYERS["bg details"],
                    )

        # Objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "Player":
                self.player = Player(
                    (obj.x, obj.y),
                    surf,
                    self.all_sprites,
                    self.collision_sprites,
                    self.semicollision_sprites,
                    level_frames["player"],
                )
            else:
                if obj.name in ["barrel", "crate"]:
                    Sprite(
                        (obj.x, obj.y),
                        obj.image,
                        (self.all_sprites, self.collision_sprites),
                    )
                else:
                    # Frames
                    frames = (
                        level_frames[obj.name]
                        if "palm" not in obj.name
                        else level_frames["palms"][obj.name]
                    )
                    if obj.name == "floor_spike" and obj.properties["inverted"]:
                        frames = [
                            pygame.transform.flip(frame, False, True)
                            for frame in frames
                        ]

                    # Groups
                    groups = [self.all_sprites]
                    if obj.name in ["palm_small", "palm_large"]:
                        groups.append(self.semicollision_sprites)
                    if obj.name in ["saw", "floor_spike"]:
                        groups.append(self.damage_sprites)

                    # Z Index
                    z = (
                        Z_LAYERS["main"]
                        if "bg" not in obj.name
                        else Z_LAYERS["bg details"]
                    )

                    # Animation Speed
                    animation_speed = (
                        ANIMATION_SPEED
                        if "palm" not in obj.name
                        else ANIMATION_SPEED + uniform(-2, 2)
                    )

                    AnimatedSprite((obj.x, obj.y), frames, groups, z, animation_speed)

        # Moving Objects
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == "helicopter":
                # Calculating movement direction
                if obj.width > obj.height:  # Horizontal
                    move_dir = "x"
                    start_pos = (
                        obj.x,
                        obj.y + obj.height / 2,
                    )
                    end_pos = (
                        obj.x + obj.width,
                        obj.y + obj.height / 2,
                    )
                else:  # Vertical
                    move_dir = "y"
                    start_pos = (
                        obj.x + obj.width / 2,
                        obj.y,
                    )
                    end_pos = (
                        obj.x + obj.width / 2,
                        obj.y + obj.height,
                    )
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
        self.display.fill("black")
        self.all_sprites.draw(self.player.hitbox.center)
