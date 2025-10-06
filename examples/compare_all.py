"""
Comprehensive comparison across multiple instances
"""

import pandas as pd
from src.problems.knapsack import KnapsackProblem
from src.algorithms.hill_climbing import HillClimbing
from src.algorithms.simulated_annealing import SimulatedAnnealing
from src.algorithms.tabu_search import TabuSearch
from src.algorithms.genetic_algorithm import GeneticAlgorithm
import matplotlib.pyplot as plt
import seaborn as sns


def run_experiments(num_instances=5, problem_size=20):
    """Run experiments across multiple instances"""

    results_data = []

    for instance_id in range(num_instances):
        print(f"\n{'=' * 60}")
        print(f"Instance {instance_id + 1}/{num_instances}")
        print('=' * 60)

        # Generate an instance
        problem = KnapsackProblem.generate_random(
            n=problem_size,
            seed=instance_id
        )

        # Algorithms to test
        algorithms = [
            ('Hill Climbing', HillClimbing(problem, max_iterations=500)),
            ('Simulated Annealing', SimulatedAnnealing(problem)),
            ('Tabu Search', TabuSearch(problem, max_iterations=300)),
            ('Genetic Algorithm', GeneticAlgorithm(problem, generations=100)),
        ]

        # Run each algorithm
        for algo_name, algo in algorithms:
            print(f"  {algo_name}...", end=' ')
            result = algo.run()

            results_data.append({
                'Instance': instance_id,
                'Algorithm': algo_name,
                'Value': result['best_value'],
                'Time': result['execution_time'],
                'Iterations': result['iterations']
            })

            print(f"({result['best_value']:.1f})")

    return pd.DataFrame(results_data)


def analyze_results(df):
    """Statistical analysis of results"""

    print("\n" + "=" * 60)
    print("STATISTICAL ANALYSIS")
    print("=" * 60)

    # Means by algorithm
    print("\nMeans:")
    print(df.groupby('Algorithm')[['Value', 'Time']].mean().round(4))

    # Standard deviations
    print("\nStandard deviations:")
    print(df.groupby('Algorithm')[['Value', 'Time']].std().round(4))

    # Best results per instance
    print("\nBest per instance:")
    best_per_instance = df.loc[df.groupby('Instance')['Value'].idxmax()]
    print(best_per_instance[['Instance', 'Algorithm', 'Value']])

    # Plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Boxplot of values
    sns.boxplot(data=df, x='Algorithm', y='Value', ax=axes[0, 0])
    axes[0, 0].set_title('Distribution of Values', fontweight='bold')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # 2. Boxplot of times
    sns.boxplot(data=df, x='Algorithm', y='Time', ax=axes[0, 1])
    axes[0, 1].set_title('Distribution of Times', fontweight='bold')
    axes[0, 1].tick_params(axis='x', rotation=45)

    # 3. Scatter: Value vs Time
    for algo in df['Algorithm'].unique():
        data = df[df['Algorithm'] == algo]
        axes[1, 0].scatter(data['Time'], data['Value'], label=algo, s=100, alpha=0.6)
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylabel('Value')
    axes[1, 0].set_title('Quality-Time Trade-off', fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # 4. Bar plot of means
    means = df.groupby('Algorithm')['Value'].mean().sort_values(ascending=False)
    axes[1, 1].bar(range(len(means)), means.values, color='skyblue', edgecolor='navy')
    axes[1, 1].set_xticks(range(len(means)))
    axes[1, 1].set_xticklabels(means.index, rotation=45)
    axes[1, 1].set_ylabel('Average Value')
    axes[1, 1].set_title('Average Performance', fontweight='bold')

    plt.tight_layout()
    plt.savefig('data/results/statistical_analysis.png', dpi=300)
    plt.show()


def main():
    print("=" * 60)
    print("COMPREHENSIVE COMPARATIVE ANALYSIS")
    print("=" * 60)

    # Run experiments
    df = run_experiments(num_instances=10, problem_size=20)

    # Save results
    df.to_csv('data/results/all_results.csv', index=False)
    print("\nResults saved: data/results/all_results.csv")

    # Analyze
    analyze_results(df)

    print("\nAnalysis completed!")
    print("Generated files:")
    print("   - data/results/all_results.csv")
    print("   - data/results/statistical_analysis.png")


if __name__ == "__main__":
    main()