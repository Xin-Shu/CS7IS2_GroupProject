## Genetic solver for Sudoku game
> Ref: https://github.com/chinyan/Genetic-Algorithm-based-Sudoku-Solver

### Usage
```python
# Import module
from genetic.geneticSolver import SudokuSolver
...
# Create a genetic solver
genesolver = SudokuSolver()
# Call solve function
""" Paramters: 
[gird]          Input grid
[populations]   Number of initial population, default=1000
[generations]   Number of generations, default=10000
[mutation_rate] Mutation ratio, default=0.05
"""
solution = genesolver.solve(grid, populations=1000)
...
# Get predictions
prediction = solution.values
...
# Update gird
grid = prediction
```
