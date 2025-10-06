"""
Problème du Sac à Dos (Knapsack Problem)
"""

import random
from typing import List
from .base import OptimizationProblem


class KnapsackProblem(OptimizationProblem):
    """
    Problème du sac à dos 0-1

    Maximiser: sum(values[i] * x[i])
    Contrainte: sum(weights[i] * x[i]) <= capacity
    où x[i] ∈ {0, 1}
    """

    def __init__(self, weights: List[int], values: List[int], capacity: int):
        super().__init__("Knapsack Problem")
        self.weights = weights
        self.values = values
        self.capacity = capacity
        self.n = len(weights)
        self.optimal_value = None  # Si connu

    def evaluate(self, solution: List[int]) -> float:
        """Retourne la valeur totale (ou -inf si invalide)"""
        if not self.is_feasible(solution):
            return -float('inf')
        return sum(v * s for v, s in zip(self.values, solution))

    def is_feasible(self, solution: List[int]) -> bool:
        """Vérifie la contrainte de capacité"""
        total_weight = sum(w * s for w, s in zip(self.weights, solution))
        return total_weight <= self.capacity

    def random_solution(self) -> List[int]:
        """Génère une solution aléatoire faisable"""
        solution = [0] * self.n
        for i in random.sample(range(self.n), self.n):
            solution[i] = 1
            if not self.is_feasible(solution):
                solution[i] = 0
        return solution

    def get_neighbor(self, solution: List[int]) -> List[int]:
        """Flip un bit aléatoire"""
        neighbor = solution.copy()
        i = random.randint(0, self.n - 1)
        neighbor[i] = 1 - neighbor[i]
        return neighbor if self.is_feasible(neighbor) else solution

    def get_all_neighbors(self, solution: List[int]) -> List[List[int]]:
        """Retourne tous les voisins valides"""
        neighbors = []
        for i in range(self.n):
            neighbor = solution.copy()
            neighbor[i] = 1 - neighbor[i]
            if self.is_feasible(neighbor):
                neighbors.append(neighbor)
        return neighbors

    @classmethod
    def generate_random(cls, n: int = 20, seed: int = None):
        """Génère une instance aléatoire"""
        if seed:
            random.seed(seed)

        weights = [random.randint(1, 50) for _ in range(n)]
        values = [random.randint(1, 100) for _ in range(n)]
        capacity = int(sum(weights) * 0.5)

        return cls(weights, values, capacity)

    def __str__(self):
        return f"Knapsack(n={self.n}, capacity={self.capacity})"