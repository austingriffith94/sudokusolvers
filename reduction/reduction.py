# Sudoku Solver
# Reduction Method
# Austin Griffith

import time
from csv import reader, writer
from string import ascii_uppercase

# cross product of two values
def cross(X, Y):
    return [x + y for x in X for y in Y]

# create dict of values with cell coord
def valkey(p,pair):
    nums = []
    for r in p:
        nums = nums + r
    gridvals = dict(zip(pair, nums))
    return(gridvals)

# create list of possible values for each cell
def possible(cur,vals,keys):
    for p,n in cur.items():
        checks = []

        # run loop for all unchosen cells
        if n == 0:
            for k in keys[p]:
                for i in k:
                    if cur[i] != 0 and cur[i] not in checks:
                        # create list of numbers already in line or square
                        # with current cell
                        checks.append(cur[i])
            if checks:
                for c in checks:
                    try:
                        # remove values from the checks
                        vals[p].remove(c)
                    except:
                        # if already removed, then pass
                        pass
        else:
            # if number already chosen, then it is a single value
            vals[p] = [n]
    return(vals)

# if there is a single value for a cell, place that in the current puzzle
# repeat till the puzzle isn't being updated
def traditional_solve(cur,vals,keys):
    check = False
    v = vals.copy()

    while check == False:
        v = possible(cur,v,keys)
        curnew = cur.copy()

        for p,n in v.items():
            if len(n) == 1:
                curnew[p] = n[0]

        if curnew == cur:
            check = True

        cur = curnew.copy()

    return(cur)

# backtrack functions
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
def brute_solve(p):

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
            check = brute_solve(p)

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

# solve function
def solve_sudoku(puz):

    # get column index
    col = str()
    for i in range(1,10):
        col = col + str(i)

    # get row index
    row = ascii_uppercase[:9]

    # letter to number key
    letnumkey = dict()
    for i,l in enumerate(ascii_uppercase):
       letnumkey[l] = i

    # create unit list of coordinates
    pairs = cross(row, col)
    rowm = [cross(row,c) for c in col]
    colm = [cross(r,col) for r in row]
    squarem = [cross(r,c) for r in [row[:3],row[3:6],row[6:9]] for c in [col[:3],col[3:6],col[6:9]]]
    matches = rowm + colm + squarem

    # the 3 checks for each cell
    key =  dict((p, [m for m in matches if p in m]) for p in pairs)

    # create dictionary from initial puzzle values
    current = valkey(puz,pairs)

    # create dictionary of all possible puzzle values
    values = dict((p, [c for c in range(1,10)]) for p in pairs)

    # run reduction solver till no more new values can be deduced
    currentnew = traditional_solve(current,values,key)
    # turn values back into a list of lists
    puzzlenew = [list() for p in range(9)]
    for p,n in currentnew.items():
        puzzlenew[letnumkey[p[0]]].append(n)
    # run brute force solver on partially solved puzzle
    solved = brute_solve(puzzlenew)

    return(solved)

# main run
def mainout(filein='input.csv'):
    # pull puzzle from puz
    puzzlecsv = []
    with open(filein, newline='') as csvfile:
        inputreader = reader(csvfile, delimiter=' ', quotechar='|')
        for row in inputreader:
            puzzlecsv.append(row[0].split(','))

    puzzle = [list(map(int, x)) for x in puzzlecsv]

    start = time.time()
    solved = solve_sudoku(puzzle)

    print('Time to Complete:', time.time() - start)
    print('Is puzzle solved?:', solution_check(solved))

    # print solution to puzzle
    print()
    print('Solution:\n')
    display_puzzle(solved)

    # write to output csv
    fileout = 'output'
    with open(fileout + '.csv', 'w') as f:
        write = writer(f, lineterminator='\n')
        write.writerows(solved)
    f.close()

    print()
    print()
    input("Press Enter to continue...")





if __name__ == "__main__":
    f = 'input.csv'
    mainout(filein=f)
