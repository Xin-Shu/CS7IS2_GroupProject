
import numpy as np

boardIN = np.zeros((9, 9), dtype=int)
rowFlag = np.zeros((9, 10), dtype=int)
colFlag = np.zeros((9, 10), dtype=int)
blockFlag = np.zeros((9, 10), dtype=int)
blankpos = []

# board = [[0, 0, 4, 3, 0, 0, 2, 0, 9],
#          [0, 0, 5, 0, 0, 9, 0, 0, 1],
#          [0, 7, 0, 0, 6, 0, 0, 4, 3],
#          [0, 0, 6, 0, 0, 2, 0, 8, 7],
#          [1, 9, 0, 0, 0, 7, 4, 0, 0],
#          [0, 5, 0, 0, 8, 3, 0, 0, 0],
#          [6, 0, 0, 0, 0, 0, 1, 0, 5],
#          [0, 0, 3, 5, 0, 8, 6, 9, 0],
#          [0, 4, 2, 9, 1, 0, 3, 0, 0]]


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
    global boardIN
    if n < 0:
        return 1
    r = blankpos[n][0]
    c = blankpos[n][1]
    for num in range(1, 10):
        if Isok(r, c, num):
            boardIN[r][c] = num
            setallflag(r, c, num, 1)
            if Dfs(n - 1):
                return 1
            setallflag(r, c, num, 0)
    return 0


def exportResult(boardIN_):
    global boardIN, blankpos, rowFlag, colFlag, blockFlag
    boardIN = boardIN_
    for i in range(9):
        for j in range(9):
            if boardIN[i][j] != 0:
                setallflag(i, j, boardIN[i][j], 1)
            else:
                blankpos.append((i, j))
    if Dfs(len(blankpos) - 1):
        boardTemp_ = boardIN
        boardIN = np.zeros((9, 9), dtype=int)
        rowFlag = np.zeros((9, 10), dtype=int)
        colFlag = np.zeros((9, 10), dtype=int)
        blockFlag = np.zeros((9, 10), dtype=int)
        blankpos = []
        return boardTemp_


if __name__ == '__main__':
    board = [[2, 1, 0, 8, 0, 3, 0, 0, 6],
             [0, 0, 0, 0, 9, 0, 0, 2, 0],
             [5, 0, 8, 0, 0, 6, 1, 4, 0],
             [0, 5, 0, 0, 8, 0, 9, 0, 4],
             [3, 0, 6, 1, 0, 4, 2, 8, 0],
             [0, 4, 0, 0, 0, 9, 0, 0, 0],
             [4, 2, 0, 0, 0, 0, 0, 7, 5],
             [0, 8, 5, 0, 6, 7, 0, 0, 0],
             [6, 7, 1, 0, 3, 5, 8, 9, 0]]
    boardOUT = exportResult(board)
    print(boardOUT)

