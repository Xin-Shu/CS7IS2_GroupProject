from scripts.heuristics import select_unassigned_variable, order_domain_values
from scripts.utils import is_consistent, assign, unassign

"""
Backtracking Algorithm
pseudo code found @ https://sandipanweb.files.wordpress.com/2017/03/im31.png
"""
def recursive_backtrack_algorithm(assignment, sudoku,lists):

    # if assignment is complete then return assignment
    if len(assignment) == len(sudoku.cells):
        return assignment

    # var = select-unassigned-variables(csp)
    cell = select_unassigned_variable(assignment, sudoku)

    # for each value in order-domain-values(csp, var)
    for value in order_domain_values(sudoku, cell):

        # if value is consistent with assignment
        if is_consistent(sudoku, assignment, cell, value):

            # add {cell = value} to assignment
            assign(sudoku, cell, value, assignment)
            test_list={}
            test_list=(sudoku.possibilities).copy()
            for current_cell, current_value in assignment.items():
                test_list[current_cell]=[current_value]
            lists.append(list_return(sudoku, test_list))
            # result = backtrack(assignment, csp)
            result = recursive_backtrack_algorithm(assignment, sudoku,lists)
            # if result is not a failure return result
            if result:
                return result

            # remove {cell = value} from assignment
            unassign(sudoku, cell, assignment)
   
    # return failure
    return False

def list_return(csp,test_list):
    lists=[]
    for cell in csp.cells:
        if type(test_list[cell]) == list:
            if len(test_list[cell]) == 1:
                value = test_list[cell][0]
            else :
                value = 0
        lists.append(value)
    return lists
        
