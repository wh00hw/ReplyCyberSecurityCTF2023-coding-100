# Reply Cyber Security Challenge 2023 - coding-100 - NumOps enigma

In this challenge, we are given a series of zip files, each protected by a password. The goal is to extract the contents of these zip files and retrieve a flag hidden within them. The challenge progressively becomes more difficult as we move from one level to the next.

## Problem Description

The challenge consists of several levels, each of which provides a text file, `lvl_<level>.txt` and a zip file `lvl_<level>.zip` containing the next Sudoku puzzle to solve. The puzzle is a grid of cells, and each cell contains a variable `n_<r>_<c>`, where `r` is the row index and `c` is the column index. The goal is to determine the values of these variables that satisfy certain constraints. Once we have the correct sudoku values, we can use them as the password to extract the contents of the corresponding zip file for that level. The last zip file should contains `flag.txt`

### Sudoku Constraints

1. Each cell must contain an integer from 1 to N, where N is the size of the grid.
2. No two cells in the same row or column can contain the same value.
3. Certain regions in the grid are marked with letters (e.g., 'A', 'B', 'C'). These regions have specific constraints:
   - '+' indicates that the values in the region must sum up to a given constant.
   - '*' indicates that the values in the region must multiply to a given constant.
   - '-' indicates that the values in the region must be either x - y or y - x, where x and y are constants.
   - '/' indicates that the values in the region must be either x / y or y / x, where x and y are constants.



### Constraint Satisfaction Problem (CSP)

A **Constraint Satisfaction Problem** is a formal framework for representing and solving problems where a set of variables must be assigned values while satisfying a set of constraints. In this CTF challenge, the CSP includes:

1. **Variables**: These are represented by `n_<r>_<c>`, where `r` and `c` represent the row and column indexes in the grid. The goal is to find values that satisfy the constraints.

2. **Domains**: The domain for each variable is the integers from 1 to N, where N is the size of the grid. Variables are assigned values from this domain.

3. **Constraints**: Constraints are rules that define the relationships between variables. In this challenge, there are three types of constraints:
   - **Uniqueness Constraints**: No two cells in the same row or column can have the same value. This is implemented with lambda functions that ensure different values for variables in the same row or column.
   - **Region Constraints**: These are specific to regions in the grid marked with letters. Depending on the operator ('+', '*', '-', '/'), constraints are added to ensure the values in the region satisfy the given operation.

### Recursive Backtracking Algorithm

**Recursive Backtracking** is a systematic search algorithm used to solve CSPs by exploring the possible assignments of values to variables. It works as follows:

1. **Variable Selection**: Choose an unassigned variable. In this challenge, variables represent the grid cells, and they are typically chosen in a predefined order.

2. **Value Assignment**: Assign a value from the variable's domain to the chosen variable.

3. **Constraint Propagation**: Check if the assignment violates any constraints. If it does, backtrack and try a different value for the variable. If the assignment is valid, proceed to the next unassigned variable.

4. **Recursive Exploration**: Repeat steps 1 to 3 for all unassigned variables. If a solution is found, return it. If a variable has no valid assignments left, backtrack to the previous variable and explore a different assignment.

### Applying Recursive Backtracking to the Challenge

In this challenge, Recursive Backtracking is used to search for valid assignments of values to the grid cells (variables) while respecting the CSP's constraints. Here's how it works:

1. **Variable Selection**: Variables are typically selected in the order they appear in the grid. This ensures that the solver explores the puzzle systematically.

2. **Value Assignment**: Values from the domain (1 to N) are assigned to the chosen variable.

3. **Constraint Propagation**: The constraints are enforced during each assignment. If a constraint is violated, the solver backtracks to the previous variable and explores a different value.

4. **Recursive Exploration**: The solver iterates through the variables recursively, attempting to find a valid assignment for each variable. If a solution is found, it is used as the password to extract the corresponding zip file. If a variable has no valid assignments left, the solver backtracks and explores different values for the previous variables.

By following this process, the solver systematically explores the search space of variable assignments until it finds a valid solution.

## Solution

The solution involves using a constraint satisfaction problem solver to find a valid assignment of values to the variables. The code provided uses the `constraint` library to formulate and solve the problem. The process can be broken down as follows:

1. Read the sudoku constraints from the text file for the current level.
2. Create variables for each cell in the grid and set their domains to integers from 1 to N.
3. Add constraints to ensure that no two cells in the same row or column have the same value.
4. For each region, add constraints based on the region's specified operation ('+', '*', '-', '/').
5. Solve the constraint satisfaction problem to find a valid assignment of values.
6. Use the obtained values as a password to extract the contents of the corresponding zip file.
7. If the extraction is successful, print the flag.

The code `solver.py` iterates through each level, progressively solving more complex sudoku and extracting zip files until the flag is found.
