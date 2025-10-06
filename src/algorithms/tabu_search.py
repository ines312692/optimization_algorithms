"""
Algorithme de Recherche Tabou
"""

from typing import Any, Tuple, List
import copy
from .base import Algorithm
from src.problems.base import OptimizationProblem


class TabuSearch(Algorithm):
    """
    Recherche Tabou (Tabu Search)
    - Maintient une liste de mouvements interdits (tabous)
    - Critère d'aspiration pour accepter un mouvement tabou
    """

    def __init__(self, problem: OptimizationProblem,
                 tabu_tenure: int = 10,
                 max_iterations: int = 500):
        super().__init__(problem, "Tabu Search")
        self.tabu_tenure = tabu_tenure
        self.max_iterations = max_iterations
        self.tabu_list = []

    def solve(self) -> Tuple[Any, float]:
        # Solution initiale
        current = self.problem.random_solution()
        current_value = self.problem.evaluate(current)

        best = copy.deepcopy(current)
        best_value = current_value

        self.convergence_history = [best_value]

        for iteration in range(self.max_iterations):
            # Générer plusieurs voisins
            neighbors = [self.problem.get_neighbor(current) for _ in range(20)]

            # Trouver le meilleur voisin non tabou
            best_neighbor = None
            best_neighbor_value = -float('inf')
            best_move = None

            for i, neighbor in enumerate(neighbors):
                value = self.problem.evaluate(neighbor)
                move = str(neighbor)  # Représentation simplifiée du mouvement

                # Critère d'aspiration
                is_tabu = move in self.tabu_list
                aspiration = value > best_value

                if (not is_tabu or aspiration) and value > best_neighbor_value:
                    best_neighbor = neighbor
                    best_neighbor_value = value
                    best_move = move

            if best_neighbor is None:
                break

            # Mettre à jour
            current = best_neighbor
            current_value = best_neighbor_value

            # Ajouter à la liste taboue
            self.tabu_list.append(best_move)
            if len(self.tabu_list) > self.tabu_tenure:
                self.tabu_list.pop(0)

            # Mettre à jour le meilleur
            if current_value > best_value:
                best = copy.deepcopy(current)
                best_value = current_value

            self.convergence_history.append(best_value)

        return best, best_value
