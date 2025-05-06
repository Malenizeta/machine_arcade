
import random

def share_diagonal(x0, y0, x1, y1):
    dy = y1 - y0
    dx = x1 - x0

    return abs(dx) == abs(dy)

def col_clashes(exist_chess, index):

    for i in range(index):
        if share_diagonal(i, exist_chess[i], index, exist_chess[index]):
            return True

    return False

def has_clashes_2(chess_list):
    for i, item in enumerate(chess_list):
        if item == -1:
            continue

        for j, pre_item in enumerate(chess_list):
            if j >= i:
                break

            if pre_item == -1:  
                continue

            if share_diagonal(j, pre_item, i, item):
                print("conflict: index {0} value {1} conflicts with \ index {2} value {3}".format(j, pre_item, i, item))
                return True

    return False
