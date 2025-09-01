import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import median_abs_deviation


def generate_instances(num_variables, num_clauses, num_vars_in_clause, num_of_instances):
    instances = []
    for _ in range(num_of_instances):
        instance = []
        for _ in range(num_clauses):
            clause_variables = random.sample(range(1, num_variables + 1), num_vars_in_clause)
            clause = [f"x{i}" if random.choice([True, False]) else f"not x{i}" for i in clause_variables]
            instance.append(f"({' or '.join(clause)})")
        instances.append(instance)
    return instances


def count_successful_clauses(instances, values):
    def evaluate_clause(clause):
        literals = clause.replace("(", "").replace(")", "").split(" or ")
        for literal in literals:
            if "not " in literal:
                var = literal.split("not ")[1]
                if not values[var]:
                    return True
            else:
                if values[literal]:
                    return True
        return False

    total_success = 0
    for instance in instances:
        total_success += sum(evaluate_clause(clause) for clause in instance)
    return total_success


def generate_random_configuration_and_neighbors(num_variables):
    main_config = {f"x{i}": random.choice([True, False]) for i in range(1, num_variables + 1)}
    neighbors = []

    for var in main_config:
        neighbor = main_config.copy()
        neighbor[var] = not neighbor[var]
        neighbors.append(neighbor)

    return main_config, neighbors


def is_local_optimum(config, instances, num_variables):
    main_count = count_successful_clauses(instances, config)
    _, neighbors = generate_random_configuration_and_neighbors(num_variables)
    for neighbor in neighbors:
        neighbor_count = count_successful_clauses(instances, neighbor)
        if neighbor_count >= main_count:
            return False

    return True


def calculate_metrics_for_instance(instance, num_variables, num_configurations):
    neighbors_counts = []  # Изменено на подсчет количества

    for _ in range(num_configurations):
        config, neighbors = generate_random_configuration_and_neighbors(num_variables)
        if is_local_optimum(config, [instance], num_variables):
            height = count_successful_clauses([instance], config)

            same_height_neighbors_count = 0
            for neighbor in neighbors:
                neighbor_height = count_successful_clauses([instance], neighbor)
                if neighbor_height == height:
                    same_height_neighbors_count += 1

            neighbors_counts.append(same_height_neighbors_count)

        if len(neighbors_counts) >= 100:
            break

    if len(neighbors_counts) < 100:
        raise ValueError("Did not find 100 local optima.")

    # Вычисляем метрики для инстанции
    metrics = {
        'mean': np.mean(neighbors_counts),
        'std_dev': np.std(neighbors_counts),
        'median': np.median(neighbors_counts),
        'mad': median_abs_deviation(neighbors_counts)
    }

    return metrics


def visualize_all_metrics(all_metrics, metric_names):
    plt.figure(figsize=(12, 12))
    for i, metric_key in enumerate(metric_names.keys(), 1):
        plt.subplot(2, 2, i)
        plt.hist(all_metrics[metric_key], bins=20, alpha=0.75, color='royalblue', edgecolor='black')
        plt.title(f'Distribution of {metric_names[metric_key]}')
        plt.xlabel(metric_names[metric_key])
        plt.ylabel('Number of Instances')
        plt.grid(True, linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

# Main program
# n
num_variables = 20
# m
num_clauses = 50
# r
num_vars_in_clause = 3

num_of_instances = 100
num_configurations = 10000

instances = generate_instances(num_variables, num_clauses, num_vars_in_clause, num_of_instances)

all_metrics = {'mean': [], 'std_dev': [], 'median': [], 'mad': []}

metric_names = {
    'mean': 'Average Number of Same-Level Neighbors',
    'std_dev': 'Standard Deviation of Same-Level Neighbors',
    'median': 'Median Number of Same-Level Neighbors',
    'mad': 'Median Absolute Deviation of Same-Level Neighbors'
}

for instance in instances:
    try:
        metrics = calculate_metrics_for_instance(instance, num_variables, num_configurations)
        for key in all_metrics.keys():
            all_metrics[key].append(metrics[key])
    except ValueError as e:
        print(e)
        continue

visualize_all_metrics(all_metrics, metric_names)