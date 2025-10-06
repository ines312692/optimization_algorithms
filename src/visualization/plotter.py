"""
Visualisation des résultats
"""

import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict


class Plotter:
    """Génère les graphiques de comparaison"""

    def __init__(self):
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)

    def plot_convergence(self, results: List[Dict], save_path: str = None):
        """Graphique de convergence des algorithmes"""
        plt.figure(figsize=(12, 6))

        for result in results:
            algo_name = result['algorithm']
            history = result.get('convergence_history', [])
            if history:
                plt.plot(history, label=algo_name, linewidth=2)

        plt.xlabel('Itération', fontsize=12)
        plt.ylabel('Valeur de la solution', fontsize=12)
        plt.title('Convergence des Algorithmes', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_comparison(self, results: List[Dict], save_path: str = None):
        """Graphique comparatif: valeur vs temps"""
        plt.figure(figsize=(12, 6))

        algorithms = [r['algorithm'] for r in results]
        values = [r['best_value'] for r in results]
        times = [r['execution_time'] for r in results]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Valeurs
        ax1.bar(algorithms, values, color='skyblue', edgecolor='navy')
        ax1.set_ylabel('Valeur de la solution', fontsize=12)
        ax1.set_title('Qualité des Solutions', fontsize=14, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)

        # Temps
        ax2.bar(algorithms, times, color='lightcoral', edgecolor='darkred')
        ax2.set_ylabel('Temps (secondes)', fontsize=12)
        ax2.set_title('Temps d\'Exécution', fontsize=14, fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()


print(" Structure du projet créée avec succès!")
print("\nContenu:")
print("- Problèmes: Knapsack, TSP")
print("- Algorithmes: Hill Climbing, Simulated Annealing, Tabu Search, Genetic Algorithm, Branch & Bound")
print("- Visualisation: Convergence, Comparaison")
print("\nProchaine étape: Voir les exemples d'utilisation")