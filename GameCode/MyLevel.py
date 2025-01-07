import pygame
from pygame import Vector2 as vector
from random import uniform
import json
from MySprites import (
    Sprite,
    AnimatedSprite,
    MovingSprite,
    Spike,
    Item,
    ParticleEffectSprite,
)
from MyEnemies import Tooth, Shell, Pearl
from MyPlayer import Player
from MyGroups import AllSprites


class Level:
    """
    A class for handling the level properties and behavior.

    :param tmx_map: The Tiled map object.
    :param level_frames: The level frames dictionary.
    :param data: The data object.
    """

    def __init__(
        self,
        tmx_map,
        level_frames: dict[str, list[pygame.Surface]],
        audio: dict[str, pygame.mixer.Sound],
        data,
    ) -> None:
        """
        Initialize the level.

        :param tmx_map: The Tiled map object.
        :param level_frames: The level frames dictionary.
        :param audio: The audio dictionary.
        :param data: The data object.
        :type data: Data
        """

        # Getting Game Settings
        with open("GameCode/GameSettings.json", "r") as f:
            x = f.read()
            self.settings = json.loads(x)

        # The display surface.
        self.display: pygame.Surface = pygame.display.get_surface()

        # The data object.
        self.data: Data = data

        # Level Data
        # The width and height of the level in pixels.
        self.level_width: int = tmx_map.width * self.settings["TILE_SIZE"]
        self.level_height: int = tmx_map.height * self.settings["TILE_SIZE"]

        # Level properties from the Tiled map.
        tmx_level_properties = tmx_map.get_layer_by_name("Data")[0].properties

        # The background tile.
        if tmx_level_properties["bg"]:
            bg_tile: pygame.Surface = level_frames["bg_tiles"][
                tmx_level_properties["bg"]
            ]
        else:
            # No background tile.
            bg_tile: pygame.Surface = None

        # Sprite Groups
        # The main sprite group.
        self.all_sprites: AllSprites = AllSprites(
            tmx_map.width,
            tmx_map.height,
            {
                "large": level_frames["cloud_large"],
                "small": level_frames["cloud_small"],
            },
            tmx_level_properties["horizon_line"],
            bg_tile,
            tmx_level_properties["top_limit"],
        )

        # The groups.
        # The collision sprite group.
        self.collision_sprites = pygame.sprite.Group()
        # The semicollision sprite group.
        self.semicollision_sprites = pygame.sprite.Group()
        # The damage sprite group.
        self.damage_sprites = pygame.sprite.Group()
        # The tooth sprite group.
        self.tooth_sprites = pygame.sprite.Group()
        # The pearl sprite group.
        self.pearl_sprites = pygame.sprite.Group()
        # The item sprite group.
        self.item_sprites = pygame.sprite.Group()

        # Surfaces
        # Set up the level.
        self.setup(tmx_map, level_frames, audio)

        # The pearl surface.
        self.pearl_surf: pygame.Surface = level_frames["pearl"]
        # The particle surface.
        self.particle_surf: pygame.Surface = level_frames["particle"]

        # Sound
        # The coin sound.
        self.coin_sound = audio["coin"]
        # The coin sound volume.
        self.coin_sound.set_volume(
            0.1
            * self.settings["SOUND"]["SOUND_VOLUME"]
            * self.settings["SOUND"]["SFX_VOLUME"]
        )
        # The pearl sound.
        self.pearl_sound = audio["pearl"]
        self.pearl_sound.set_volume(
            1
            * self.settings["SOUND"]["SOUND_VOLUME"]
            * self.settings["SOUND"]["SFX_VOLUME"]
        )
        # The hit sound
        self.hit_sound = audio["hit"]
        # The hit sound volume.
        self.hit_sound.set_volume(
            0.5
            * self.settings["SOUND"]["SOUND_VOLUME"]
            * self.settings["SOUND"]["SFX_VOLUME"]
        )
        # The win sound.
        self.win_sound = audio["win"]
        # The win sound volume.
        self.win_sound.set_volume(
            0.1
            * self.settings["SOUND"]["SOUND_VOLUME"]
            * self.settings["SOUND"]["SFX_VOLUME"]
        )

    def setup(self, tmx_map, level_frames, audio):
        Z_LAYERS = self.settings["Z_LAYERS"]
        TILE_SIZE = self.settings["TILE_SIZE"]
        ANIMATION_SPEED = self.settings["ANIMATION_SPEED"]

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
                        z = Z_LAYERS["bg tiles"]
                    case _:
                        z = Z_LAYERS["main"]

                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        # BG extras
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
                    self.data,
                    attack_sound=audio["attack"],
                    jump_sound=audio["jump"],
                    damage_sound=audio["damage"],
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
            if obj.name == "flag":
                self.level_finish_rect = pygame.FRect((obj.x, obj.y), (5, obj.height))
        # Moving Objects
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == "spike":
                Spike(
                    (obj.x + obj.width / 2, obj.y + obj.height / 2),
                    level_frames["spike"],
                    (self.all_sprites, self.damage_sprites),
                    obj.properties["radius"],
                    obj.properties["speed"],
                    obj.properties["start_angle"],
                    obj.properties["end_angle"],
                )
                for i in range(0, obj.properties["radius"], 20):
                    Spike(
                        (obj.x + obj.width / 2, obj.y + obj.height / 2),
                        level_frames["spike_chain"],
                        (self.all_sprites),
                        i,
                        obj.properties["speed"],
                        obj.properties["start_angle"],
                        obj.properties["end_angle"],
                        z=Z_LAYERS["bg details"],
                    )

            else:
                frames = level_frames[obj.name]
                if obj.properties["platform"]:
                    groups = (self.all_sprites, self.semicollision_sprites)
                else:
                    groups = (self.all_sprites, self.damage_sprites)
                # Calculating movement direction
                if obj.width > obj.height:  # Horizontal
                    move_dir = "x"
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (
                        obj.x + obj.width,
                        obj.y + obj.height / 2,
                    )
                else:  # Vertical
                    move_dir = "y"
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)

                speed = obj.properties["speed"]
                MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed)

                if obj.name == "saw":
                    if move_dir == "x":
                        y = start_pos[1] - level_frames["saw_chain"].get_height() / 2
                        left, right = start_pos[0], end_pos[0]
                        for x in range(int(left), int(right), 20):
                            Sprite(
                                (x, y),
                                level_frames["saw_chain"],
                                self.all_sprites,
                                Z_LAYERS["bg details"],
                            )
                    else:
                        x = start_pos[0] - level_frames["saw_chain"].get_width() / 2
                        top, bottom = int(start_pos[1]), int(end_pos[1])
                        for y in range(top, bottom, 20):
                            Sprite(
                                (x, y),
                                level_frames["saw_chain"],
                                self.all_sprites,
                                Z_LAYERS["bg details"],
                            )

        # Enemies
        for obj in tmx_map.get_layer_by_name("Enemies"):
            if obj.name == "tooth":
                Tooth(
                    (obj.x, obj.y),
                    level_frames["tooth"],
                    (self.all_sprites, self.damage_sprites, self.tooth_sprites),
                    self.collision_sprites.sprites()
                    + self.semicollision_sprites.sprites(),
                )
            if obj.name == "shell":
                Shell(
                    (obj.x, obj.y),
                    level_frames["shell"],
                    (self.all_sprites, self.collision_sprites),
                    obj.properties["reverse"],
                    self.player,
                    self.create_pearl,
                )

        # Items
        for obj in tmx_map.get_layer_by_name("Items"):
            Item(
                obj.name,
                (obj.x, obj.y),
                level_frames["items"][obj.name],
                (self.all_sprites, self.item_sprites),
                self.data,
            )

    def create_pearl(self, pos, direction):
        Pearl(
            pos,
            (self.all_sprites, self.damage_sprites, self.pearl_sprites),
            self.pearl_surf,
            direction,
            150,
        )
        self.pearl_sound.play()

    def pearl_collision(self):
        for sprite in self.collision_sprites:
            surf = pygame.sprite.spritecollide(sprite, self.pearl_sprites, True)
            if surf:
                ParticleEffectSprite(
                    surf[0].rect.topleft + vector(-5, -5),
                    self.particle_surf,
                    self.all_sprites,
                )

    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.hit_rect.colliderect(self.player.hitbox):
                self.player.get_damage()
                if type(sprite) is Pearl:
                    ParticleEffectSprite(
                        sprite.rect.topleft + vector(-5, -5),
                        self.particle_surf,
                        self.all_sprites,
                    )
                    sprite.kill()

    def item_collision(self):
        for sprite in self.item_sprites:
            if sprite.hit_rect.colliderect(self.player.rect):
                sprite.activate()
                ParticleEffectSprite(
                    sprite.rect.topleft, self.particle_surf, self.all_sprites
                )
                self.coin_sound.play()
                sprite.kill()

    def attack_collision(self):
        for target in self.pearl_sprites.sprites() + self.tooth_sprites.sprites():
            facing_target = (
                self.player.rect.centerx < target.rect.centerx
                and self.player.facing_right
                or self.player.rect.centerx > target.rect.centerx
                and not self.player.facing_right
            )

            if (
                target.rect.colliderect(self.player.rect)
                and self.player.attacking
                and facing_target
            ):
                target.reverse()
                self.hit_sound.play()

    def check_constraint(self):
        # Left Right Constain
        if self.player.hitbox.left <= 0:
            self.player.hitbox.left = 0
        if self.player.hitbox.right >= self.level_width:
            self.player.hitbox.right = self.level_width

        # Bottom
        if self.player.hitbox.y >= self.level_height:
            self.data.dead = True

        # Success
        if self.player.hitbox.colliderect(self.level_finish_rect):
            pygame.mixer.music.stop()
            self.win_sound.play()

    def run(self, dt):
        self.all_sprites.update(dt)

        self.pearl_collision()
        self.hit_collision()
        self.item_collision()
        self.attack_collision()

        self.check_constraint()

        self.all_sprites.draw(self.player.hitbox.center, dt)
