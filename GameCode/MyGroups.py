import pygame
from pygame import Vector2 as vector
from GameSettings import WIN_WIDTH, WIN_HEIGHT

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        
        self.offset = vector()
    
    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WIN_WIDTH/2)
        self.offset.y = -(target_pos[1] - WIN_HEIGHT/2)
        
        for sprite in sorted(self, key=lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display.blit(sprite.image, offset_pos)