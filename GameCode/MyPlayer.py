import pygame
from pygame.math import Vector2 as vector
from pygame.transform import flip
from math import sin
from GameSettings import *
from MyTimer import Timer


class Player(pygame.sprite.Sprite):
    """
    A class for handling the player sprite's properties and behavior.

    :param pos: The player's initial position.
    :param surf: The player's initial surface.
    :param groups: The groups the player belongs to.
    :param collision_sprites: The sprites that the player can collide with.
    :param semicollision_sprites: The sprites that the player can semicollide with.
    :param frames: The frames used for the player's animation.
    :param data: The player's data.
    """

    def __init__(
        self,
        pos: tuple,
        surf,
        groups: [pygame.sprite.Group],
        collision_sprites: [pygame.sprite.Sprite],
        semicollision_sprites: [pygame.sprite.Sprite],
        frames,
        data,
    ) -> None:
        # General Setup
        """
        Initialize the player sprite.
        """
        super().__init__(groups)
        self.z = Z_LAYERS["main"]
        self.data = data

        # Image
        """
        The player's image.
        """
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = "idle", True
        self.image = self.frames[self.state][self.frame_index]

        # Rects
        """
        The player's rectangles.
        """
        self.rect = self.image.get_frect(topleft=pos - vector(20, 20))
        self.hitbox = self.rect.inflate(-76, -36)  # -41, -24
        self.old_rect = self.hitbox.copy()

        # Movement values
        """
        The player's movement values.
        """
        self.direction = vector()
        self.speed = TILE_SIZE * 10
        self.reg_speed = self.speed
        self.shift_speed = self.speed / 3
        self.gravity = 1300
        self.jump = False
        self.jump_height = TILE_SIZE * 20
        self.attacking = False

        # Collisions
        """
        The player's collisions.
        """
        self.collision_sprites = collision_sprites
        self.semicollision_sprites = semicollision_sprites
        self.on_surface = {"floor": False, "left": False, "right": False}
        self.platform = None

        # Timer
        """
        The player's timer.
        """
        self.timers = {
            "wall jump": Timer(100),
            "wall slide block": Timer(250),
            "platform skip": Timer(100),
            "attack block": Timer(500),
            "hit": Timer(400),
        }

    def input(self) -> None:
        """
        Handle the player's input.

        :return: None
        """
        # Get the current state of all keyboard buttons
        keys = pygame.key.get_pressed()
        # Initialize the input vector to zero
        input_vector = vector(0, 0)

        # Check if the player is not currently in the middle of a wall jump
        if not self.timers["wall jump"].active:
            # Check for horizontal movement
            if keys[pygame.K_RIGHT] | keys[pygame.K_d]:
                # Move the input vector right
                input_vector.x += 1
                # Set the player's facing direction to right
                self.facing_right = True

            if keys[pygame.K_LEFT] | keys[pygame.K_a]:
                # Move the input vector left
                input_vector.x -= 1
                # Set the player's facing direction to left
                self.facing_right = False

            # Check for vertical movement
            if keys[pygame.K_DOWN] | keys[pygame.K_s]:
                # Activate the platform skip timer
                self.timers["platform skip"].activate()

            # Check for attack
            if keys[pygame.K_w]:
                # Call the attack method
                self.attack()

            # Calculate the final direction vector
            self.direction.x = (
                input_vector.normalize().x if input_vector.x else input_vector.x
            )

        # Check for jumping
        if keys[pygame.K_SPACE]:
            # Set the jump flag to true
            self.jump = True

        # Check for shift
        if keys[pygame.K_LSHIFT]:
            # Set the speed to the shift speed
            self.speed = self.shift_speed
        else:
            # Set the speed to the regular speed
            self.speed = self.reg_speed

    def attack(self) -> None:
        """
        Initiates the player's attack if not currently on attack cooldown.

        :return: None
        """
        if not self.timers["attack block"].active:
            # Set the player to an attacking state
            self.attacking: bool = True
            # Reset the animation frame index
            self.frame_index: int = 0
            # Activate the attack cooldown timer
            self.timers["attack block"].activate()

    def move(self, dt: float) -> None:
        """
        Move the player based on input and physics.

        :param dt: The time passed since the last frame.
        :return: None
        """
        # Horizontal
        self.hitbox.x += self.direction.x * self.speed * dt
        self.collision("Horizontal")

        # Vertical
        if (
            not self.on_surface["floor"]
            and any((self.on_surface["left"], self.on_surface["right"]))
            and not self.timers["wall slide block"].active
        ):
            # If the player is on a wall, apply gravity
            self.direction.y = 0
            self.hitbox.y += self.gravity / 10 * dt
        else:
            # Apply gravity and move the player
            self.direction.y += self.gravity / 2 * dt
            self.hitbox.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt

        if self.jump:
            if self.on_surface["floor"]:
                # If the player is on the ground, apply the jump height
                self.direction.y = -self.jump_height
                self.timers["wall slide block"].activate()
                self.hitbox.bottom -= 1
            elif (
                any((self.on_surface["left"], self.on_surface["right"]))
                and not self.timers["wall slide block"].active
            ):
                # If the player is on a wall, apply the wall jump height
                self.timers["wall jump"].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface["left"] else -1
            self.jump = False

        self.collision("Vertical")
        self.semi_collision()
        self.rect.center = self.hitbox.center

    def platform_move(self, dt: float) -> None:
        """
        Move the player horizontally based on the platform's speed and direction.

        :param dt: The time passed since the last frame.
        :return: None
        """
        if self.platform is not None:
            # Move the player's hitbox horizontally by the platform's speed and direction
            self.hitbox.topleft += self.platform.direction * self.platform.speed * dt

    def check_contact(self):
        """
        Check if the player is in contact with the floor or a wall.

        :return: None
        """
        # Create a rectangle for the floor
        floor_rect = pygame.Rect(self.hitbox.bottomleft, (self.hitbox.width, 1))
        # Create rectangles for the left and right walls
        left_rect = pygame.Rect(
            self.hitbox.topleft + vector(-1, self.hitbox.height / 4),
            (1, self.hitbox.height / 2),
        )
        right_rect = pygame.Rect(
            self.hitbox.topright + vector(0, self.hitbox.height / 4),
            (1, self.hitbox.height / 2),
        )
        # Get the collision rectangles from the collision sprites and semicollision sprites
        collision_rects = [sprite.rect for sprite in self.collision_sprites]
        semicollision_rects = [sprite.rect for sprite in self.semicollision_sprites]

        # Check for collisions with the floor
        self.on_surface["floor"] = (
            True
            if floor_rect.collidelist(collision_rects) >= 0
            or floor_rect.collidelist(semicollision_rects) >= 0
            and self.direction.y >= 0
            else False
        )
        # Check for collisions with the left wall
        self.on_surface["left"] = (
            True if left_rect.collidelist(collision_rects) >= 0 else False
        )
        # Check for collisions with the right wall
        self.on_surface["right"] = (
            True if right_rect.collidelist(collision_rects) >= 0 else False
        )

        # Check for moving collisions
        self.platform = None
        sprites = (
            self.collision_sprites.sprites() + self.semicollision_sprites.sprites()
        )
        for sprite in [sprite for sprite in sprites if hasattr(sprite, "moving")]:
            # Check if the sprite's rectangle collides with the floor rectangle
            if sprite.rect.colliderect(floor_rect):
                # Set the platform to the sprite
                self.platform = sprite

    def collision(self, axis: str) -> None:
        """
        Check for collisions with the sprites in the collision_sprites group.

        :param axis: The axis to check for collisions on. This can be either "Horizontal" or "Vertical".
        :return: None
        """
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                # Check for horizontal collisions
                if axis == "Horizontal":
                    # Check for the player hitting the sprite from the left
                    if all(
                        (
                            self.hitbox.left <= sprite.rect.right,
                            int(self.old_rect.left) >= int(sprite.old_rect.right),
                        )
                    ):
                        # Move the player to the right of the sprite
                        self.hitbox.left = sprite.rect.right

                    # Check for the player hitting the sprite from the right
                    if all(
                        (
                            self.hitbox.right >= sprite.rect.left,
                            int(self.old_rect.right) <= int(sprite.old_rect.left),
                        )
                    ):
                        # Move the player to the left of the sprite
                        self.hitbox.right = sprite.rect.left

                # Check for vertical collisions
                else:
                    # Check for the player hitting the sprite from the top
                    if all(
                        (
                            self.hitbox.top <= sprite.rect.bottom,
                            int(self.old_rect.top) >= int(sprite.old_rect.bottom),
                        )
                    ):
                        # Move the player to the bottom of the sprite
                        self.hitbox.top = sprite.rect.bottom
                        # If the sprite is moving, move the player down by 6 units
                        if hasattr(sprite, "moving"):
                            self.hitbox.top += 6

                    # Check for the player hitting the sprite from the bottom
                    if all(
                        (
                            self.hitbox.bottom >= sprite.rect.top,
                            int(self.old_rect.bottom) <= int(sprite.old_rect.top),
                        )
                    ):
                        # Move the player to the top of the sprite
                        self.hitbox.bottom = sprite.rect.top

                    # Set the vertical direction to 0
                    self.direction.y = 0

    def semi_collision(self):
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

    def update_timers(self):
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

    def get_state(self):
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

    def get_damage(self):
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
        self.update_timers()

        self.input()
        self.move(dt)
        self.platform_move(dt)
        self.check_contact()

        self.get_state()
        self.animate(dt)
        self.flicker()
