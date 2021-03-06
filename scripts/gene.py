"""_gene.py_

Definations of classes about genetic algorithm
"""

import random
import operator
import numpy as np
from past.builtins import range

random.seed()

gridSize = 9  # Size of Sudoku grid


class Population(object):
    """ Population class
    
    Initial Population
    """

    def __init__(self):
        self.candidates = []
        return

    def seed(self, Nc, given):
        self.candidates = []

        # Determine the legal values that each square can take.
        helper = Candidate()
        helper.values = [[[] for j in range(0, gridSize)] for i in range(0, gridSize)]
        for row in range(0, gridSize):
            for column in range(0, gridSize):
                for value in range(1, 10):
                    if ((given.values[row][column] == 0) and not (given.is_column_duplicate(column, value) or given.is_block_duplicate(row, column, value) or given.is_row_duplicate(row, value))):
                        # Value is available.
                        helper.values[row][column].append(value)
                    elif given.values[row][column] != 0:
                        # Given value from file.
                        helper.values[row][column].append(given.values[row][column])
                        break

        # Seed a new population.
        for p in range(0, Nc):
            g = Candidate()
            for i in range(0, gridSize):  # New row in candidate.
                row = np.zeros(gridSize)

                # Fill in the givens.
                for j in range(0, gridSize):  # New column j value in row i.

                    # If value is already given, don't change it.
                    if given.values[i][j] != 0:
                        row[j] = given.values[i][j]
                    # Fill in the gaps using the helper board.
                    elif given.values[i][j] == 0:
                        row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j]) - 1)]

                # If we don't have a valid board, then try again. max iteration 500,000
                # There must be no duplicates in the row.
                ii = 0
                while len(list(set(row))) != gridSize:
                    ii += 1
                    if ii > 500000:
                        return 0
                    for j in range(0, gridSize):
                        if given.values[i][j] == 0:
                            row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j]) - 1)]

                g.values[i] = row
            self.candidates.append(g)
            
        self.update_fitness()
        return 1

    def update_fitness(self):
        """ Update fitness of every candidate/chromosome. 
        """
        for candidate in self.candidates:

            candidate.update_fitness()
        return

    def sort(self):
        """ Sort the population based on fitness. 
        """
        self.candidates = sorted(self.candidates, key=operator.attrgetter('fitness'))
        return

class Candidate(object):
    """ Candidate class
    
    A candidate solutions to the Sudoku puzzle. 
    """

    def __init__(self):
        self.values = np.zeros((gridSize, gridSize))
        self.fitness = None
        return

    def update_fitness(self):
        column_count = np.zeros(gridSize)
        block_count = np.zeros(gridSize)
        column_sum = 0
        block_sum = 0

        self.values = self.values.astype(int)
        for j in range(0, gridSize):
            for i in range(0, gridSize):
                column_count[self.values[i][j] - 1] += 1

            for k in range(len(column_count)):
                if column_count[k] == 1:
                    column_sum += (1/gridSize)/gridSize
            column_count = np.zeros(gridSize)

        for i in range(0, gridSize, 3):
            for j in range(0, gridSize, 3):
                block_count[self.values[i][j] - 1] += 1
                block_count[self.values[i][j + 1] - 1] += 1
                block_count[self.values[i][j + 2] - 1] += 1

                block_count[self.values[i + 1][j] - 1] += 1
                block_count[self.values[i + 1][j + 1] - 1] += 1
                block_count[self.values[i + 1][j + 2] - 1] += 1

                block_count[self.values[i + 2][j] - 1] += 1
                block_count[self.values[i + 2][j + 1] - 1] += 1
                block_count[self.values[i + 2][j + 2] - 1] += 1

                for k in range(len(block_count)):
                    if block_count[k] == 1:
                        block_sum += (1/gridSize)/gridSize
                block_count = np.zeros(gridSize)

        # Calculate overall fitness.
        if int(column_sum) == 1 and int(block_sum) == 1:
            fitness = 1.0
        else:
            fitness = column_sum * block_sum

        self.fitness = fitness
        return

    def mutate(self, mutation_rate, given):
        """ Mutate a candidate by picking a row, and then picking two values within that row to swap. """

        r = random.uniform(0, 1.1)
        while r > 1:  # Outside [0, 1] boundary - choose another
            r = random.uniform(0, 1.1)

        success = False
        if r < mutation_rate:  # Mutate.
            while not success:
                row1 = random.randint(0, 8)
                row2 = random.randint(0, 8)
                row2 = row1

                from_column = random.randint(0, 8)
                to_column = random.randint(0, 8)
                while from_column == to_column:
                    from_column = random.randint(0, 8)
                    to_column = random.randint(0, 8)

                    # Check if the two places are free to swap
                if given.values[row1][from_column] == 0 and given.values[row1][to_column] == 0:
                    # ...and that we are not causing a duplicate in the rows' columns.
                    if not given.is_column_duplicate(to_column, self.values[row1][from_column]) and not given.is_column_duplicate(from_column, self.values[row2][to_column]) and not given.is_block_duplicate(row2, to_column, self.values[row1][from_column]) and not given.is_block_duplicate(row1, from_column, self.values[row2][to_column]):
                        # Swap values.
                        temp = self.values[row2][to_column]
                        self.values[row2][to_column] = self.values[row1][from_column]
                        self.values[row1][from_column] = temp
                        success = True

        return success


