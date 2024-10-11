import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill("White")
        self.image.set_colorkey("Blue")
        self.vel = 3
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.left -= self.vel

        if keys[pygame.K_RIGHT]:
            self.rect.right += self.vel

        if keys[pygame.K_UP]:
            self.rect.top -= self.vel

        if keys[pygame.K_DOWN]:
            self.rect.bottom += self.vel

        if keys[pygame.K_LSHIFT]:
            self.vel = 1
        else:
            self.vel = 3

        self.update()
