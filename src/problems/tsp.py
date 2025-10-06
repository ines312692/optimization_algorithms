"""
Problème du Voyageur de Commerce (TSP)
"""

import random
import math
from typing import List, Tuple
from .base import OptimizationProblem


class TSPProblem(OptimizationProblem):
    """
    Travelling Salesman Problem

    Minimiser: la distance totale du tour
    """

    def __init__(self, cities: List[Tuple[float, float]]):
        super().__init__("TSP")
        self.cities = cities
        self.n = len(cities)
        self.distance_matrix = self._compute_distances()

    def _compute_distances(self):
        """Calcule la matrice des distances euclidiennes"""
        n = self.n
        dist = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d = math.sqrt(
                    (self.cities[i][0] - self.cities[j][0]) ** 2 +
                    (self.cities[i][1] - self.cities[j][1]) ** 2
                )
                dist[i][j] = dist[j][i] = d
        return dist

    def evaluate(self, solution: List[int]) -> float:
        """Retourne la distance totale (à minimiser, donc négative)"""
        total_distance = 0
        for i in range(len(solution)):
            j = (i + 1) % len(solution)
            total_distance += self.distance_matrix[solution[i]][solution[j]]
        return -total_distance  # Négatif car on maximise

    def is_feasible(self, solution: List[int]) -> bool:
        """Vérifie que c'est une permutation valide"""
        return (len(solution) == self.n and
                len(set(solution)) == self.n and
                all(0 <= city < self.n for city in solution))

    def random_solution(self) -> List[int]:
        """Génère un tour aléatoire"""
        solution = list(range(self.n))
        random.shuffle(solution)
        return solution

    def get_neighbor(self, solution: List[int]) -> List[int]:
        """2-opt: inverse un segment"""
        neighbor = solution.copy()
        i, j = sorted(random.sample(range(self.n), 2))
        neighbor[i:j + 1] = reversed(neighbor[i:j + 1])
        return neighbor

    @classmethod
    def generate_random(cls, n: int = 20, seed: int = None):
        """Génère une instance aléatoire"""
        if seed:
            random.seed(seed)
        cities = [(random.uniform(0, 100), random.uniform(0, 100))
                  for _ in range(n)]
        return cls(cities)

    def __str__(self):
        return f"TSP(n={self.n} cities)"
