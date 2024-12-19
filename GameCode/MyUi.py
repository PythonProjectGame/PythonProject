import pygame
from MySprites import AnimatedSprite
from random import randint
from GameSettings import *
from MyTimer import Timer


class UI:
    """A class for managing the user interface."""

    def __init__(self, font, frames):
        """Initialize the user interface.

        :param font: The font to use for the user interface.
        :param frames: The frames for the heart sprites.
        """
        self.display = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font

        # Health
        self.heart_frames = frames["heart"]
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 5

        # Coins
        self.coin_surf = frames["coin"]
        self.coin_amount = 0
        self.coin_timer = Timer(1000)

    def create_hearts(self, amount):
        """Create the specified number of hearts in the upper left of the screen.

        :param amount: The number of hearts to create.
        """
        for sprite in self.sprites:
            sprite.kill()

        for heart in range(amount):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x, y), self.heart_frames, self.sprites)

    def display_text(self):
        """Display the number of coins currently collected."""

        if self.coin_timer.active:
            text_surf = self.font.render(str(self.coin_amount), False, "#33323d")
            tect_rect = text_surf.get_frect(topleft=(16, 34))
            self.display.blit(text_surf, tect_rect)

            coin_rect = self.coin_surf.get_frect(center=tect_rect.bottomleft)
            self.display.blit(self.coin_surf, coin_rect)

    def show_coins(self, amount):
        """Show the specified number of coins in the upper right of the screen.

        :param amount: The number of coins to show.
        """
        self.coin_amount = amount
        self.coin_timer.activate()

    def update(self, dt):
        """Update the user interface.

        :param dt: The time since the last update.
        """
        self.coin_timer.update()
        self.sprites.update(dt)
        self.sprites.draw(self.display)
        self.display_text()


class Heart(AnimatedSprite):
    """The heart in the upper left of the screen that sometimes beats."""

    def __init__(self, pos, frames, groups):
        """Initialize the heart.

        :param pos: The position of the heart.
        :param frames: The frames of the heart.
        :param groups: The groups the heart should be in.
        """
        super().__init__(pos, frames, groups)
        self.active = False

    def animate(self, dt):
        """Animate the heart.

        :param dt: The time passed since the last frame.
        """
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0
            self.image = self.frames[0]

    def update(self, dt):
        """Update the heart.

        :param dt: The time passed since the last frame.
        """
        if self.active:
            self.animate(dt)
        else:
            # Sometimes the heart starts beating
            if randint(0, 1000) == 1:
                self.active = True
