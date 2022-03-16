import math
import random
import pygame
import time

from settings import *

class Tile:
    def __init__(self, row, col, value = 0, isBomb = False, isRevealed = False, isFlagged = False):
        """
        Create new tile with specified row and column on board
        value determines the number displayed by the tile
        (-1 is bomb, 0 has no surrounding bombs, 1 has 1 surrounding bomb, etc.)
        isBomb tells whether the tile is a bomb
        isRevealed tells whether the tile has been revealed by the player
        """
        self.row = row
        self.col = col
        self.value = value
        self.isBomb = isBomb
        self.isRevealed = isRevealed
        self.isFlagged = False
        self.bomb_image = pygame.image.load("sprites/bomb.png")
        self.flag_image = pygame.image.load("sprites/flag.png")

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def getValue(self):
        return self.value

    def setValue(self, newValue):
        self.value = newValue

    def getBombState(self):
        return self.isBomb

    def setBombState(self, newValue):
        self.isBomb = newValue
        if self.isBomb:
            self.value = -1

    def getRevealedState(self):
        return self.isRevealed

    def setRevealedState(self, newValue):
        self.isRevealed = newValue

    def isExploded(self):
        """
        returns whether the tile is an exploded bomb, indicating that the game should end
        """
        if self.isBomb and self.isRevealed:
            return True
        return False

    def inRange(self, mx, my):
        if (self.col * TILE_WIDTH < mx < self.col * TILE_WIDTH + TILE_WIDTH and
            self.row * TILE_HEIGHT < my < self.row * TILE_HEIGHT + TILE_HEIGHT):
            return True
        return False

    def sendClick(self):
        self.isRevealed = True
        if self.isFlagged:
            self.isFlagged == False
            return 1
        return 0

    def sendRightClick(self):
        if self.isRevealed == False:
            if self.isFlagged == False:
                self.isFlagged = True
                return 1
            else:
                self.isFlagged = False
                return -1
        return 0

    def draw(self, surface, text_obj):
        if (self.isRevealed == False and self.isFlagged == False):
            pygame.draw.rect(surface, UNREVEALED, (self.col * TILE_WIDTH, self.row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
        pygame.draw.rect(surface, BLACK, (self.col * TILE_WIDTH, self.row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 2)
        if (self.isRevealed):
            if (self.value == 1):
                text_obj.render_to(surface, (self.col * TILE_WIDTH + TILE_WIDTH * 0.38,
                                    self.row * TILE_HEIGHT + TILE_HEIGHT * 0.27), str(self.value), COL1)
            elif (self.value == 2):
                text_obj.render_to(surface, (self.col * TILE_WIDTH + TILE_WIDTH * 0.35,
                                    self.row * TILE_HEIGHT + TILE_HEIGHT * 0.27), str(self.value), COL2)
            elif (self.value == 3):
                text_obj.render_to(surface, (self.col * TILE_WIDTH + TILE_WIDTH * 0.35,
                                    self.row * TILE_HEIGHT + TILE_HEIGHT * 0.27), str(self.value), COL3)
            elif (self.value == 4):
                text_obj.render_to(surface, (self.col * TILE_WIDTH + TILE_WIDTH * 0.33,
                                    self.row * TILE_HEIGHT + TILE_HEIGHT * 0.27), str(self.value), COL4)
            elif (self.value == 5):
                text_obj.render_to(surface, (self.col * TILE_WIDTH + TILE_WIDTH * 0.34,
                                    self.row * TILE_HEIGHT + TILE_HEIGHT * 0.27), str(self.value), COL5)
            elif (self.value == 6):
                text_obj.render_to(surface, (self.col * TILE_WIDTH + TILE_WIDTH * 0.35,
                                    self.row * TILE_HEIGHT + TILE_HEIGHT * 0.27), str(self.value), COL6)
            elif (self.value == 7):
                text_obj.render_to(surface, (self.col * TILE_WIDTH + TILE_WIDTH * 0.35,
                                    self.row * TILE_HEIGHT + TILE_HEIGHT * 0.27), str(self.value), COL7)
            elif (self.value == 8):
                text_obj.render_to(surface, (self.col * TILE_WIDTH + TILE_WIDTH * 0.32,
                                    self.row * TILE_HEIGHT + TILE_HEIGHT * 0.27), str(self.value), COL8)
            elif (self.value == -1):
                surface.blit(self.bomb_image, (self.col * TILE_WIDTH + TILE_WIDTH * 0.27,
                                                self.row * TILE_HEIGHT + TILE_HEIGHT * 0.2))
        elif (self.isFlagged):
            surface.blit(self.flag_image, (self.col * TILE_WIDTH + TILE_WIDTH * 0.1,
                                                self.row * TILE_HEIGHT + TILE_HEIGHT * 0.2))


class GameBoard:
    def __init__(self, boardWidth, boardHeight, difficulty):
        """
        Create a new board object width specified dimensions
        Contains a 2D array containing tiles
        boardHeight rows and boardWidth columns
        Difficulty setting is used to set the number of bombs on the board (% of board area)
        """
        self.width = boardWidth
        self.height = boardHeight
        self.difficulty = difficulty
        self.isFresh = True # Ensures that first click will be a "zero" tile
        self.generateNewBoard(difficulty)
        self.spots_visited = []
        self.flags_left = -1
        self.game_status = 0 # 0 = ongoing, 1 = win, 2 = loss

    def generateNewBoard(self, difficulty):
        self.difficulty = difficulty
        self.isFresh = True
        self.spots_visited = []
        self.game_status = 0
        self.board = []
        # Create board
        for row in range(0, self.height):
            temp = []
            for col in range(0, self.width):
                temp.append(Tile(row, col, 0))
            self.board.append(temp)

        # Sets number of bombs to add according to difficulty
        bombsToAdd = self.difficulty * self.width * self.height
        bombsToAdd = math.floor(bombsToAdd) # Rounds down to nearest integer number of bombs
        self.total_bombs = bombsToAdd
        self.flags_left = bombsToAdd

        # Adds bombs to the board at random
        while bombsToAdd > 0:
            rowToTry = random.randint(0, self.height - 1)
            colToTry = random.randint(0, self.width - 1)
            if self.board[rowToTry][colToTry].getBombState() == False:
                self.board[rowToTry][colToTry].setBombState(True)
                bombsToAdd -= 1
        
        # Updates the value of each tile based on the number of adjacent bombs
        for row in range(0, self.height):
            for col in range(0, self.width):
                self.updateValue(row, col)
    
    def updateValue(self, tileRow, tileCol):
        """
        Updates the value of an individual tile based on number of adjacent bombs
        """
        if self.board[tileRow][tileCol].getBombState() == False:
            numAdjBombs = 0

            for r in range(tileRow - 1, tileRow + 2):
                for c in range(tileCol - 1, tileCol + 2):
                    if r >= 0 and r < self.height and c >= 0 and c < self.width:
                        if self.board[r][c].getBombState() == True:
                            numAdjBombs += 1

            self.board[tileRow][tileCol].setValue(numAdjBombs)
            
    def printBoard(self):
        """
        Prints current board state for debugging purposes
        """
        for row in self.board:
            for col in row:
                print(f"{col.value:2} ", end = "")
            print()

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def printInfo(self):
        pass

    def revealAll(self):
        for row in self.board:
            for col in row:
                col.setRevealedState(True)

    def sendClick(self, mx, my):
        # Forces the first click to be on a zero tile
        if self.isFresh == True:
            for row in range(0, self.height):
                for col in range(0, self.width):
                    if self.board[row][col].inRange(mx, my):
                        while (self.board[row][col].getValue() != 0):
                            self.generateNewBoard(self.difficulty)
                        self.isFresh = False
                        self.sendTileClick(row, col)
        else:
            for row in range(0, self.height):
                for col in range(0, self.width):
                    if self.board[row][col].inRange(mx, my):
                        self.sendTileClick(row, col)
        self.spots_visited = []

    def sendRightClick(self, mx, my):
        if self.isFresh == False:
            for row in range(0, self.height):
                for col in range(0, self.width):
                    if self.board[row][col].inRange(mx, my):
                        self.flags_left -= self.board[row][col].sendRightClick()

    def sendTileClick(self, row, col):
        self.spots_visited.append((row, col))
        self.flags_left += self.board[row][col].sendClick()
        if self.board[row][col].getValue() == 0:
            if row > 0 and col > 0 and (row-1, col-1) not in self.spots_visited:
                self.sendTileClick(row-1, col-1)
            if row > 0 and (row-1, col) not in self.spots_visited:
                self.sendTileClick(row-1, col)
            if row > 0 and col < self.width-1 and (row-1, col+1) not in self.spots_visited:
                self.sendTileClick(row-1, col+1)
            if col > 0 and (row, col-1) not in self.spots_visited:
                self.sendTileClick(row, col-1)
            if col < self.width-1 and (row, col+1) not in self.spots_visited:
                self.sendTileClick(row, col+1)
            if row < self.height-1 and col > 0 and (row+1, col-1) not in self.spots_visited:
                self.sendTileClick(row+1, col-1)
            if row < self.height-1 and (row+1, col) not in self.spots_visited:
                self.sendTileClick(row+1, col)
            if row < self.height-1 and col < self.width-1 and (row+1, col+1) not in self.spots_visited:
                self.sendTileClick(row+1, col+1)

    def check_state(self):
        bomb_counter = self.total_bombs
        reveal_counter = self.height * self.width
        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.board[row][col].isFlagged and self.board[row][col].isBomb:
                    bomb_counter -= 1
                if self.board[row][col].isExploded():
                    self.game_over()
                if self.board[row][col].isRevealed or (self.board[row][col].isFlagged and self.board[row][col].isBomb):
                    reveal_counter -= 1
        if bomb_counter == 0 and reveal_counter == 0:
            self.win_game()

    def game_over(self):
        self.game_status = 2

    def win_game(self):
        self.game_status = 1

    def draw(self, surface, text_obj, text_obj2):
        for row in self.board:
            for col in row:
                col.draw(surface, text_obj)

        if self.isFresh:
            text_obj2.render_to(surface, (15, 515), "Click anywhere to begin", BLACK)
        else:
            text_obj2.render_to(surface, (15, 515), "Flags Remaining: " + str(self.flags_left), BLACK)
            text_obj2.render_to(surface, (15, 545), "Total Bombs: " + str(self.total_bombs), BLACK)
            if self.game_status == 0:
                text_obj2.render_to(surface, (265, 515), "Right click to flag", BLACK)

        if self.game_status == 1:
            text_obj2.render_to(surface, (235, 525), "Congratulations! You win!", GREEN)
            pygame.display.update()
            time.sleep(4)
            self.generateNewBoard(self.difficulty + 0.02)

        elif self.game_status == 2:
            text_obj2.render_to(surface, (265, 525), "Game Over!", RED)
            if self.flags_left == 0:
                text_obj2.render_to(surface, (265, 545), "All flags used!", RED)
            pygame.display.update()
            time.sleep(4)
            self.generateNewBoard(self.difficulty)
