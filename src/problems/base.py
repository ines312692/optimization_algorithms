"""
Classe abstraite pour définir un problème d'optimisation
"""

from abc import ABC, abstractmethod
from typing import Any, List


class OptimizationProblem(ABC):
    """Classe de base pour tous les problèmes d'optimisation"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def evaluate(self, solution: Any) -> float:
        """Évalue la qualité d'une solution (à maximiser ou minimiser)"""
        pass

    @abstractmethod
    def is_feasible(self, solution: Any) -> bool:
        """Vérifie si une solution est valide"""
        pass

    @abstractmethod
    def random_solution(self) -> Any:
        """Génère une solution aléatoire valide"""
        pass

    @abstractmethod
    def get_neighbor(self, solution: Any) -> Any:
        """Génère une solution voisine"""
        pass

    def __str__(self):
        return f"Problem: {self.name}"