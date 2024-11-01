import pygame
from pygame.math import Vector2 as vector
from pygame.transform import flip
from math import sin
from GameSettings import TILE_SIZE, Z_LAYERS, ANIMATION_SPEED
from MyTimer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple,
        surf,
        groups: [pygame.sprite.Group],
        collision_sprites: [pygame.sprite.Sprite],
        semicollision_sprites: [pygame.sprite.Sprite],
        frames,
        data
    ) -> None:
        # General Setup
        super().__init__(groups)
        self.z = Z_LAYERS["main"]
        self.data = data

        # Image
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = "idle", True
        self.image = self.frames[self.state][self.frame_index]

        # Rects
        self.rect = self.image.get_frect(topleft=pos - vector(20, 20))
        self.hitbox = self.rect.inflate(-76, -36)  # -41, -24
        self.old_rect = self.hitbox.copy()

        # Movement values
        self.direction = vector()
        self.speed = TILE_SIZE * 15
        self.reg_speed = self.speed
        self.shift_speed = self.speed / 3
        self.gravity = 1300
        self.jump = False
        self.jump_height = TILE_SIZE * 20
        self.attacking = False

        # Collisions
        self.collision_sprites = collision_sprites
        self.semicollision_sprites = semicollision_sprites
        self.on_surface = {"floor": False, "left": False, "right": False}
        self.platform = None

        # Timer
        self.timers = {
            "wall jump": Timer(100),
            "wall slide block": Timer(250),
            "platform skip": Timer(100),
            "attack block": Timer(500),
            "hit": Timer(400),
        }

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

        if not self.timers["wall jump"].active:
            if keys[pygame.K_RIGHT] | keys[pygame.K_d]:
                input_vector.x += 1
                self.facing_right = True
                
            if keys[pygame.K_LEFT] | keys[pygame.K_a]:
                input_vector.x -= 1
                self.facing_right = False
                
            if keys[pygame.K_DOWN] | keys[pygame.K_s]:
                self.timers["platform skip"].activate()
            
            if keys[pygame.K_w]:
                self.attack()
            self.direction.x = (
                input_vector.normalize().x if input_vector.x else input_vector.x
            )

        if keys[pygame.K_SPACE]:
            self.jump = True

        if keys[pygame.K_LSHIFT]:
            self.speed = self.shift_speed
        else:
            self.speed = self.reg_speed

    def attack(self):
        if not self.timers["attack block"].active:
            self.attacking = True
            self.frame_index = 0
            self.timers["attack block"].activate()

    def move(self, dt: float) -> None:
        # Horizontal
        self.hitbox.x += self.direction.x * self.speed * dt
        self.collision("Horizontal")

        # Vertical
        if (
            not self.on_surface["floor"]
            and any((self.on_surface["left"], self.on_surface["right"]))
            and not self.timers["wall slide block"].active
        ):
            self.direction.y = 0
            self.hitbox.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.hitbox.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt

        if self.jump:
            if self.on_surface["floor"]:
                self.direction.y = -self.jump_height
                self.timers["wall slide block"].activate()
                self.hitbox.bottom -= 1
            elif (
                any((self.on_surface["left"], self.on_surface["right"]))
                and not self.timers["wall slide block"].active
            ):
                self.timers["wall jump"].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface["left"] else -1
            self.jump = False

        self.collision("Vertical")
        self.semiCollision()
        self.rect.center = self.hitbox.center

    def platformMove(self, dt):
        if self.platform is not None:
            self.hitbox.topleft += self.platform.direction * self.platform.speed * dt

    # Checks contacts between all( surfaces
    def checkContact(self):
        floor_rect = pygame.Rect(self.hitbox.bottomleft, (self.hitbox.width, 1))
        left_rect = pygame.Rect(
            self.hitbox.topleft + vector(-1, self.hitbox.height / 4),
            (1, self.hitbox.height / 2),
        )
        right_rect = pygame.Rect(
            self.hitbox.topright + vector(0, self.hitbox.height / 4),
            (1, self.hitbox.height / 2),
        )
        collision_rects = [sprite.rect for sprite in self.collision_sprites]
        semicollision_rects = [sprite.rect for sprite in self.semicollision_sprites]

        # Collisions
        self.on_surface["floor"] = (
            True
            if floor_rect.collidelist(collision_rects) >= 0
            or floor_rect.collidelist(semicollision_rects) >= 0
            and self.direction.y >= 0
            else False
        )
        self.on_surface["left"] = (
            True if left_rect.collidelist(collision_rects) >= 0 else False
        )
        self.on_surface["right"] = (
            True if right_rect.collidelist(collision_rects) >= 0 else False
        )

        # Moving Collisions
        self.platform = None
        sprites = (
            self.collision_sprites.sprites() + self.semicollision_sprites.sprites()
        )
        for sprite in [sprite for sprite in sprites if hasattr(sprite, "moving")]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite

    def collision(self, axis: str) -> None:
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if axis == "Horizontal":
                    # Left
                    if all(
                        (
                            self.hitbox.left <= sprite.rect.right,
                            int(self.old_rect.left) >= int(sprite.old_rect.right),
                        )
                    ):
                        self.hitbox.left = sprite.rect.right

                    # Right
                    if all(
                        (
                            self.hitbox.right >= sprite.rect.left,
                            int(self.old_rect.right) <= int(sprite.old_rect.left),
                        )
                    ):
                        self.hitbox.right = sprite.rect.left

                else:  # Vertical
                    # Top
                    if all(
                        (
                            self.hitbox.top <= sprite.rect.bottom,
                            int(self.old_rect.top) >= int(sprite.old_rect.bottom),
                        )
                    ):
                        self.hitbox.top = sprite.rect.bottom
                        if hasattr(sprite, "moving"):
                            self.hitbox.top += 6

                    # Bottom
                    if all(
                        (
                            self.hitbox.bottom >= sprite.rect.top,
                            int(self.old_rect.bottom) <= int(sprite.old_rect.top),
                        )
                    ):
                        self.hitbox.bottom = sprite.rect.top

                    self.direction.y = 0

    def semiCollision(self):
        if not self.timers["platform skip"].active:
            for sprite in self.semicollision_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if all(
                        (
                            [
                                self.hitbox.bottom >= sprite.rect.top,
                                int(self.old_rect.bottom) <= int(sprite.old_rect.top),
                            ]
                        )
                    ):
                        self.hitbox.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0

    def updateTimers(self):
        for timer in self.timers.values():
            timer.update()

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.state == "attack" and self.frame_index >= len(self.frames[self.state]):
            self.state = "idle"
        
        self.image = self.frames[self.state][
            int(self.frame_index % len(self.frames[self.state]))
        ]
        self.image = self.image if self.facing_right else flip(self.image, True, False)
        
        if self.attacking and self.frame_index > len(self.frames[self.state]):
            self.attacking = False

    def getState(self):
        if self.on_surface["floor"]:
            if self.attacking:
                self.state = "attack"
            else:
                self.state = "idle" if self.direction.x == 0 else "run"
        else:
            if self.attacking:
                self.state = "air_attack"
            else:
                if any((self.on_surface["left"], self.on_surface["right"])):
                    self.state = "wall"
                else:
                    self.state = "jump" if self.direction.y < 0 else "fall"

    def getDamage(self):
        if not self.timers["hit"].active:
            self.data.health -= 1
            self.timers["hit"].activate()
    
    def flicker(self):
        if self.timers["hit"].active and sin(pygame.time.get_ticks() * 100) > 0:
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey("black")
            self.image = white_surf

    def update(self, dt: float) -> None:
        self.old_rect = self.hitbox.copy()
        self.updateTimers()

        self.input()
        self.move(dt)
        self.platformMove(dt)
        self.checkContact()

        self.getState()
        self.animate(dt)
        self.flicker()
