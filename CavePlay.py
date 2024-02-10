# A program that lets you play a cave (light up) puzzle
# Adam Snoyman, adamsnoyman@gmail.com, September 2021
import pygame
import os
import datetime
import math

from os import listdir
from os.path import isfile, join

pygame.display.set_caption("Light Up!")

# Colours used
WHITE = (255, 255, 255)
YELLOW = (252, 212, 64)
GREY = (169, 169, 169)
DARK_GREY = (43, 45, 47)
BLACK = (0,0,0)

NOT_WALL = 6
CLUELESS_WALL = 5
NOT_LIGHT = -1
LIGHT = 1

BLOCK_SIZE = 50

FPS = 60

# Image names
LIGHT_BULB_IMAGE = pygame.image.load(os.path.join('Assets', 'light_bulb.png'))
LIGHT_BULB = pygame.transform.scale(LIGHT_BULB_IMAGE, (math.floor(BLOCK_SIZE * 0.9), math.floor(BLOCK_SIZE * 0.96)))

CROSS_IMAGE = pygame.image.load(os.path.join('Assets', 'cross.png'))
CROSS = pygame.transform.scale(CROSS_IMAGE, (math.floor(BLOCK_SIZE * 0.9), math.floor(BLOCK_SIZE * 0.9)))

ZERO_IMAGE = pygame.image.load(os.path.join('Assets', 'zero.png'))
ZERO = pygame.transform.scale(ZERO_IMAGE, (math.floor(BLOCK_SIZE * 0.9), math.floor(BLOCK_SIZE * 0.96)))

ONE_IMAGE = pygame.image.load(os.path.join('Assets', 'one.png'))
ONE = pygame.transform.scale(ONE_IMAGE, (math.floor(BLOCK_SIZE * 0.9), math.floor(BLOCK_SIZE * 0.96)))

TWO_IMAGE = pygame.image.load(os.path.join('Assets', 'two.png'))
TWO = pygame.transform.scale(TWO_IMAGE, (math.floor(BLOCK_SIZE * 0.9), math.floor(BLOCK_SIZE * 0.96)))

THREE_IMAGE = pygame.image.load(os.path.join('Assets', 'three.png'))
THREE = pygame.transform.scale(THREE_IMAGE, (math.floor(BLOCK_SIZE * 0.9), math.floor(BLOCK_SIZE * 0.96)))

FOUR_IMAGE = pygame.image.load(os.path.join('Assets', 'four.png'))
FOUR = pygame.transform.scale(FOUR_IMAGE, (math.floor(BLOCK_SIZE * 0.9), math.floor(BLOCK_SIZE * 0.96)))

