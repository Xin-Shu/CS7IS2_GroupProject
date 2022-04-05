# import pygame library
import time
import Sudoku
import pygame
import numpy as np

# Solution scriptes
import tensorflow as tf
from scripts import inferenceSudoku
from scripts import ac3Solver
from scripts.geneticSolver import SudokuSolver

# model = tf.keras.models.load_model('dataset/trainedCNNModel.h5')

# initialise the pygame font
pygame.font.init()

# Total window
screen = pygame.display.set_mode((500, 600))

# Title and Icon
pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING")

x = 0
y = 0
dif = 500 / 9


# Default Sudoku Board.
grid = Sudoku.exportSeries(1)

# Some global variables for DFS
rowFlag = np.zeros((9, 10), dtype=int)
colFlag = np.zeros((9, 10), dtype=int)
blockFlag = np.zeros((9, 10), dtype=int)
blankpos = []
dfsLoopNum = 0

# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 15)
font2 = pygame.font.SysFont("comicsans", 18)


def get_cord(pos):
    global x
    x = pos[0] // dif
    global y
    y = pos[1] // dif


# Highlight the cell selected
def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)


# Function to draw required lines for making Sudoku grid
def draw():
    # Draw the lines

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (0, 153, 153), (i * dif, j * dif, dif + 1, dif + 1))

                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))
    # Draw lines horizontally and verticallyto form grid
    for i in range(10):
        if i % 3 == 0:
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)


# Fill value entered in cell
def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))


# Raise error when wrong value entered
def raise_error1():
    text1 = font1.render("WRONG !!!", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))


def raise_error2():
    text1 = font1.render("Wrong !!! Not a valid Key", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))


# Check if the value entered in board is valid
def valid(m, i, j, val):
    for it in range(9):
        if m[i][it] == val:
            return False
        if m[it][j] == val:
            return False
    it = i // 3
    jt = j // 3
    for i in range(it * 3, it * 3 + 3):
        for j in range(jt * 3, jt * 3 + 3):
            if m[i][j] == val:
                return False
    return True


# Solves the sudoku board using Backtracking Algorithm
def solve(grid, i, j):
    while grid[i][j] != 0:
        if i < 8:
            i += 1
        elif i == 8 and j < 8:
            i = 0
            j += 1
        elif i == 8 and j == 8:
            return True
    pygame.event.pump()
    for it in range(1, 10):
        if valid(grid, i, j, it):
            grid[i][j] = it
            global x, y
            x = i
            y = j
            # white color background\
            screen.fill((255, 255, 255))
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(20)
            if solve(grid, i, j) == 1:
                return True
            else:
                grid[i][j] = 0
            # white color background\
            screen.fill((255, 255, 255))

            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(50)
    return False


# Display instruction for the game
def instruction():
    text1 = font2.render("PRESS D TO RESET TO DEFAULT / R TO EMPTY", 1, (0, 0, 0))
    text2 = font2.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
    screen.blit(text2, (20, 540))


# Display options when solved
def result():
    text1 = font1.render("FINISHED PRESS R or D", 1, (255, 0, 0))
    screen.blit(text1, (20, 570))


def getBlockNum(r, c):
    rr = r // 3
    cc = c // 3
    return rr * 3 + cc


def setallflag(i, j, num, f):
    rowFlag[i][num] = f
    colFlag[j][num] = f
    blockFlag[getBlockNum(i, j)][num] = f


def Isok(i, j, num):
    if (rowFlag[i][num] or colFlag[j][num] or blockFlag[getBlockNum(i, j)][num]) == 0:
        return 1
    else:
        return 0


def Dfs(n):
    global grid, dfsLoopNum
    dfsLoopNum += 1
    if n < 0:
        return 1
    r = blankpos[n][0]
    c = blankpos[n][1]
    for num in range(1, 10):
        if Isok(r, c, num):
            grid[r][c] = num
            setallflag(r, c, num, 1)
            if Dfs(n - 1):
                return 1
            setallflag(r, c, num, 0)
    return 0


