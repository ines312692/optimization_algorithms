"""
Example: Solving the TSP with metaheuristics
"""

from src.problems.tsp import TSPProblem
from src.algorithms.hill_climbing import HillClimbing
from src.algorithms.simulated_annealing import SimulatedAnnealing
from src.algorithms.tabu_search import TabuSearch
from src.algorithms.genetic_algorithm import GeneticAlgorithm
from src.visualization.plotter import Plotter
import matplotlib.pyplot as plt


def visualize_tour(problem, solution, title="Tour"):
    """Visualize a TSP tour"""
    cities = problem.cities
    tour = solution + [solution[0]]  # Close the tour

    plt.figure(figsize=(10, 10))

    # Draw the cities
    x_coords = [cities[i][0] for i in range(len(cities))]
    y_coords = [cities[i][1] for i in range(len(cities))]
    plt.scatter(x_coords, y_coords, c='red', s=100, zorder=2)

    # Label the cities
    for i, (x, y) in enumerate(cities):
        plt.annotate(str(i), (x, y), fontsize=12, ha='center')

    # Draw the tour
    tour_x = [cities[i][0] for i in tour]
    tour_y = [cities[i][1] for i in tour]
    plt.plot(tour_x, tour_y, 'b-', linewidth=2, alpha=0.7, zorder=1)

    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def main():
    print("=" * 60)
    print("ALGORITHM COMPARISON - TSP")
    print("=" * 60)

    # Create a problem instance
    print("\nGenerating the TSP problem...")
    problem = TSPProblem.generate_random(n=20, seed=42)
    print(f"   Number of cities: {problem.n}")

    # List of algorithms
    algorithms = [
        HillClimbing(problem, max_iterations=1000),
        SimulatedAnnealing(problem, initial_temp=1000, cooling_rate=0.98),
        TabuSearch(problem, tabu_tenure=15, max_iterations=500),
        GeneticAlgorithm(problem, population_size=100, generations=200),
    ]

    # Run the algorithms
    results = []
    print("\nRunning the algorithms...")
    print("-" * 60)

    for algo in algorithms:
        print(f"\n{algo.name}...")
        result = algo.run()
        results.append({
            'algorithm': algo.name,
            'best_value': -result['best_value'],  # Convert back to positive
            'execution_time': result['execution_time'],
            'iterations': result['iterations'],
            'convergence_history': [-v for v in algo.convergence_history],
            'solution': result['solution']
        })

        print(f"   Total distance: {-result['best_value']:.2f}")
        print(f"   Time: {result['execution_time']:.4f}s")

    # Comparative table
    print("\n" + "=" * 60)
    print("COMPARATIVE RESULTS")
    print("=" * 60)
    print(f"{'Algorithm':<25} {'Distance':<15} {'Time (s)':<12}")
    print("-" * 60)

    for r in results:
        print(f"{r['algorithm']:<25} {r['best_value']:<15.2f} "
              f"{r['execution_time']:<12.4f}")

    # Best
    best = min(results, key=lambda x: x['best_value'])
    print(f"\nBest tour: {best['algorithm']} ({best['best_value']:.2f})")

    # Visualize the best tour
    print("\nVisualizing the best tour...")
    visualize_tour(problem, best['solution'],
                   f"Best Tour - {best['algorithm']}")

    # Convergence
    plotter = Plotter()
    plotter.plot_convergence(results, save_path='data/results/tsp_convergence.png')

    print("\nDone!")


if __name__ == "__main__":
    main()