PLAY_IMAGE = pygame.image.load(os.path.join('Assets', 'play.png'))
PLAY = pygame.transform.scale(PLAY_IMAGE, (BLOCK_SIZE * 3 // 4, BLOCK_SIZE * 3 // 4))

PAUSE_IMAGE = pygame.image.load(os.path.join('Assets', 'pause.png'))
PAUSE = pygame.transform.scale(PAUSE_IMAGE, (BLOCK_SIZE * 3 // 4, BLOCK_SIZE * 3 // 4))


class button():
    def __init__(self, colour, row, col, width, wall, light_bulb, lit):
        self.colour = colour
        self.row = row
        self.col = col
        self.width = width
        self.wall = wall #int from 0 to 6
        self.light_bulb = light_bulb #int -1, 0, 1
        self.lit = lit #bool

    def draw(self, win):
        pygame.draw.rect(win, self.colour, \
            (self.row + 2,self.col + 2,self.width - 2,self.width - 2), 0)

    def isOver(self, pos):
        # pos is the mouse position
        # ie: a tuple of (row,col) coordinates
        if pos[0] > self.row and pos[0] < self.row + self.width:
            if pos[1] > self.col and pos[1] < self.col + self.width:
                return True
        return False
    
    def cellNotLight(self):
        self.light_bulb = NOT_LIGHT
    
    def cellIsLight(self):
        self.light_bulb = LIGHT
        self.lit = True
    
    def lightUpCell(self):
        self.lit = True
        self.light_bulb = NOT_LIGHT
    
    def checkClashes(self, grid, n):
        x = self.row // BLOCK_SIZE
        y = self.col // BLOCK_SIZE - 1
        for j in range(y + 1, n):
            if grid[x][j].wall != NOT_WALL:
                break
            if grid[x][j].light_bulb == LIGHT:
                return False
        for j in range(y - 1, -1, -1):
            if grid[x][j].wall != NOT_WALL:
                break
            if grid[x][j].light_bulb == LIGHT:
                return False
        for i in range(x + 1, n):
            if grid[i][y].wall != NOT_WALL:
                break
            if grid[i][y].light_bulb == LIGHT:
                return False
        for i in range(x - 1, -1, -1):
            if grid[i][y].wall != NOT_WALL:
                break
            if grid[i][y].light_bulb == LIGHT:
                return False
        return True

    # Checks each cell to see if it lit
    def updateCell(self, grid, n):
        if self.wall != NOT_WALL:
            return
        if self.light_bulb == LIGHT:
            self.lit = True
        else:
            self.lit = False
            x = self.row // BLOCK_SIZE
            y = self.col // BLOCK_SIZE - 1
            for j in range(y + 1, n):
                if grid[x][j].wall != NOT_WALL:
                    break
                if grid[x][j].light_bulb == LIGHT:
                    self.lit = True
            for j in range(y - 1, -1, -1):
                if grid[x][j].wall != NOT_WALL:
                    break
                if grid[x][j].light_bulb == LIGHT:
                    self.lit = True
            for i in range(x + 1, n):
                if grid[i][y].wall != NOT_WALL:
                    break
                if grid[i][y].light_bulb == LIGHT:
                    self.lit = True
            for i in range(x - 1, -1, -1):
                if grid[i][y].wall != NOT_WALL:
                    break
                if grid[i][y].light_bulb == LIGHT:
                    self.lit = True

# Creates the initial grey grid
def drawInitial(width, window):
    grid = []
    rect = pygame.Rect(0, 0, width, BLOCK_SIZE)
    pygame.draw.rect(window, DARK_GREY, rect)
    pausePlay = button(DARK_GREY, width - BLOCK_SIZE, 0, BLOCK_SIZE, NOT_WALL, 0, False)
    pausePlay.draw(window)
    for x in range(0, width, BLOCK_SIZE):
        a = []
        for y in range(BLOCK_SIZE, width + BLOCK_SIZE, BLOCK_SIZE):
            square = button(GREY, x, y, BLOCK_SIZE, NOT_WALL, 0, False)
            square.draw(window)
            a.append(square)
        grid.append(a)
    pygame.display.update()
    return grid, pausePlay

# Modifies walls in setup
def drawWalls(width, grid, window):
    for x in range(0, width, BLOCK_SIZE):
        for y in range(0, width, BLOCK_SIZE):
            row = x // BLOCK_SIZE
            col = y // BLOCK_SIZE
            # If there is a wall, put it in with its respective number
            if grid[row][col].wall != NOT_WALL:
                grid[row][col].draw(window)
                if grid[row][col].wall == 0:
                    window.blit(ZERO, (x + math.floor(BLOCK_SIZE / 50), y + BLOCK_SIZE + math.floor(BLOCK_SIZE / 50)))
                elif grid[row][col].wall == 1:
                    window.blit(ONE, (x + math.floor(BLOCK_SIZE / 50), y + BLOCK_SIZE + math.floor(BLOCK_SIZE / 50)))
                elif grid[row][col].wall == 2:
                    window.blit(TWO, (x + math.floor(BLOCK_SIZE / 50), y + BLOCK_SIZE + math.floor(BLOCK_SIZE / 50)))
                elif grid[row][col].wall == 3:
                    window.blit(THREE, (x + math.floor(BLOCK_SIZE / 50), y + BLOCK_SIZE + math.floor(BLOCK_SIZE / 50)))
                elif grid[row][col].wall == 4:
                    window.blit(FOUR, (x + math.floor(BLOCK_SIZE / 50), y + BLOCK_SIZE + math.floor(BLOCK_SIZE / 50)))
            else:
                grid[row][col].draw(window)
    pygame.display.update()


# Create the GUI
def drawWindow(width, grid, window):
    for x in range(0, width, BLOCK_SIZE):
        for y in range(0, width, BLOCK_SIZE):
            row = x // BLOCK_SIZE
            col = y // BLOCK_SIZE
            if grid[row][col].wall == NOT_WALL:
                # If the square is lit up, make it YELLOW
                if grid[row][col].lit:
                    grid[row][col].colour = YELLOW
                    grid[row][col].draw(window)
                # Else make it GREY
                else:
                    grid[row][col].colour = GREY
                    grid[row][col].draw(window)
                if grid[row][col].light_bulb == LIGHT:
                        window.blit(LIGHT_BULB, (x + 2.5, y + BLOCK_SIZE + 1))
                if grid[row][col].light_bulb == NOT_LIGHT:
                    window.blit(CROSS, (x + 2.5, y + BLOCK_SIZE + 1))
        
    pygame.display.update()

# Returns true if every wall is solved and every cell is lit
def gridSolved(grid, n):
    for i in range(0, n):
        for j in range(0,n):
            if grid[i][j].wall == NOT_WALL and grid[i][j].lit == False:
                return False
            elif grid[i][j].wall == NOT_WALL and grid[i][j].light_bulb == LIGHT \
                    and grid[i][j].checkClashes(grid, n) == False:
                return False
            elif checkWalls(grid, n) == False:
                return False
    return True

def checkWalls(grid,n):
    for i in range(n):
        for j in range(n):
            if grid[i][j].wall == NOT_WALL or grid[i][j].wall == CLUELESS_WALL:
                continue
            # For each unsolved wall, tally how many orthogonally adjacent
            # cells are lights, and how many could be lights
            lights = 0
            if i != 0 and grid[i - 1][j].light_bulb == LIGHT and grid[i - 1][j].wall == NOT_WALL:
                lights += 1
            if i != n - 1 and grid[i + 1][j].light_bulb == LIGHT and grid[i + 1][j].wall == NOT_WALL:
                lights += 1
            if j != 0 and grid[i][j - 1].light_bulb == LIGHT and grid[i][j - 1].wall == NOT_WALL:
                lights += 1
            if j != n - 1 and grid[i][j + 1].light_bulb == LIGHT and grid[i][j + 1].wall == NOT_WALL:
                lights += 1
            
            if lights != grid[i][j].wall:
                return False
    return True

# Creates a grid and returns the grid and size
def loadCave(file):
    n = int(file.readline())
    width = n * BLOCK_SIZE

    # Create grid of n width and fill it from input file.
    grid = []
    for i in range(0, width, BLOCK_SIZE):
        a = []
        for j in range(BLOCK_SIZE, width + BLOCK_SIZE, BLOCK_SIZE):
            x = int(file.read(1))
            if x == NOT_WALL:
                cell = button(GREY, i, j, BLOCK_SIZE, x, 0, False)
            else:
                cell = button(BLACK, i, j, BLOCK_SIZE, x, 0, False)
            a.append(cell) 
        grid.append(a)
        file.read(1)
    
    return n, grid

def main(): 
    window = pygame.display.set_mode((500, 500))
    window.fill(GREY)
    pygame.display.update()

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 32)
    text = 'Enter grid size or load cave: '
    input = '' 

    run = True
    while run:
        for event in pygame.event.get():
            clock.tick(FPS)
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(text)
                    text = ''
                    run = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    input = input[:-1]
                else:
                    text += event.unicode
                    input += event.unicode
        
        window.fill(GREY)
        txt_surface = font.render(text, True, BLACK)
        window.blit(txt_surface, (100, 200))

        pygame.display.update()

    # Load a cave from the test file
    if input[0] == "l":
        path = "tests/" + input[1:]
        file = open(path, "r")
        n, grid = loadCave(file)
        width = n * BLOCK_SIZE
        window = pygame.display.set_mode((width, width + BLOCK_SIZE))
        window.fill(BLACK)
        pausePlay = drawInitial(width, window)[1]
        drawWalls(width, grid, window)
        pygame.display.update()
    # Create a blank grid to become a cave
    else:
        n = int(input)
        if n < 5:
            print("Too small")
            return
        width = n * BLOCK_SIZE
        window = pygame.display.set_mode((width, width + BLOCK_SIZE))
        window.fill(BLACK)
        grid, pausePlay = drawInitial(width, window)

    saved = False
    run = True
    while run:
        for event in pygame.event.get():
            clock.tick(FPS)
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                elif event.key == pygame.K_s:
                    tests = [f for f in listdir("tests") if isfile(join("tests", f))]
                    name = len(tests)
                    f = open(f"tests/{name}", "a")
                    f.write(f"{str(n)}\n")
                    for i in range(n):
                        for j in range(n):
                            f.write(str(grid[j][i].wall))
                        f.write("\n")
                    f.close()
                    run = False
                    saved = True
                elif event.key == pygame.K_BACKSPACE:
                    for i in range(n):
                        for j in range(n):
                            if grid[i][j].isOver(pos):
                                grid[i][j].colour = GREY
                                grid[i][j].wall = NOT_WALL
                elif event.key == pygame.K_0:
                    for i in range(n):
                        for j in range(n):
                            if grid[i][j].isOver(pos):
                                if grid[i][j].wall == 0:
                                    grid[i][j].colour = GREY
                                    grid[i][j].wall = NOT_WALL
                                else:
                                    grid[i][j].colour = BLACK
                                    grid[i][j].wall = 0
                elif event.key == pygame.K_1:
                    for i in range(n):
                        for j in range(n):
                            if grid[i][j].isOver(pos):
                                if grid[i][j].wall == 1:
                                    grid[i][j].colour = GREY
                                    grid[i][j].wall = NOT_WALL
                                else:
                                    grid[i][j].colour = BLACK
                                    grid[i][j].wall = 1
                elif event.key == pygame.K_2:
                    for i in range(n):
                        for j in range(n):
                            if grid[i][j].isOver(pos):
                                if grid[i][j].wall == 2:
                                    grid[i][j].colour = GREY
                                    grid[i][j].wall = NOT_WALL
                                else:
                                    grid[i][j].colour = BLACK
                                    grid[i][j].wall = 2
                elif event.key == pygame.K_3:
                    for i in range(n):
                        for j in range(n):
                            if grid[i][j].isOver(pos):
                                if grid[i][j].wall == 3:
                                    grid[i][j].colour = GREY
                                    grid[i][j].wall = NOT_WALL
                                else:
                                    grid[i][j].colour = BLACK
                                    grid[i][j].wall = 3
                elif event.key == pygame.K_4:
                    for i in range(n):
                        for j in range(n):
                            if grid[i][j].isOver(pos):
                                if grid[i][j].wall == 4:
                                    grid[i][j].colour = GREY
                                    grid[i][j].wall = NOT_WALL
                                else:
                                    grid[i][j].colour = BLACK
                                    grid[i][j].wall = 4
                elif event.key == pygame.K_SPACE:
                    for i in range(n):
                        for j in range(n):
                            if grid[i][j].isOver(pos):
                                if grid[i][j].wall == CLUELESS_WALL:
                                    grid[i][j].colour = GREY
                                    grid[i][j].wall = NOT_WALL
                                else:
                                    grid[i][j].colour = BLACK
                                    grid[i][j].wall = CLUELESS_WALL
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(n):
                    for j in range(n):
                        if grid[i][j].isOver(pos):
                            if grid[i][j].wall == NOT_WALL:
                                grid[i][j].wall = CLUELESS_WALL
                                grid[i][j].colour = BLACK
                            elif grid[i][j].wall == CLUELESS_WALL:
                                grid[i][j].wall = 0
                            elif grid[i][j].wall == 4:
                                grid[i][j].wall = NOT_WALL
                                grid[i][j].colour = GREY
                            else:
                                grid[i][j].wall += 1
        drawWalls(width, grid, window)

        pygame.display.update()

    run = True
    timer = True
    start_time = datetime.datetime.now()
    pre_pause = datetime.timedelta()
    elapsed = datetime.timedelta()
    while run:
        time_shown = 'Time: '
        for event in pygame.event.get():
            clock.tick(FPS)
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if gridSolved(grid, n):
                        print("Congratulations!")
                        run = False
                    else:
                        print("Keep trying!")
                elif event.key == pygame.K_s and saved == False:
                    tests = [f for f in listdir("tests") if isfile(join("tests", f))]
                    name = len(tests)
                    f = open(f"tests/{name}", "a")
                    f.write(f"{str(n)}\n")
                    for i in range(n):
                        for j in range(n):
                            f.write(str(grid[j][i].wall))
                        f.write("\n")
                    f.close()
                    saved = True
                elif event.key == pygame.K_SPACE:
                    for i in range(n):
                        for j in range(n):
                            if grid[i][j].isOver(pos) and grid[i][j].wall == NOT_WALL:
                                if grid[i][j].light_bulb == 0:
                                    grid[i][j].light_bulb = LIGHT
                                elif grid[i][j].light_bulb == LIGHT:
                                    grid[i][j].light_bulb = NOT_LIGHT
                                elif grid[i][j].light_bulb == NOT_LIGHT:
                                    grid[i][j].light_bulb = 0
                    for i in range(n):
                        for j in range(n):
                            grid[i][j].updateCell(grid, n)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pausePlay.isOver(pos):
                    if timer:
                        timer = False
                    else:
                        start_time = datetime.datetime.now()
                        pre_pause = elapsed
                        timer = True
                else:
                    for i in range(n):
                        for j in range(n):
                            if grid[i][j].isOver(pos) and grid[i][j].wall == NOT_WALL:
                                if grid[i][j].light_bulb == 0:
                                    grid[i][j].light_bulb = LIGHT
                                elif grid[i][j].light_bulb == LIGHT:
                                    grid[i][j].light_bulb = NOT_LIGHT
                                elif grid[i][j].light_bulb == NOT_LIGHT:
                                    grid[i][j].light_bulb = 0
                    for i in range(n):
                        for j in range(n):
                            grid[i][j].updateCell(grid, n)
        if timer:
            now = datetime.datetime.now()
            elapsed = now + pre_pause - start_time
        time_shown += str(elapsed)[2:-7]
        rect = pygame.Rect(0, 0, width, BLOCK_SIZE)
        pygame.draw.rect(window, DARK_GREY, rect)
        txt_surface = font.render(time_shown, True, WHITE)
        window.blit(txt_surface, (width // 2 - 70, 12))
        if timer:
            window.blit(PAUSE, (width - BLOCK_SIZE * 7 // 8, BLOCK_SIZE // 8))
        else: 
            window.blit(PLAY, (width - BLOCK_SIZE * 7 // 8, BLOCK_SIZE // 8))

        drawWindow(width, grid, window)
    
    pygame.draw.rect(window, DARK_GREY, rect)
    window.blit(txt_surface, (width // 2 - 70, 12))
    drawWindow(width, grid, window)

    run = True
    while run:
        for event in pygame.event.get():
            clock.tick(FPS)
            if event.type == pygame.QUIT:
                pygame.quit()

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
