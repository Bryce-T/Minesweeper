"""
Minesweeper by Bryce Taylor
- Coded in 2021/2022
- Created using Pygame
- Concept is based off the popular game Minesweeper

"""

import pygame

from game_board import *
from settings import *

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bomb_image = pygame.image.load("sprites/bomb.png")
    pygame.display.set_caption("Minesweeper")
    pygame.display.set_icon(bomb_image)

    text_obj = pygame.freetype.Font("font/FreeSansBold.ttf", 35)
    text_obj2 = pygame.freetype.Font("font/FreeSansBold.ttf", 20)

    clock = pygame.time.Clock()


    board = GameBoard(10, 10, 0.16)
    #print()
    #board.printBoard()
    #board.revealAll()

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if board.game_status == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                mouseX , mouseY = pygame.mouse.get_pos()
                if (0 <= mouseX < board.getWidth() * TILE_WIDTH and 0 <= mouseY < board.getHeight() * TILE_HEIGHT):
                    if event.button == 1: # left click
                        board.sendClick(mouseX, mouseY)
                    if event.button == 3: # right click
                        board.sendRightClick(mouseX, mouseY)

                    board.check_state()

        screen.fill(WHITE)

        board.draw(screen, text_obj, text_obj2)

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":
    main()
