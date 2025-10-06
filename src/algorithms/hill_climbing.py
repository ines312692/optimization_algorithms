"""
Algorithme Hill Climbing (Montée de colline)
"""

from typing import Any, Tuple
from .base import Algorithm
from src.problems.base import OptimizationProblem


class HillClimbing(Algorithm):
    """
    Hill Climbing simple
    - Part d'une solution aléatoire
    - Explore tous les voisins
    - Prend le meilleur voisin si amélioration
    - S'arrête quand aucun voisin n'améliore
    """

    def __init__(self, problem: OptimizationProblem, max_iterations: int = 1000):
        super().__init__(problem, "Hill Climbing")
        self.max_iterations = max_iterations

    def solve(self) -> Tuple[Any, float]:
        # Solution initiale
        current = self.problem.random_solution()
        current_value = self.problem.evaluate(current)

        self.convergence_history = [current_value]

        for iteration in range(self.max_iterations):
            # Générer tous les voisins
            improved = False

            for _ in range(10):  # Essayer plusieurs voisins
                neighbor = self.problem.get_neighbor(current)
                neighbor_value = self.problem.evaluate(neighbor)

                if neighbor_value > current_value:
                    current = neighbor
                    current_value = neighbor_value
                    improved = True
                    break

            self.convergence_history.append(current_value)

            if not improved:
                break  # Optimum local atteint

        return current, current_value