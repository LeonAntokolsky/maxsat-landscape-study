import random
import matplotlib.pyplot as plt
import numpy as np


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


def calculate_local_optima_heights(instances, num_variables, num_configurations):
    all_heights = []
    for instance in instances:
        local_optima_heights = []
        for _ in range(num_configurations):
            config, _ = generate_random_configuration_and_neighbors(num_variables)
            if is_local_optimum(config, [instance], num_variables):
                height = count_successful_clauses([instance], config)
                local_optima_heights.append(height)
        all_heights.append(local_optima_heights)
    return all_heights


def is_local_optimum(config, instances, num_variables):
    main_count = count_successful_clauses(instances, config)
    _, neighbors = generate_random_configuration_and_neighbors(num_variables)
    for neighbor in neighbors:
        neighbor_count = count_successful_clauses(instances, neighbor)
        if neighbor_count > main_count:
            return False
    return True


# Main program
# n
num_variables = 20
# m
num_clauses = 50
# r
num_vars_in_clause = 3

num_of_instances = 100
num_configurations = 1000

instances = generate_instances(num_variables, num_clauses, num_vars_in_clause, num_of_instances)

flattened_optima = [height for sublist in calculate_local_optima_heights(instances, num_variables, num_configurations)
                    for height in sublist]

# Calculate metrics
mean_value = np.mean(flattened_optima)
standard_deviation = np.std(flattened_optima)
median_value = np.median(flattened_optima)
mad = np.mean(np.abs(flattened_optima - mean_value))

# Print results
print(f"Mean: {mean_value}")
print(f"Standard deviation: {standard_deviation}")
print(f"Median: {median_value}")
print(f"Mean Absolute Deviation: {mad}")
