import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

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
        if neighbor_count > main_count:
            return False
    return True


def find_local_optima_by_height(instance, num_variables, num_configurations, required_count=100):
    heights = {}
    for _ in range(num_configurations):
        config, _ = generate_random_configuration_and_neighbors(num_variables)
        if is_local_optimum(config, [instance], num_variables):
            height = count_successful_clauses([instance], config)
            if height not in heights:
                heights[height] = []
            heights[height].append(config)
            if len(heights[height]) == required_count:
                break
    return heights


def calculate_hamming_distances(optima):
    num_optima = len(optima)
    distances = []
    expected_size = len(optima[0])
    for opt in optima:
        if len(opt) != expected_size:
            raise ValueError("Inconsistent sizes in local optima configurations")

    for i in range(num_optima):
        for j in range(i + 1, num_optima):
            distance = sum(optima[i][k] != optima[j][k] for k in optima[i])
            normalized_distance = distance / expected_size
            distances.append(normalized_distance)
    return distances


def analyze_optima_heights(instances, num_variables, num_configurations):
    distance_means_by_height = {}
    for instance in instances:
        heights = find_local_optima_by_height(instance, num_variables, num_configurations)
        for height, optima in heights.items():
            if len(optima) >= 30:
                distances = calculate_hamming_distances(optima)
                distance_means_by_height[height] = np.mean(distances)
    return distance_means_by_height


def visualize_height_distance_seaborn(distance_means_by_height):
    data = pd.DataFrame({
        "Height": list(distance_means_by_height.keys()),
        "Average Hamming Distance": list(distance_means_by_height.values())
    })

    plt.figure(figsize=(12, 8))
    sns.barplot(x="Height", y="Average Hamming Distance", data=data, palette="Blues_d")
    plt.title('Average Hamming Distance by Local Optima Height')
    plt.xlabel('Height of Local Optima')
    plt.ylabel('Average Hamming Distance')
    plt.xticks(rotation=45)
    plt.grid(True, which='both')
    plt.show()

# n
num_variables = 50
# m
num_clauses = 700
# r
num_vars_in_clause = 3

num_of_instances = 100
num_configurations = 40000

instances = generate_instances(num_variables, num_clauses, num_vars_in_clause, num_of_instances)
distance_means_by_height = analyze_optima_heights(instances, num_variables, num_configurations)
visualize_height_distance_seaborn(distance_means_by_height)
