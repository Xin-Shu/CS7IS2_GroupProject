"""_geneticSolver.py_

Definations of class SudokuSolver
"""

from scripts.gene import *


class SudokuSolver(object):
    """SudokuSolver
    
    Solves a given Sudoku puzzle using a genetic algorithm. 
    
    """

    def __init__(self):
        self.given = None
        return

    def solve(self, gird, populations=1000, generations=10000, mutation_rate=0.05):
        """Solve sudoku using genetic algorithm

        Args:
            gird (List): Input sudoku grid
            populations (int, optional): Number of initial population. Defaults to 1000.
            generations (int, optional): Number of generations. Defaults to 10000.
            mutation_rate (float, optional): Mutation ratio. Defaults to 0.05.

        Returns:
            List: Solution (Return empty list if no solution)
        """
        self.given = Given(gird)    # Load from gird
        numelites = int(0.05 * populations)
        mutations = 0
        phi = 0
        sigma = 1

        # Check given one first
        if not self.given.no_duplicates():
            return []

        # Create initial population
        self.population = Population()
        if self.population.seed(populations, self.given) == 1:
            pass
        else:
            return []

        stale = 0
        for generation in range(0, generations):

            # Check for a solution
            best_fitness = 0.0
            for c in range(0, populations):
                fitness = self.population.candidates[c].fitness
                if (fitness == 1):
                    print("Solution found! (generation=%d)" % generation)
                    return self.population.candidates[c]

                # Find the best fitness and corresponding chromosome
                if (fitness > best_fitness):
                    best_fitness = fitness

            # Create the next population
            next_population = []

            # Select elites (the fittest candidates) and preserve them for the next generation
            self.population.sort()
            elites = []
            for e in range(0, numelites):
                elite = Candidate()
                elite.values = np.copy(self.population.candidates[e].values)
                elites.append(elite)

            # Create the rest of the candidates.
            for count in range(numelites, populations, 2):
                # Select parents from population via a tournament.
                t = Tournament()
                parent1 = t.compete(self.population.candidates)
                parent2 = t.compete(self.population.candidates)

                ## Cross-over.
                cc = CycleCrossover()
                child1, child2 = cc.crossover(parent1, parent2, crossover_rate=1.0)

                # Mutate child1.
                child1.update_fitness()
                old_fitness = child1.fitness
                success = child1.mutate(mutation_rate, self.given)
                child1.update_fitness()
                if (success):
                    mutations += 1
                    if (child1.fitness > old_fitness):  # Used to calculate the relative success rate of mutations.
                        phi = phi + 1

                # Mutate child2.
                child2.update_fitness()
                old_fitness = child2.fitness
                success = child2.mutate(mutation_rate, self.given)
                child2.update_fitness()
                if (success):
                    mutations += 1
                    if (child2.fitness > old_fitness):  # Used to calculate the relative success rate of mutations.
                        phi = phi + 1

                # Add children to new population.
                next_population.append(child1)
                next_population.append(child2)

            # Append elites onto the end of the population. These will not have been affected by crossover or mutation.
            for e in range(0, numelites):
                next_population.append(elites[e])

            # Select next generation.
            self.population.candidates = next_population
            self.population.update_fitness()

            # Calculate new adaptive mutation rate (based on Rechenberg's 1/5 success rule).
            # This is to stop too much mutation as the fitness progresses towards unity.
            if (mutations == 0):
                phi = 0
            else:
                phi = phi / mutations

            if (phi > 0.2):
                sigma = sigma / 0.998
            elif (phi < 0.2):
                sigma = sigma * 0.998

            mutation_rate = abs(np.random.normal(loc=0.0, scale=sigma, size=None))

            # Check for stale population.
            self.population.sort()
            if (self.population.candidates[0].fitness != self.population.candidates[1].fitness):
                stale = 0
            else:
                stale += 1

            # Re-seed the population if 100 generations have passed
            # with the fittest two candidates always having the same fitness.
            if (stale >= 100):
                self.population.seed(populations, self.given)
                stale = 0
                sigma = 1
                phi = 0
                mutation_rate = 0.06

        print("No solution was found")
        return []