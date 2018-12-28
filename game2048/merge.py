#encoding:utf8
__author__ = 'gold'

__doc__ = '''this file is used to help change the matrix'''

import random

win = 'you win'
lose = 'you lose'
not_over = 'not over'

def random2(matrix):
    '''
    choose a random position whose value is 0 to set its value t0 2
    :param matrix:
    :return:
    '''
    x = random.randint(0,len(matrix) - 1)
    y = random.randint(0,len(matrix) - 1)
    while matrix[x][y] != 0:
        x = random.randint(0, len(matrix) - 1)
        y = random.randint(0, len(matrix) - 1)
    matrix[x][y] = random.choice([2,4])

def getNewMatrix(n = 4):
    '''
    get a new gamen matrix
    :param n:int,represent the width and height of the matrix
    :return: [[int],],a matix with n sut int-list while each list has 4 zero
    '''
    return [[0] * n for _ in range(n)]

def getState(matrix,point = 2048):
    '''
    get the state of the game now
    :param matrix: [[int],]，the num matrix of the game
    :return: str,represent the state of the game,ie:'you win' means the gamer win it,
                'you lose' means the gamer loses the game,
                'not over' means the game can be continued
    '''
    for row in range(len(matrix)):
        for col in range(len(matrix)):
            if matrix[row][col] == point:
                return win
            if matrix[row][col] == 0:
                return not_over
            if row < len(matrix) - 1 and matrix[row][col] == matrix[row + 1][col]:
                return not_over
            if col < len(matrix) - 1 and matrix[row][col] == matrix[row][col + 1]:
                return not_over
            if row == len(matrix) - 1:
                if col < len(matrix) - 1 and matrix[row][col] == matrix[row][col + 1]:
                    return not_over
            if col == len(matrix) - 1:
                if row < len(matrix) - 1 and matrix[row][col] == matrix[row + 1][col]:
                    return not_over

    return lose

def leftMerge(matrix):
    '''
    merge from right to left
    :param matrix: [[int],],the matrix
    :return: bool,bool means if this can work
    '''
    ok = False
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == 0:
                continue
            index = col + 1
            while index < len(matrix):
                if matrix[row][index] == 0:
                    index += 1
                    continue
                if matrix[row][index] == matrix[row][col]:
                    matrix[row][col] *= 2
                    matrix[row][index] = 0
                    ok = True
                break

        for col in range(len(matrix[0])):
            if matrix[row][col] != 0:
                continue
            index = col + 1
            while index < len(matrix[0]):
                if matrix[row][index] != 0:
                    break
                index += 1
            if index != len(matrix[0]):
                matrix[row][col] = matrix[row][index]
                matrix[row][index] = 0
                ok = True
            else:
                break

    return ok

def rightMerge(matrix):
    '''
    merge from left to right
    :param matrix: [[int],],the matrix
    :return: bool
    '''
    ok = False
    for row in range(len(matrix)):
        for col in range(len(matrix) - 1,-1,-1):
            if matrix[row][col] == 0:
                continue
            index = col - 1
            while index > -1:
                if matrix[row][index] == 0:
                    index -= 1
                    continue
                if matrix[row][index] == matrix[row][col]:
                    matrix[row][col] *= 2
                    matrix[row][index] = 0
                    ok = True
                break

        for col in range(len(matrix[0]) - 1,-1,-1):
            if matrix[row][col] != 0:
                continue
            index = col - 1
            while index > -1:
                if matrix[row][index] != 0:
                    break
                index -= 1
            if index >= 0:
                matrix[row][col] = matrix[row][index]
                matrix[row][index] = 0
                ok = True
            else:
                break

    return ok

def topMerge(matrix):
    '''
    merge from down to top
    :param matrix:
    :return:
    '''
    ok = False
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            if matrix[row][col] == 0:
                continue
            index = row + 1
            while index < len(matrix):
                if matrix[index][col] == 0:
                    index += 1
                    continue
                if matrix[index][col] == matrix[row][col]:
                    matrix[row][col] *= 2
                    matrix[index][col] = 0
                    ok = True
                break
        for row in range(len(matrix)):
            if matrix[row][col] != 0:
                continue
            index = row + 1
            while index < len(matrix):
                if matrix[index][col] != 0:
                    break
                index += 1
            if index < len(matrix):
                matrix[row][col] = matrix[index][col]
                matrix[index][col] = 0
                ok = True
            else:
                break

    return ok

def bottomMerge(matrix):
    '''
    merge from top to bottom
    :param matrix:
    :return:
    '''
    ok = False
    for col in range(len(matrix[0])):
        for row in range(len(matrix) - 1,-1,-1):
            if matrix[row][col] == 0:
                continue
            index = row - 1
            while index >= 0:
                if matrix[index][col] == 0:
                    index -= 1
                    continue
                if matrix[index][col] == matrix[row][col]:
                    matrix[row][col] *= 2
                    matrix[index][col] = 0
                    ok = True
                break
        for row in range(len(matrix) - 1,-1,-1):
            if matrix[row][col] != 0:
                continue
            index = row - 1
            while index >= 0:
                if matrix[index][col] != 0:
                    break
                index -= 1
            if index >= 0:
                matrix[row][col] = matrix[index][col]
                matrix[index][col] = 0
                ok = True
            else:
                break

    return ok

def p(matrix):
    for m in matrix:
        print(m)

if __name__ == '__main__':
    matrix = [
        [2,2,0,4],
        [2,2,2,4],
        [0,2,4,4],
        [0,2,2,4],
    ]
    leftMerge(matrix)
    p(matrix)
    print('***')
    rightMerge(matrix)
    p(matrix)
    print('***')
    leftMerge(matrix)
    # leftMerge(matrix)
    p(matrix)