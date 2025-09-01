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


def is_local_optimum(config, instances, num_variables):
    main_count = count_successful_clauses(instances, config)
    _, neighbors = generate_random_configuration_and_neighbors(num_variables)

    for neighbor in neighbors:
        neighbor_count = count_successful_clauses(instances, neighbor)
        if neighbor_count >= main_count:  # Изменено условие с > на >=
            # Если хоть один сосед имеет не меньше успешных клауз, это не локальный оптимум
            return False
    # Если ни одно из условий выше не выполнено, значит, основная конфигурация лучше всех соседей
    return True


def calculate_local_optima_and_neighbor_percentage(instance, num_variables, num_configurations):
    local_optima_counts = []
    neighbor_percentages = []

    for _ in range(num_configurations):
        config, neighbors = generate_random_configuration_and_neighbors(num_variables)
        if is_local_optimum(config, [instance], num_variables):
            height = count_successful_clauses([instance], config)
            local_optima_counts.append(height)

            same_height_neighbors_count = 0
            total_neighbors_count = 0
            for neighbor in neighbors:
                neighbor_height = count_successful_clauses([instance], neighbor)
                total_neighbors_count += 1
                if neighbor_height == height:
                    same_height_neighbors_count += 1

            percentage = (same_height_neighbors_count / total_neighbors_count) if total_neighbors_count > 0 else 0
            neighbor_percentages.append(percentage)

    return local_optima_counts, neighbor_percentages


# Main program
# n
num_variables = 40
# m
num_clauses = 200
# r
num_vars_in_clause = 3

num_of_instances = 100
num_configurations = 10000

instances = generate_instances(num_variables, num_clauses, num_vars_in_clause, num_of_instances)

neighbor_percentages_all_instances = []
local_optima_counts_all_instances = []

for instance in instances:
    local_optima_counts, neighbor_percentages = calculate_local_optima_and_neighbor_percentage(instance, num_variables,
                                                                                               num_configurations)
    local_optima_counts_all_instances.extend(local_optima_counts)
    neighbor_percentages_all_instances.extend(neighbor_percentages)

total_local_optima = len(neighbor_percentages_all_instances)

weights = np.ones_like(
    neighbor_percentages_all_instances) / total_local_optima  # Нормализация на общее количество конфигураций

plt.figure(figsize=(12, 6))
plt.hist(neighbor_percentages_all_instances, bins=20, weights=weights, alpha=0.75, edgecolor='black')
mean_value = np.mean(neighbor_percentages_all_instances)
plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1)
plt.text(mean_value * 1.05, plt.ylim()[1] * 0.95, 'Mean: {:.2f}'.format(mean_value), color='red')

plt.title('The distribution of local optima by ratio of same-height neighbors')
plt.xlabel('Normalized Percentage of Neighbors with the Same Height')
plt.ylabel('Normalized Number of Local Optima')
plt.grid(True, which='both')
plt.show()
