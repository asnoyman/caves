# A program that solves a cave (light up) puzzle
# Adam Snoyman, adamsnoyman@gmail.com, September 2021
import pygame
import os
import copy
import math
import time

pygame.display.set_caption("Light Up!")

# Colours used
YELLOW = (252, 212, 64)
GREY = (169, 169, 169)
BLACK = (0,0,0)

NOT_WALL = 6
CLUELESS_WALL = 5
NOT_LIGHT = -1
LIGHT = 1

BLOCK_SIZE = 50

SLEEP = 0
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

# A cell has 6 inputs, all of which are listed below with
# what values they are expected to take:
# row and col denote the position of a cell,
# wall gives the nature of whether it is a wall (and if so what clue is in it),
# solved says whether a wall has all its clue filled,
# light_bulb says whether there is a light or a cross (or unsure)
# and lit just states whether or not a cell is seen by a light bulb
class Cell:
    def __init__(self, row, col, wall, light_bulb, lit, solved):
        self.row = row #int 0 - n
        self.col = col #int 0 - n
        self.wall = wall #int 0 - 6
        self.solved = solved #bool
        self.light_bulb = light_bulb #int -1, 0, 1
        self.lit = lit #bool

    def __repr__(self):
        return f"{self.wall} "

    def cellNotLight(self):
        self.light_bulb = NOT_LIGHT

    def cellIsLight(self):
        self.light_bulb = LIGHT
        self.lit = True

    def lightUpCell(self):
        self.lit = True
        self.light_bulb = NOT_LIGHT

    # Adds a light to a cell, lighting up every cell orthagonally
    # until a wall is hit in each direction
    # returns false if a light is already seeing that square
    def addLight(self, grid, n):
        if self.light_bulb != 0 or self.lit == True or self.wall != NOT_WALL:
            return False
        self.cellIsLight()
        for j in range(self.col + 1, n):
            if grid[self.row][j].wall != NOT_WALL:
                break
            grid[self.row][j].lightUpCell()
        for j in range(self.col - 1, -1, -1):
            if grid[self.row][j].wall != NOT_WALL:
                break
            grid[self.row][j].lightUpCell()
        for i in range(self.row + 1, n):
            if grid[i][self.col].wall != NOT_WALL:
                break
            grid[i][self.col].lightUpCell()
        for i in range(self.row -1, -1, -1):
            if grid[i][self.col].wall != NOT_WALL:
                break
            grid[i][self.col].lightUpCell()

    # Returns True if a cell is not on the edge of the grid
    def notEdge(self, n):
        if self.row == 0 or self.row == n - 1 or self.col == 0 or self.col == n - 1:
            return False
        return True

# Do logic about walls. If the grid gets changed, calls itself again
def checkAllWalls(grid, n):
    for i in range (0, n):
        for j in range (0, n):
            if grid[i][j].wall == NOT_WALL or grid[i][j].solved == True:
                continue
            # For each unsolved wall, tally how many orthogonally adjacent
            # cells are lights, and how many could be lights
            lights = 0
            maybes = 0
            if i != 0 and grid[i - 1][j].light_bulb == LIGHT and grid[i - 1][j].wall == NOT_WALL:
                lights += 1
            elif i != 0 and grid[i - 1][j].light_bulb == 0 and grid[i - 1][j].wall == NOT_WALL:
                maybes += 1
            if i != n - 1 and grid[i + 1][j].light_bulb == LIGHT and grid[i + 1][j].wall == NOT_WALL:
                lights += 1
            elif i != n - 1 and grid[i + 1][j].light_bulb == 0 and grid[i + 1][j].wall == NOT_WALL:
                maybes += 1
            if j != 0 and grid[i][j - 1].light_bulb == LIGHT and grid[i][j - 1].wall == NOT_WALL:
                lights += 1
            elif j != 0 and grid[i][j - 1].light_bulb == 0 and grid[i][j - 1].wall == NOT_WALL:
                maybes += 1
            if j != n - 1 and grid[i][j + 1].light_bulb == LIGHT and grid[i][j + 1].wall == NOT_WALL:
                lights += 1
            elif j != n - 1 and grid[i][j + 1].light_bulb == 0 and grid[i][j + 1].wall == NOT_WALL:
                maybes += 1

            # If there are too many lights, or
            # if there can never be enough, return False
            if lights > grid[i][j].wall or lights + maybes < grid[i][j].wall:
                return False

            # If the number of lights matches the wall clue,
            # make the rest NOT_LIGHT and say that the wall
            # is solved. Then call checkAllWalls again
            if lights == grid[i][j].wall:
                if i != 0 and grid[i - 1][j].light_bulb != LIGHT and grid[i - 1][j].wall == NOT_WALL:
                    grid[i - 1][j].cellNotLight()
                if i != n - 1 and grid[i + 1][j].light_bulb != LIGHT and grid[i + 1][j].wall == NOT_WALL:
                    grid[i + 1][j].cellNotLight()
                if j != 0 and grid[i][j - 1].light_bulb != LIGHT and grid[i][j - 1].wall == NOT_WALL:
                    grid[i][j - 1].cellNotLight()
                if j != n - 1 and grid[i][j + 1].light_bulb != LIGHT and grid[i][j + 1].wall == NOT_WALL:
                    grid[i][j + 1].cellNotLight()
                grid[i][j].solved = True
                checkAllWalls(grid, n)

            # If the sum of lights and maybes match the clue,
            # make all maybes LIGHT and make the wall solved.
            # Then call check all walls again.
            elif lights + maybes == grid[i][j].wall:
                if i != 0 and grid[i - 1][j].light_bulb != NOT_LIGHT and grid[i - 1][j].wall == NOT_WALL:
                    grid[i - 1][j].addLight(grid, n)
                if i != n - 1 and grid[i + 1][j].light_bulb != NOT_LIGHT and grid[i + 1][j].wall == NOT_WALL:
                    grid[i + 1][j].addLight(grid, n)
                if j != 0 and grid[i][j - 1].light_bulb != NOT_LIGHT and grid[i][j - 1].wall == NOT_WALL:
                    grid[i][j - 1].addLight(grid, n)
                if j != n - 1 and grid[i][j + 1].light_bulb != NOT_LIGHT and grid[i][j + 1].wall == NOT_WALL:
                    grid[i][j + 1].addLight(grid, n)
                grid[i][j].solved = True
                checkAllWalls(grid, n)

