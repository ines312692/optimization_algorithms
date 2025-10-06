"""
Example: Solving the knapsack problem with all algorithms
"""

from src.problems.knapsack import KnapsackProblem
from src.algorithms.hill_climbing import HillClimbing
from src.algorithms.simulated_annealing import SimulatedAnnealing
from src.algorithms.tabu_search import TabuSearch
from src.algorithms.genetic_algorithm import GeneticAlgorithm
from src.algorithms.branch_and_bound import BranchAndBound
from src.visualization.plotter import Plotter


def main():
    print("=" * 60)
    print("ALGORITHM COMPARISON - KNAPSACK PROBLEM")
    print("=" * 60)

    # Create a problem instance
    print("\nGenerating the problem...")
    problem = KnapsackProblem.generate_random(n=15, seed=42)
    print(f"   Items: {problem.n}")
    print(f"   Capacity: {problem.capacity}")
    print(f"   Total weight: {sum(problem.weights)}")
    print(f"   Total value: {sum(problem.values)}")

    # List of algorithms to test
    algorithms = [
        HillClimbing(problem, max_iterations=500),
        SimulatedAnnealing(problem, initial_temp=100, cooling_rate=0.95),
        TabuSearch(problem, tabu_tenure=10, max_iterations=300),
        GeneticAlgorithm(problem, population_size=50, generations=100),
        BranchAndBound(problem, max_nodes=50000),  # Exact
    ]

    # Run all algorithms
    results = []
    print("\nRunning algorithms...")
    print("-" * 60)

    for algo in algorithms:
        print(f"\n▶ {algo.name}...")
        result = algo.run()
        results.append({
            'algorithm': algo.name,
            'best_value': result['best_value'],
            'execution_time': result['execution_time'],
            'iterations': result['iterations'],
            'convergence_history': algo.convergence_history,
            'solution': result['solution']
        })

        print(f"   ✓ Best value: {result['best_value']:.2f}")
        print(f"   ✓ Time: {result['execution_time']:.4f}s")
        print(f"   ✓ Iterations: {result['iterations']}")

    # Show the comparison table
    print("\n" + "=" * 60)
    print(" COMPARATIVE RESULTS")
    print("=" * 60)
    print(f"{'Algorithm':<25} {'Value':<12} {'Time (s)':<12} {'Iterations':<12}")
    print("-" * 60)

    for r in results:
        print(f"{r['algorithm']:<25} {r['best_value']:<12.2f} "
              f"{r['execution_time']:<12.4f} {r['iterations']:<12}")

    # Find the best
    best = max(results, key=lambda x: x['best_value'])
    fastest = min(results, key=lambda x: x['execution_time'])

    print("\n" + "=" * 60)
    print(" WINNERS")
    print("=" * 60)
    print(f" Best solution: {best['algorithm']} ({best['best_value']:.2f})")
    print(f"⚡ Fastest: {fastest['algorithm']} ({fastest['execution_time']:.4f}s)")

    # Visualization
    print("\n Generating charts...")
    plotter = Plotter()

    # Convergence curves
    plotter.plot_convergence(results, save_path='data/results/knapsack_convergence.png')

    # Comparison
    plotter.plot_comparison(results, save_path='data/results/knapsack_comparison.png')

    print("\n Charts saved in data/results/")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()