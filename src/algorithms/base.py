"""
Classe de base pour tous les algorithmes
"""

from abc import ABC, abstractmethod
from typing import Any, Tuple, List
import time
from src.problems.base import OptimizationProblem


class Algorithm(ABC):
    """Classe de base pour tous les algorithmes d'optimisation"""

    def __init__(self, problem: OptimizationProblem, name: str):
        self.problem = problem
        self.name = name
        self.best_solution = None
        self.best_value = -float('inf')
        self.convergence_history = []
        self.execution_time = 0.0

    @abstractmethod
    def solve(self) -> Tuple[Any, float]:
        """
        Résout le problème
        Returns: (meilleure_solution, meilleure_valeur)
        """
        pass

    def run(self) -> dict:
        """Exécute l'algorithme et retourne les résultats"""
        start_time = time.time()
        self.best_solution, self.best_value = self.solve()
        self.execution_time = time.time() - start_time

        return {
            'algorithm': self.name,
            'problem': str(self.problem),
            'best_value': self.best_value,
            'execution_time': self.execution_time,
            'iterations': len(self.convergence_history),
            'solution': self.best_solution
        }

    def __str__(self):
        return f"{self.name} on {self.problem}"