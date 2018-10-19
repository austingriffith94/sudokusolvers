# sudokusolvers
A sudoku script and executables that read .csv files as inputs, then outputs the solution. The scripts utilize only simple python data structures, for both speed and executable size. Scripts were turned into executables using the pyinstaller package.

## backtracknp.py
This is the first iteration of the solver. The functions execute a recursive function to brute force a solution to the given puzzle. It utilizes the pandas and numpy packages to run the script. The input.csv file is read in using the pandas reader, and holds the values in numpy arrays for the recursive functions. However, these data structure aren't efficient with the iterative loops required by this method. Therefore, it can take a few seconds for the easy puzzles, and upwards of 10 to 20 minutes for the more difficult puzzles. This is entirely unacceptable, since this would be enough time for the user to complete the sudoku himself/herself, defeating the purpose of the solver. Furthermore, the numpy and pandas packages make the executable bloat to 200+ Mb. Hence, this script is a useful reference, but otherwise inefficient. It shouldn't be used unless the user is curious for time comparisons.

## backtrack.py and backtrack.exe
The second iteration of the solver utilized the same recursive methods as the numpy/pandas based code. However, in order to increase speed and reduce the executable size, all numpy and pandas functions and data structures were replaced with base python structures and functions. Lists proved invaluable in increasing the efficiency of the recursive function. The script reduced the time to complete challenging puzzles from 10+ minutes down to 20 seconds. Still time consuming, but 60 times shorter. It is also important to note that the removal of the more complex packages (now only using built in packages like 'csv') allowed the executable to take up only 5 Mb when compiled.

## reduction.py and reduction.exe
A new method was introduced in this next script. It involves solving the puzzle much like a person would. Each cell is part of a row and column. The method uses the cell's row column information to determine which values are possible. If there is only one possible value, then this is the correct value. That cell is changed to the singular value, and the new puzzle has the possible values updated. This is repeated until no more new cells can be solved. Once this method is exhausted, the brute force solver is implemented to finish the puzzle. This significantly reduces the complexity of the given puzzle. Therefore, even if the reduction method doesn't completely solve the puzzle, it can drastically reduce the time for the brute force method. For simpler puzzles, completion times dropped by an order of magnitude. For the most difficult puzzles available, the time was reduced from 20+ to 18 seconds. Similar to the backtrack script, it utilizes only built in python packages and data structures.

## Time Measurements
The time to solve is the most important feature of the solver, outside of it being able to solve the puzzle correctly. In order to get an idea of how these scripts performed, they were modified to suppress output, and then tested on a series of puzzles. For the first round, they were tested on XXXX easy to normal difficulty puzzles, randomly sampled from a list of 1 million sudokus. This file can be found on Kaggle, [here.](https://www.kaggle.com/bryanpark/sudoku) The solvers' time to complete were measured. You can see the results below.

![Backtrack Numpy](https://github.com/austingriffith94/sudokusolvers/blob/master/timetest/backnp.png "Backtrack Numpy")

![Backtrack](https://github.com/austingriffith94/sudokusolvers/blob/master/timetest/back.png "Backtrack")

![Reduction](https://github.com/austingriffith94/sudokusolvers/blob/master/timetest/reduction.png "Reduction")

As you can see from the distributions, each refinement of the method leads to an order of magnitude decrease in computation time. The average time to completion are as follows:

    Reduction       : 0.00228 s
    Backtrack       : 0.00848 s
    Backtrack Numpy : 0.14555 s
