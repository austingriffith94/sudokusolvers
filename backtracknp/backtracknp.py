# Sudoku Solver
# BFS (Brute Force Method)
# Austin Griffith

import pandas as pd
import numpy as np
import time

def solution_check(p):
    check = np.math.factorial(9)

    for i in range(9):
        if np.prod(p[i]) != check or np.prod(p[:,i]) != check:
            return(False)
        else:
            return(True)

# check row for same values
def row_check(x,i,p):
    check = np.any(i == p[x])
    return(check)

# check column for same values
def col_check(y,i,p):
    check = np.any(i == p[:,y])
    return(check)

# set grid dimensions
def grid_set(a):
    if a < 3:
        return(3)
    elif a < 6:
        return(6)
    else:
        return(9)

# check grid for same values
def grid_check(x,y,i,p):
    gx = grid_set(x)
    gy = grid_set(y)

    grid = p[gx-3:gx,gy-3:gy]

    check = np.any(i == grid)
    return(check)

# check row, column and grid
# if any are matches, then not a correct choice
def safe_choice(x,y,i,p):
    r = row_check(x,i,p)
    c = col_check(y,i,p)
    g = grid_check(x,y,i,p)

    if r == True or c == True or g == True:
        return(False)
    else:
        return(True)

# find the next empty cell
# if no empty cells, then complete
def find_empty(p):
    for y in range(9):
        for x in range(9):
            if p[x,y] == 0:
                return([x,y])
    return([-1,-1])

# solve the puzzle using the functions defined above
def solve_sudoku(p):

    # if the puzzle is complete, exit function
    if find_empty(p) == [-1,-1]:
        return(p)

    # get coordinates of next empty spot
    coord = find_empty(p)

    # loop through possible numbers 1-9
    for num in range(1,10):

        # check if current number is acceptable
        if safe_choice(coord[0],coord[1],num,p) == True:
            # if safe, set in coordinates
            p[coord[0],coord[1]] = num

            # build recursive function
            check = solve_sudoku(p)

            # if recursive returns completed puzzle, then return puzzle
            if find_empty(check) == [-1,-1]:
                return(p)

            # if recursive doesn't return completed puzzle, reset coordinates
            p[coord[0],coord[1]] = 0

    # if get through loop without success, return same incomplete puzzle
    return(p)

# main run
def mainout(filename='input.csv'):
    # pull puzzle from csv
    puzzlecsv = pd.read_csv(filename,header=None)
    puzzle = np.matrix(puzzlecsv)

    # solve puzzle
    start = time.time()
    solved = solve_sudoku(puzzle)
    print(time.time() - start)
    print("Is puzzle solved?:",solution_check(puzzle))

    # write the solved value to a csv
    solvedcsv = pd.DataFrame(solved)
    solvedcsv.to_csv('output.csv', header=False, index=False)



if __name__ == "__main__":
    f = 'input.csv'
    mainout(filename=f)