def main():

    global grid, x, y
    global rowFlag, colFlag, blockFlag, blankpos, dfsLoopNum

    flag1, flag2 = 0, 0
    rs, error, val = 0, 0, 0
    model = []
    run = True
    # The loop thats keep the window running
    while run:

        # White color background
        screen.fill((170, 170, 170))
        # Loop through the events stored in event.get()
        for event in pygame.event.get():
            # Quit the game windows
            if event.type == pygame.QUIT:
                run = False
            # Get the mouse position to insert number
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag1 = 1
                pos = pygame.mouse.get_pos()
                get_cord(pos)
            # Get the number to be inserted if key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x -= 1
                    flag1 = 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                    flag1 = 1
                if event.key == pygame.K_UP:
                    y -= 1
                    flag1 = 1
                if event.key == pygame.K_DOWN:
                    y += 1
                    flag1 = 1
                if event.key == pygame.K_1:
                    val = 1
                if event.key == pygame.K_2:
                    val = 2
                if event.key == pygame.K_3:
                    val = 3
                if event.key == pygame.K_4:
                    val = 4
                if event.key == pygame.K_5:
                    val = 5
                if event.key == pygame.K_6:
                    val = 6
                if event.key == pygame.K_7:
                    val = 7
                if event.key == pygame.K_8:
                    val = 8
                if event.key == pygame.K_9:
                    val = 9
                if event.key == pygame.K_RETURN:
                    flag2 = 1
                # If 'q', reset grid to 'easy' mode
                if event.key == pygame.K_q:
                    print(pygame.key.get_mods())
                    rs = 0
                    error = 0
                    flag2 = 0
                    grid = Sudoku.exportSeries(1)

                # If 'w', reset grid to 'medium' mode
                if event.key == pygame.K_w:
                    rs = 0
                    error = 0
                    flag2 = 0
                    grid = Sudoku.exportSeries(2)
                # If 'e', reset grid to 'hard' mode
                if event.key == pygame.K_e:
                    rs = 0
                    error = 0
                    flag2 = 0
                    grid = Sudoku.exportSeries(3)

                # Press 'l' to crack game, algorithm using 'backtracking'
                if event.key == pygame.K_s:
                    start_ = time.time()
                    print(grid)
                    solve(grid, 0, 0)
                    currentState = Sudoku.Find_Empty_Cell(grid)
                    if currentState[2] == 0:
                        print("INFO: Algorithm BackTracking, Time used: {:.2f} s".format(time.time() - start_))
                        rs = 1

                # Press 'l' to crack game, algorithm using 'DNN inference'
                if event.key == pygame.K_l:
                    grid = np.array(grid)
                    start_ = time.time()
                    if not model:
                        model = tf.keras.models.load_model('dataset/trainedCNNModel.h5')
                        print(f"INFO: Loaded DNN pre-trained model, time used: {time.time() - start_}")
                    prediction = inferenceSudoku.inference_sudoku(model, grid, 1)
                    if prediction is not None:
                        print(prediction)
                        print(f"INFO: Algorithm DNN, Time used: {time.time() - start_:.4f} secs")
                        grid = prediction
                        rs = 1

                # Press 'l' to crack game, algorithm using 'ac3' and 'backTracking'
                if event.key == pygame.K_a:
                    digitCount, gridTemp = 0, ''
                    for i in range(0, len(grid)):
                        for j in range(0, len(grid[i])):
                            gridTemp += str(grid[i][j])
                    start_ = time.time()
                    solution = ac3Solver.solve(gridTemp, 1, 1)
                    print("INFO: Algorithm ac-3 Solver, Time used: {:6.2f} s".format(time.time() - start_))
                    grid = list(ac3Solver.list_split(solution, 9))
                    rs = 1

                # Press 'g' for genetic solver
                if event.key == pygame.K_g:
                    grid = np.array(grid)
                    print("Solving using genetic algorithm...")
                    start_ = time.time()
                    genesolver = SudokuSolver()
                    solution = genesolver.solve(grid, populations=1000)
                    if solution:
                        prediction = solution.values
                        print(prediction)
                        print("INFO: Algorithm Genetic Solver, Time used: {:6.2f} s".format(time.time() - start_))
                        grid = prediction
                        rs = 1

                # Press 'b' to crack game, algorithm using depth first search (baseline model)
                if event.key == pygame.K_d:

                    start_ = time.time()
                    grid = np.array(grid)
                    for i in range(9):
                        for j in range(9):
                            if grid[i][j] != 0:
                                setallflag(i, j, grid[i][j], 1)
                            else:
                                blankpos.append((i, j))
                    if Dfs(len(blankpos) - 1):
                        rowFlag = np.zeros((9, 10), dtype=int)
                        colFlag = np.zeros((9, 10), dtype=int)
                        blockFlag = np.zeros((9, 10), dtype=int)
                        blankpos = []
                        print(f"INFO: Algorithm Depth First Search, Time used: {time.time() - start_:.4f} secs,"
                              f"DFS loop number: {dfsLoopNum}.")

        # Display algorithm
        if flag2 == 1:
            if not solve(grid, 0, 0):
                error = 1
            else:
                rs = 1
            flag2 = 0
        if val != 0:
            draw_val(val)
            # print(x)
            # print(y)
            if valid(grid, int(x), int(y), val):
                grid[int(x)][int(y)] = val
                flag1 = 0
            else:
                grid[int(x)][int(y)] = 0
                raise_error2()
            val = 0
        if error == 1:
            raise_error1()
        if rs == 1:
            result()
        draw()
        if flag1 == 1:
            draw_box()
        instruction()

        # Update window
        pygame.display.update()


if __name__ == '__main__':
    main()
    # Quit pygame window
    pygame.quit()
