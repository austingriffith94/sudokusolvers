# Sudoku Solver
# Backtrack Method
# Austin Griffith

import time
from csv import reader, writer

# check final puzzle solution using sum products rows/columns
def solution_check(p):
    check = 1
    for i in range(1,10):
        check = check * i

    for i in range(9):
        rowi = 1
        coli = 1
        for j in range(9):
            rowi = rowi * p[i][j]
            coli = coli * p[j][i]
        if rowi != check or coli != check:
            return(False)
    return(True)

# check row for same values
def row_check(x,i,p):
    check = i in p[x]
    return(check)

# check column for same values
def col_check(y,i,p):
    temp = [j[y] for j in p]
    check = i in temp
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

    grid = []
    for j in range(gx-3,gx):
        grid.append(p[j][gy-3:gy])
    flatgrid = [j for sub in grid for j in sub]
    check = i in flatgrid
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
            if p[x][y] == 0:
                return([x,y])
    return([-1,-1])

# recursive loop to solve the sudoku
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
            # if safe, set number choice in coordinates
            p[coord[0]][coord[1]] = num

            # build recursive function
            check = solve_sudoku(p)

            # if recursive returns completed puzzle, then return puzzle
            if find_empty(check) == [-1,-1]:
                return(p)

            # if recursive doesn't return completed puzzle, reset coordinates
            p[coord[0]][coord[1]] = 0

    # if get through loop without success, return same incomplete puzzle
    return(p)

# print list of values as a sudoku grid in command console
def display_puzzle(p):
    values = str()
    for i in p:
        for j in i:
            if j == 0:
                k = '.'
            else:
                k = j
            values = values + str(k)

    for x in range(1,10):
        v = values[x*9-9:x*9]
        w = '|'.join(v[i:i+3] for i in range(0, len(v), 3))
        print(' '.join(w[j] for j in range(0, len(w), 1)))

        if x % 3 == 0 and x < 9:
            print('- - - - - - - - - - -')

# main run
def mainout(filein='input.csv'):
    # pull puzzle from csv
    puzzlecsv = []
    with open(filein, newline='') as csvfile:
        inputreader = reader(csvfile, delimiter=' ', quotechar='|')
        for row in inputreader:
            puzzlecsv.append(row[0].split(','))

    puzzle = [list(map(int, x)) for x in puzzlecsv]

    # solve puzzle
    start = time.time()
    solved = solve_sudoku(puzzle)
    return(time.time() - start)





if __name__ == "__main__":
    f = 'input.csv'
    mainout(filein=f)

