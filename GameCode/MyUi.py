import pygame
from MySprites import AnimatedSprite
from random import randint
from GameSettings import ANIMATION_SPEED
from MyTimer import Timer

class UI:
    def __init__(self, font, frames):
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

    def createHearts(self, amount):
        for sprite in self.sprites:
            sprite.kill()
            
        for heart in range(amount):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x, y), self.heart_frames, self.sprites)
    
    def displayText(self):
        if self.coin_timer.active:
            text_surf = self.font.render(str(self.coin_amount), False, "#33323d")
            tect_rect = text_surf.get_frect(topleft=(16, 34))
            self.display.blit(text_surf, tect_rect)
            
            coin_rect = self.coin_surf.get_frect(center=tect_rect.bottomleft)
            self.display.blit(self.coin_surf, coin_rect)
    
    def showCoins(self, amount):
        self.coin_amount = amount
        self.coin_timer.activate()
        
    def update(self, dt):
        self.coin_timer.update()
        self.sprites.update(dt)
        self.sprites.draw(self.display)
        self.displayText()


class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False
    
    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0
            self.image = self.frames[0]
    
    def update(self, dt):
        if self.active:
            self.animate(dt)
        else:
            if randint(0, 1000) == 1:
                self.active = True
        
