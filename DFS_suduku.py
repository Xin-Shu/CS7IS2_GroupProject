

import numpy as np

board = np.zeros((9, 9), dtype=int)  # 整个棋盘
rowFlag = np.zeros((9, 10), dtype=int)  # rowFlag[i][num]=1,表示第i行已放了数字num
colFlag = np.zeros((9, 10), dtype=int)  # colFlag[i][num]=1,表示第i列已放了数字num
blockFlag = np.zeros((9, 10), dtype=int)  # blockFlag[i][num]=1,表示第i块已放了数字num
blankpos = []  # blankpos[i]表示第i+1个空白控制

board = [[0, 0, 4, 3, 0, 0, 2, 0, 9],
         [0, 0, 5, 0, 0, 9, 0, 0, 1],
         [0, 7, 0, 0, 6, 0, 0, 4, 3],
         [0, 0, 6, 0, 0, 2, 0, 8, 7],
         [1, 9, 0, 0, 0, 7, 4, 0, 0],
         [0, 5, 0, 0, 8, 3, 0, 0, 0],
         [6, 0, 0, 0, 0, 0, 1, 0, 5],
         [0, 0, 3, 5, 0, 8, 6, 9, 0],
         [0, 4, 2, 9, 1, 0, 3, 0, 0]]


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
    if n < 0:
        return 1
    r = blankpos[n][0]
    c = blankpos[n][1]
    for num in range(1, 10):
        if Isok(r, c, num):
            board[r][c] = num
            setallflag(r, c, num, 1)
            if Dfs(n - 1):
                return 1
            setallflag(r, c, num, 0)
    return 0


for i in range(9):
    for j in range(9):
        if board[i][j] != 0:
            setallflag(i, j, board[i][j], 1)
        else:
            blankpos.append((i, j))

print("问题：", board)
if Dfs(len(blankpos) - 1):
    print("结果：", board)

