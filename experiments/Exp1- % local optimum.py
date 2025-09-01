import random
import matplotlib.pyplot as plt
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def generate_instances(num_variables, num_clauses, num_vars_in_clause, num_of_instances):
    instances = []
    variables_range = range(1, num_variables + 1)
    for _ in range(num_of_instances):
        instance = []
        for _ in range(num_clauses):
            clause_variables = random.sample(variables_range, num_vars_in_clause)
            clause = [f"x{i}" if random.choice([True, False]) else f"not x{i}" for i in clause_variables]
            instance.append(f"({' or '.join(clause)})")
        instances.append(instance)
    return instances


def count_successful_clauses(instance, values):
    def evaluate_clause(clause):
        literals = clause.replace("(", "").replace(")", "").split(" or ")
        for literal in literals:
            literal = literal.strip()
            if "not " in literal:
                var = literal.split("not ")[1]
                if not values[var]:
                    return True
            else:
                if values[literal]:
                    return True
        return False

    return sum(evaluate_clause(clause) for clause in instance)


def generate_random_config(num_variables):
    return {f"x{i}": random.choice([True, False]) for i in range(1, num_variables + 1)}


def generate_neighbors(config):
    neighbors = []
    for var in config:
        neighbor = config.copy()
        neighbor[var] = not neighbor[var]
        neighbors.append(neighbor)
    return neighbors


def is_local_optimum(config, instance, strictly_greater):
    main_count = count_successful_clauses(instance, config)
    neighbors = generate_neighbors(config)

    # Находим соседа с максимальным количеством успешных клауз
    best_neighbor_count = None
    for neighbor in neighbors:
        neighbor_count = count_successful_clauses(instance, neighbor)
        if best_neighbor_count is None or neighbor_count > best_neighbor_count:
            best_neighbor_count = neighbor_count

    if strictly_greater:
        # Локальный оптимум, если best_neighbor_count < main_count
        return (best_neighbor_count is not None and best_neighbor_count < main_count) or (best_neighbor_count is None)
    else:
        # Локальный оптимум, если best_neighbor_count <= main_count
        # То есть нет соседа лучше
        return (best_neighbor_count is not None and best_neighbor_count <= main_count) or (best_neighbor_count is None)


def calculate_local_optima_percentage(instances, num_variables, num_configurations, strictly_greater):
    percentages = []
    total_local_optima = 0

    for idx, instance in enumerate(instances, start=1):
        local_optima_count = 0
        local_optima_configs = set()  # Для подсчёта уникальных локальных оптимумов при необходимости
        for _ in range(num_configurations):
            config = generate_random_config(num_variables)
            if is_local_optimum(config, instance, strictly_greater):
                local_optima_count += 1
        percentage = local_optima_count / num_configurations
        percentages.append(percentage)
        total_local_optima += local_optima_count
        logging.info(
            f"Instance {idx}: {local_optima_count} local optima out of {num_configurations} ({percentage * 100:.2f}%)")

    logging.info(f"Total local optima (not necessarily unique across all instances): {total_local_optima}")
    return percentages


def plot_histogram(percentages, title):
    # Строим гистограмму без фиксированного range=(0,1), чтобы понять реальные пределы данных
    data, bins = np.histogram(percentages, bins=20)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    plt.figure(figsize=(7, 5))
    plt.bar(bin_centers, data / np.sum(data), width=np.diff(bins), alpha=0.75,
            edgecolor='black', align='center')


    # plt.axvline(mean_val, color='red', linestyle='--', label=f'Mean = {mean_val:.2f}')

    # Определяем границы оси X по данным
    min_val = min(percentages)
    max_val = max(percentages)
    data_range = max_val - min_val

    # Чтобы "центрировать" данные, возьмем расстояние от среднего до крайних значений
    dist = max(mean_val - min_val, max_val - mean_val)

    # Если данные слишком близко к краю, расширим диапазон:
    if dist < 0.1:
        dist = 0.1  # Минимальная половина диапазона
    left = mean_val - dist
    right = mean_val + dist

    # Гарантируем, что [left, right] лежит в пределах [0,1], если вам это нужно:
    # Если вы хотите сохранять диапазон [0,1], можете убрать эти проверки.
    if left < 0:
        left = 0
    if right > 1:
        right = 1
    if left == right:  # На случай если все данные одинаковы
        left = 0
        right = 0.1

    plt.xlim(left, right)

    # Добавим линию центра 0.5 для наглядности, если range (0..1) имеет смысл:
    # Если в итоге диапазон меньше чем [0,1], можно убрать эту линию.
    if right - left > 0.5:  # Есть место для центра
        center = (left + right) / 2
        plt.axvline(center, color='blue', linestyle=':', label=f'Center ~ {center:.2f}')

    plt.xlabel('Local Optimality Ratio')
    plt.ylabel('Relative Frequency')
    plt.title(title)
    plt.grid(axis='both')
    plt.legend()
    plt.show()



if __name__ == '__main__':
    num_variables = 10
    num_clauses = 50
    num_vars_in_clause = 3
    num_of_instances = 5
    num_configurations = 1000000

    instances = generate_instances(num_variables, num_clauses, num_vars_in_clause, num_of_instances)

    logging.info("Calculating for Strictly Greater...")
    percentages_strictly_greater = calculate_local_optima_percentage(
        instances, num_variables, num_configurations, strictly_greater=True
    )

    logging.info("Calculating for Greater or Equal...")
    percentages_greater_or_equal = calculate_local_optima_percentage(
        instances, num_variables, num_configurations, strictly_greater=False
    )

    plot_histogram(percentages_strictly_greater, 'Strictly Greater')
    plot_histogram(percentages_greater_or_equal, 'Greater or Equal')
