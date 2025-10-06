"""
Branch & Bound (méthode exacte pour petites instances)
"""

from typing import Any, Tuple
from .base import Algorithm
from src.problems.base import OptimizationProblem
from src.problems.knapsack import KnapsackProblem


class BranchAndBound(Algorithm):
    """
    Branch & Bound pour Knapsack
    Méthode exacte (lente pour grandes instances)
    """

    def __init__(self, problem: KnapsackProblem, max_nodes: int = 100000):
        super().__init__(problem, "Branch & Bound")
        self.max_nodes = max_nodes
        self.nodes_explored = 0

    def solve(self) -> Tuple[Any, float]:
        if not isinstance(self.problem, KnapsackProblem):
            raise ValueError("B&B implémenté uniquement pour Knapsack")

        n = self.problem.n
        best_solution = [0] * n
        best_value = 0

        def bound(level, current_weight, current_value, items_remaining):
            """Borne supérieure relaxée (fractionnaire)"""
            if current_weight > self.problem.capacity:
                return 0

            bound_value = current_value
            weight = current_weight

            for i in items_remaining:
                if weight + self.problem.weights[i] <= self.problem.capacity:
                    weight += self.problem.weights[i]
                    bound_value += self.problem.values[i]
                else:
                    # Fraction de l'objet
                    fraction = (self.problem.capacity - weight) / self.problem.weights[i]
                    bound_value += self.problem.values[i] * fraction
                    break

            return bound_value

        def branch_and_bound_rec(level, current_solution, current_weight, current_value):
            nonlocal best_solution, best_value

            self.nodes_explored += 1
            if self.nodes_explored > self.max_nodes:
                return

            # Solution complète
            if level == n:
                if current_value > best_value:
                    best_solution = current_solution.copy()
                    best_value = current_value
                    self.convergence_history.append(best_value)
                return

            # Items restants
            remaining = list(range(level, n))

            # Branche 1: Prendre l'objet
            if current_weight + self.problem.weights[level] <= self.problem.capacity:
                new_solution = current_solution + [1]
                new_weight = current_weight + self.problem.weights[level]
                new_value = current_value + self.problem.values[level]

                # Élaguer si la borne est mauvaise
                if bound(level + 1, new_weight, new_value, remaining[1:]) > best_value:
                    branch_and_bound_rec(level + 1, new_solution, new_weight, new_value)

            # Branche 2: Ne pas prendre l'objet
            new_solution = current_solution + [0]
            if bound(level + 1, current_weight, current_value, remaining[1:]) > best_value:
                branch_and_bound_rec(level + 1, new_solution, current_weight, current_value)

        branch_and_bound_rec(0, [], 0, 0)

        return best_solution, best_value