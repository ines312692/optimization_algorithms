"""
Algorithme de Recuit Simulé
"""

import random
import math
from typing import Any, Tuple
from .base import Algorithm
from src.problems.base import OptimizationProblem


class SimulatedAnnealing(Algorithm):
    """
    Recuit Simulé (Simulated Annealing)
    - Accepte des solutions dégradantes avec probabilité décroissante
    - Permet d'échapper aux optimums locaux
    """

    def __init__(self, problem: OptimizationProblem,
                 initial_temp: float = 100.0,
                 cooling_rate: float = 0.95,
                 min_temp: float = 0.01,
                 iterations_per_temp: int = 100):
        super().__init__(problem, "Simulated Annealing")
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.iterations_per_temp = iterations_per_temp

    def solve(self) -> Tuple[Any, float]:
        # Solution initiale
        current = self.problem.random_solution()
        current_value = self.problem.evaluate(current)

        best = current
        best_value = current_value

        temperature = self.initial_temp
        self.convergence_history = [best_value]

        while temperature > self.min_temp:
            for _ in range(self.iterations_per_temp):
                # Générer un voisin
                neighbor = self.problem.get_neighbor(current)
                neighbor_value = self.problem.evaluate(neighbor)

                # Critère de Metropolis
                delta = neighbor_value - current_value

                if delta > 0 or random.random() < math.exp(delta / temperature):
                    current = neighbor
                    current_value = neighbor_value

                    if current_value > best_value:
                        best = current
                        best_value = current_value

            temperature *= self.cooling_rate
            self.convergence_history.append(best_value)

        return best, best_value
