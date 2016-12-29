
Short description of this solver:
- the CSP is modelled as a binary graph
- the nodes represent variables (and their possible domains), the edges represent constraints (implemented as Boolean functions)
- I only used the most generic python data types, I am not aware of any limitations regarding the data types for the search space
- the solution does not have to be unique (e.g. NQueens is not), but the code stops once one solution is found
- the solver uses backtracking
- at each iteration AC3 is used to shrink the search space 
- the code keeps track of open nodes, such that not all conditions have to be re-checked


Explanation of files:

CSPmain.py : contains the main algorithm
NQueens.py: solves the eight queens puzzle, has additional comments as a tutorial
einstein_puzzle.py: solves a version of the zebra puzzle
sudoku.py: solves Sudokus of shape 3x3, but contains a class that could be easily generalized
sudoku1..3.txt: contains three sample Sudokus of medium/high difficulty (for a human)

On my computer all sample files complete within less than 30sec.