# Takes in a file containing the setup of the cave
def readInput(file):
    # Take in n of grid.
    n = int(file.readline())

    # Create grid of n width and fill it from input file.
    grid = []
    for i in range(n):
        a = []
        for j in range(n):
            x = int(file.read(1))
            if x == CLUELESS_WALL:
                cell = Cell(i, j, x, 0, False, True)
            else:
                cell = Cell(i, j, x, 0, False, False)
            a.append(cell)
        grid.append(a)
        file.read(1)

    return n, grid

# Creates initial board setup
def drawInitial(width, grid):
    window = pygame.display.set_mode((width, width))

    #sets the background to GREY
    window.fill(GREY)

    for x in range(0, width, BLOCK_SIZE):
        for y in range(0, width, BLOCK_SIZE):
            rect = pygame.Rect(y, x, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(window, BLACK, rect, 1)
            row = x // BLOCK_SIZE
            col = y // BLOCK_SIZE
            # If there is a wall, put it in with its respective number
            if grid[row][col].wall != NOT_WALL:
                pygame.draw.rect(window, BLACK, rect)
                if grid[row][col].wall == 0:
                    window.blit(ZERO, (y + math.floor(BLOCK_SIZE / 50), x + math.floor(BLOCK_SIZE / 50)))
                if grid[row][col].wall == 1:
                    window.blit(ONE, (y + math.floor(BLOCK_SIZE / 50), x + math.floor(BLOCK_SIZE / 50)))
                if grid[row][col].wall == 2:
                    window.blit(TWO, (y + math.floor(BLOCK_SIZE / 50), x + math.floor(BLOCK_SIZE / 50)))
                if grid[row][col].wall == 3:
                    window.blit(THREE, (y + math.floor(BLOCK_SIZE / 50), x + math.floor(BLOCK_SIZE / 50)))
                if grid[row][col].wall == 4:
                    window.blit(FOUR, (y + math.floor(BLOCK_SIZE / 50), x + math.floor(BLOCK_SIZE / 50)))

    pygame.display.update()
    return grid


# Create the GUI
def drawWindow(width, grid):
    window = pygame.display.set_mode((width, width))

    for x in range(0, width, BLOCK_SIZE):
        for y in range(0, width, BLOCK_SIZE):
            row = x // BLOCK_SIZE
            col = y // BLOCK_SIZE
            if grid[row][col].wall == NOT_WALL:
                # If the square is lit up, make it yellow
                if grid[row][col].lit:
                    lit_cell = pygame.Rect(y + 1, x + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
                    pygame.draw.rect(window, YELLOW, lit_cell)
                    # Place lights where appropriate
                    if grid[row][col].light_bulb == LIGHT:
                        window.blit(LIGHT_BULB, (y + 1, x + 2.5))
                else:
                    grey_cell = pygame.Rect(y + 1, x + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
                    pygame.draw.rect(window, GREY, grey_cell)
                    if grid[row][col].light_bulb == NOT_LIGHT:
                        window.blit(CROSS, (y + 1, x + 2.5))

    pygame.display.update()

# Returns true if every wall is solved and every cell is lit
def gridSolved(grid, n):
    for i in range(0, n):
        for j in range(0,n):
            if grid[i][j].wall == NOT_WALL and grid[i][j].lit == False:
                return False
            elif grid[i][j].wall != NOT_WALL and grid[i][j].solved == False:
                return False
    return True

# For each square, if it can be a light, add a LIGHT and
# solve the rest based on that assumption. Anything modified
# before that light should never be changed.
# If the grid solves, return True. If it doesn't,
# make that cell not a light and try the next possiblity.
# If the grid has no correct solution, return False
def solveCave(grid, n, stack):

    while gridSolved(grid, n) == False:
        time.sleep(SLEEP)
        i, j = highestProb(grid, n)
        # If that spot didn't cause the previous attempt to fail
        # by making some cells impossible to light: add a light
        if i != -1:
            # Add current grid to stack
            stack.append((copy.deepcopy(grid), i, j))
            # Add a light to cell
            grid[i][j].addLight(grid, n)
            drawWindow(n*BLOCK_SIZE, grid)
        if checkAllWalls(grid, n) == False:
            if len(stack) == 0:
                return False
            # go back a step
            grid, i, j = stack.pop()
            # make that cell not a light
            grid[i][j].cellNotLight()
            drawWindow(n*BLOCK_SIZE, grid)
        if cellsNotReachable(grid, n):
            if len(stack) == 0:
                return False
            # go back a step
            grid, i, j = stack.pop()
            # make that cell not a light
            grid[i][j].cellNotLight()
            drawWindow(n*BLOCK_SIZE, grid)

    drawWindow(n*BLOCK_SIZE, grid)
    return True

def allLit(grid, n):
    for row in range(n):
        for col in range(n):
            if grid[row][col].wall == NOT_WALL and grid[row][col].lit == False:
                return False
    return True

# Finds the cell seen by the least potential lights
def highestProb(grid, n):
    x = -1
    y = -1
    prob = 0
    for row in range(n):
        for col in range(n):
            if grid[row][col].wall == NOT_WALL and grid[row][col].light_bulb == 0 and grid[row][col].lit == False:
                tally = 1
                for j in range(col + 1, n):
                    if grid[row][j].wall != NOT_WALL:
                        break
                    elif grid[row][j].light_bulb == 0:
                            tally += 1
                for j in range(col - 1, -1, -1):
                    if grid[row][j].wall != NOT_WALL:
                        break
                    elif grid[row][j].light_bulb == 0:
                            tally += 1
                for i in range(row + 1, n):
                    if grid[i][col].wall != NOT_WALL:
                        break
                    elif grid[i][row].light_bulb == 0:
                            tally += 1
                for i in range(row -1, -1, -1):
                    if grid[i][col].wall != NOT_WALL:
                        break
                    elif grid[i][row].light_bulb == 0:
                            tally += 1
                if (n*n - tally) / n*n > prob:
                    prob = (n*n - tally) / n*n
                    x = row
                    y = col
    return x, y

# If any cell in the grid can not be lit, returns True
def cellsNotReachable(grid, n):
    for row in range(n):
        for col in range(n):
            if grid[row][col].wall == NOT_WALL and grid[row][col].light_bulb == NOT_LIGHT and grid[row][col].lit == False:
                if cellLightable(grid, n, row, col) == False:
                    return True
    return False

# If the given cell be lit, return True
# else returns False
def cellLightable(grid, n, row, col):
    seen_one = False
    x = -1
    y = -1
    for j in range(col + 1, n):
        if grid[row][j].wall != NOT_WALL:
            break
        elif grid[row][j].light_bulb != NOT_LIGHT:
                if seen_one:
                    return True
                else:
                    seen_one = True
                    x = row
                    y = j
    for j in range(col - 1, -1, -1):
        if grid[row][j].wall != NOT_WALL:
            break
        elif grid[row][j].light_bulb != NOT_LIGHT:
                if seen_one:
                    return True
                else:
                    seen_one = True
                    x = row
                    y = j
    for i in range(row + 1, n):
        if grid[i][col].wall != NOT_WALL:
            break
        elif grid[i][col].light_bulb != NOT_LIGHT:
                if seen_one:
                    return True
                else:
                    seen_one = True
                    x = i
                    y = col
    for i in range(row -1, -1, -1):
        if grid[i][col].wall != NOT_WALL:
            break
        elif grid[i][col].light_bulb != NOT_LIGHT:
                if seen_one:
                    return True
                else:
                    seen_one = True
                    x = i
                    y = col
    if seen_one:
        grid[x][y].addLight
        return True
    return False


def main():

    path = "tests/" + input("file name: ")
    file = open(path, "r")
    setup = readInput(file)

    n = setup[0]
    grid = setup[1]
    width = BLOCK_SIZE*n

    stack = []

    clock = pygame.time.Clock()
    drawInitial(width, grid)

    if checkAllWalls(grid, n) == False:
        print("Puzzle not solvable.")
    else:
        drawWindow(width, grid)

    if solveCave(grid, n, stack):
        print("Puzzle complete!")
    else:
        print("Puzzle not solvable.")

    run = True
    while run:
        for event in pygame.event.get():
            clock.tick(FPS)
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
