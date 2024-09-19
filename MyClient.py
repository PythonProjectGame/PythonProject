import pygame
from MyNetwork import Network  # noqa: F401
from MyPlayer import Player  # noqa: F401

width = 500
height = 500
bg_colour = "#999966"
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, player):
    win.fill(bg_colour)
    player.draw(win)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

main()