class Given(Candidate):
    """ Given class
    
    Given values. 
    """

    def __init__(self, values):
        self.values = values
        return

    def is_row_duplicate(self, row, value):
        """ Check duplicate in a row. """
        for column in range(0, gridSize):
            if self.values[row][column] == value:
                return True
        return False

    def is_column_duplicate(self, column, value):
        """ Check duplicate in a column. """
        for row in range(0, gridSize):
            if self.values[row][column] == value:
                return True
        return False

    def is_block_duplicate(self, row, column, value):
        """ Check duplicate in a 3 x 3 block. """
        i = 3 * (int(row / 3))
        j = 3 * (int(column / 3))

        if ((self.values[i][j] == value)
            or (self.values[i][j + 1] == value)
            or (self.values[i][j + 2] == value)
            or (self.values[i + 1][j] == value)
            or (self.values[i + 1][j + 1] == value)
            or (self.values[i + 1][j + 2] == value)
            or (self.values[i + 2][j] == value)
            or (self.values[i + 2][j + 1] == value)
            or (self.values[i + 2][j + 2] == value)):
            return True
        else:
            return False

    def make_index(self, v):
        if v <= 2:
            return 0
        elif v <= 5:
            return 3
        else:
            return 6

    def no_duplicates(self):
        for row in range(0, gridSize):
            for col in range(0, gridSize):
                if self.values[row][col] != 0:

                    cnt1 = list(self.values[row]).count(self.values[row][col])
                    cnt2 = list(self.values[:,col]).count(self.values[row][col])

                    block_values = [y[self.make_index(col):self.make_index(col)+3] for y in
                                    self.values[self.make_index(row):self.make_index(row)+3]]
                    block_values_ = [int(x) for y in block_values for x in y]
                    cnt3 = block_values_.count(self.values[row][col])

                    if cnt1 > 1 or cnt2 > 1 or cnt3 > 1:
                        return False
        return True

class Tournament(object):
    """ Tournament class

    """
    def __init__(self):
        return

    def compete(self, candidates):
        """ Pick 2 random candidates from the population and get them to compete against each other. """
        c1 = candidates[random.randint(0, len(candidates) - 1)]
        c2 = candidates[random.randint(0, len(candidates) - 1)]
        f1 = c1.fitness
        f2 = c2.fitness

        # Find the fittest and the weakest.
        if (f1 > f2):
            fittest = c1
            weakest = c2
        else:
            fittest = c2
            weakest = c1

        # selection_rate = 0.85
        selection_rate = 0.80
        r = random.uniform(0, 1.1)
        while (r > 1):  # Outside [0, 1] boundary. Choose another.
            r = random.uniform(0, 1.1)
        if (r < selection_rate):
            return fittest
        else:
            return weakest


class CycleCrossover(object):
    """ CycleCrossover class
    
    """

    def __init__(self):
        return

    def crossover(self, parent1, parent2, crossover_rate):
        """ Create two new child candidates by crossing over parent genes. """
        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        child1.values = np.copy(parent1.values)
        child2.values = np.copy(parent2.values)

        r = random.uniform(0, 1.1)
        while (r > 1):  # Outside [0, 1] boundary. Choose another.
            r = random.uniform(0, 1.1)

        # Perform crossover.
        if (r < crossover_rate):
            # Pick a crossover point. Crossover must have at least 1 row (and at most gridSize-1) rows.
            crossover_point1 = random.randint(0, 8)
            crossover_point2 = random.randint(1, 9)
            while (crossover_point1 == crossover_point2):
                crossover_point1 = random.randint(0, 8)
                crossover_point2 = random.randint(1, 9)

            if (crossover_point1 > crossover_point2):
                temp = crossover_point1
                crossover_point1 = crossover_point2
                crossover_point2 = temp

            for i in range(crossover_point1, crossover_point2):
                child1.values[i], child2.values[i] = self.crossover_rows(child1.values[i], child2.values[i])

        return child1, child2

    def crossover_rows(self, row1, row2):
        child_row1 = np.zeros(gridSize)
        child_row2 = np.zeros(gridSize)

        remaining = range(1, gridSize + 1)
        cycle = 0

        while ((0 in child_row1) and (0 in child_row2)):  # While child rows not complete...
            if (cycle % 2 == 0):  # Even cycles.
                # Assign next unused value.
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child_row1[index] = row1[index]
                child_row2[index] = row2[index]
                next = row2[index]

                while (next != start):  # While cycle not done...
                    index = self.find_value(row1, next)
                    child_row1[index] = row1[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row2[index]
                    next = row2[index]

                cycle += 1

            else:  # Odd cycle - flip values.
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child_row1[index] = row2[index]
                child_row2[index] = row1[index]
                next = row2[index]

                while (next != start):  # While cycle not done...
                    index = self.find_value(row1, next)
                    child_row1[index] = row2[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row1[index]
                    next = row2[index]

                cycle += 1

        return child_row1, child_row2

    def find_unused(self, parent_row, remaining):
        for i in range(0, len(parent_row)):
            if (parent_row[i] in remaining):
                return i

    def find_value(self, parent_row, value):
        for i in range(0, len(parent_row)):
            if (parent_row[i] == value):
                return i