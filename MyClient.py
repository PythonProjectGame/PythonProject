import pygame
from MyNetwork import Network  # noqa: F401
from MyPlayer import Player

width = 500
height = 500
bg_colour = "White"
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def wallLimit(player):
    if player.rect.left <= 0:
        player.rect.left = 0
    if player.rect.right >= 500 - player.width:
        player.rect.right = 500 - player.width
    if player.rect.top <= 0:
        player.rect.top = 0
    if player.rect.bottom >= 500 - player.height:
        player.rect.bottom = 500 - player.height


p = Player((255, 0, 0), 100, 10)

all_sprites = pygame.sprite.Group()
all_sprites.add(p)

enemies = pygame.sprite.Group()

a = Player((0, 0, 0), 100, 10)
a.rect.left = 100
enemies.add(a)
all_sprites.add(a)


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if pygame.sprite.spritecollideany(p, enemies):
            p.kill()
            
        p.move()
        wallLimit(p)

        all_sprites.update()
        win.fill("white")
        all_sprites.draw(win)
        pygame.display.flip()

        clock.tick(60)


main()
