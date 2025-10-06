"""
Algorithme Génétique
"""

import random
from typing import Any, Tuple, List
from .base import Algorithm
from src.problems.base import OptimizationProblem


class GeneticAlgorithm(Algorithm):
    """
    Algorithme Génétique
    - Population de solutions
    - Sélection, croisement, mutation
    - Évolution sur plusieurs générations
    """

    def __init__(self, problem: OptimizationProblem,
                 population_size: int = 50,
                 generations: int = 100,
                 crossover_rate: float = 0.8,
                 mutation_rate: float = 0.1,
                 elitism: int = 2):
        super().__init__(problem, "Genetic Algorithm")
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism = elitism

    def solve(self) -> Tuple[Any, float]:
        # Population initiale
        population = [self.problem.random_solution()
                      for _ in range(self.population_size)]

        for generation in range(self.generations):
            # Évaluation
            fitness = [self.problem.evaluate(ind) for ind in population]

            # Meilleur individu
            best_idx = fitness.index(max(fitness))
            best = population[best_idx]
            best_value = fitness[best_idx]

            self.convergence_history.append(best_value)

            # Nouvelle population
            new_population = []

            # Élitisme
            sorted_pop = sorted(zip(population, fitness),
                                key=lambda x: x[1], reverse=True)
            new_population.extend([ind for ind, _ in sorted_pop[:self.elitism]])

            # Génération de nouveaux individus
            while len(new_population) < self.population_size:
                # Sélection par tournoi
                parent1 = self._tournament_selection(population, fitness)
                parent2 = self._tournament_selection(population, fitness)

                # Croisement
                if random.random() < self.crossover_rate:
                    child1, child2 = self._crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2

                # Mutation
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)

                new_population.extend([child1, child2])

            population = new_population[:self.population_size]

        # Retourner le meilleur
        fitness = [self.problem.evaluate(ind) for ind in population]
        best_idx = fitness.index(max(fitness))
        return population[best_idx], fitness[best_idx]

    def _tournament_selection(self, population: List, fitness: List, k: int = 3):
        """Sélection par tournoi"""
        tournament = random.sample(list(zip(population, fitness)), k)
        winner = max(tournament, key=lambda x: x[1])
        return winner[0]

    def _crossover(self, parent1, parent2):
        """Croisement uniforme"""
        if isinstance(parent1, list):
            child1 = [p1 if random.random() < 0.5 else p2
                      for p1, p2 in zip(parent1, parent2)]
            child2 = [p2 if random.random() < 0.5 else p1
                      for p1, p2 in zip(parent1, parent2)]

            # Réparer si nécessaire
            if not self.problem.is_feasible(child1):
                child1 = self.problem.random_solution()
            if not self.problem.is_feasible(child2):
                child2 = self.problem.random_solution()

            return child1, child2
        else:
            return parent1, parent2

    def _mutate(self, individual):
        """Mutation"""
        if random.random() < self.mutation_rate:
            return self.problem.get_neighbor(individual)
        return individual