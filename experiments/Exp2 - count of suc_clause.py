import random
import matplotlib.pyplot as plt
import numpy as np
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


class Configuration:
    def __init__(self, num_variables, values=None):
        self.num_variables = num_variables
        if values is not None:
            self.values = values
        else:
            self.values = {f"x{i + 1}": random.choice([True, False]) for i in range(num_variables)}

    def evaluate_clause(self, clause):
        literals = clause.replace("(", "").replace(")", "").split(" or ")
        for literal in literals:
            literal = literal.strip()
            if literal.startswith("not "):
                var = literal[4:].strip()
                if not self.values.get(var, False):
                    return True
            else:
                if self.values.get(literal, False):
                    return True
        return False

    def count_successful_clauses(self, clauses):
        return sum(self.evaluate_clause(clause) for clause in clauses)

    def generate_neighbors(self):
        neighbors = []
        for var in self.values:
            neighbor_values = self.values.copy()
            neighbor_values[var] = not neighbor_values[var]
            neighbor = Configuration(self.num_variables, neighbor_values)
            neighbors.append(neighbor)
        return neighbors


class Instance:
    def __init__(self, num_variables, num_clauses, num_vars_in_clause):
        self.num_variables = num_variables
        self.num_clauses = num_clauses
        self.clauses = [self.generate_clause(num_vars_in_clause) for _ in range(num_clauses)]

    def generate_clause(self, num_vars_in_clause):
        clause_variables = random.sample(range(1, self.num_variables + 1), num_vars_in_clause)
        clause = [f"x{i}" if random.choice([True, False]) else f"not x{i}" for i in clause_variables]
        return f"({' or '.join(clause)})"

    def is_local_optimum(self, config, strictly_greater):
        main_count = config.count_successful_clauses(self.clauses)
        neighbors = config.generate_neighbors()
        for neighbor in neighbors:
            neighbor_count = neighbor.count_successful_clauses(self.clauses)
            if strictly_greater:
                if main_count <= neighbor_count:
                    return False
            else:
                if main_count < neighbor_count:
                    return False
        return True

    def calculate_local_optima_distribution(self, num_configurations, strictly_greater):
        local_optima_heights = []
        for i in range(num_configurations):
            # Генерируем случайную конфигурацию
            config = Configuration(self.num_variables)
            # Проверяем, является ли конфигурация локальным оптимумом
            is_optimum = self.is_local_optimum(config, strictly_greater)
            if is_optimum:
                # Считаем число удовлетворённых клауз
                height = config.count_successful_clauses(self.clauses)
                local_optima_heights.append(height)
            if i % (max(num_configurations // 10, 1)) == 0 and i > 0:
                logging.info(f"Instance progress: {i}/{num_configurations} configurations checked")
        logging.info(f"Instance completed: {len(local_optima_heights)} local optima found out of {num_configurations}")
        return local_optima_heights


class Simulation:
    def __init__(self, num_variables, num_clauses, num_vars_in_clause, num_instances, num_configurations):
        self.num_variables = num_variables
        self.num_clauses = num_clauses
        self.num_vars_in_clause = num_vars_in_clause
        self.num_instances = num_instances
        self.num_configurations = num_configurations
        self.instances = [Instance(num_variables, num_clauses, num_vars_in_clause) for _ in range(num_instances)]

    def run(self, strictly_greater):
        all_local_optima_heights = []
        total_local_optima = 0  # Добавляем переменную для общего числа локальных оптимумов
        for idx, instance in enumerate(self.instances):
            logging.info(f"Starting instance {idx + 1}/{self.num_instances}")
            local_optima_heights = instance.calculate_local_optima_distribution(
                self.num_configurations, strictly_greater
            )
            all_local_optima_heights.extend(local_optima_heights)
            total_local_optima += len(local_optima_heights)  # Суммируем количество локальных оптимумов
            logging.info(f"Instance {idx + 1} completed: {len(local_optima_heights)} local optima found")
        logging.info(f"Total local optima found: {total_local_optima}")  # Выводим общее количество локальных оптимумов
        return all_local_optima_heights, total_local_optima  # Возвращаем общее количество локальных оптимумов

    def plot_height_distribution(self, local_optima_heights):
        # Проверяем, есть ли локальные оптимумы
        if not local_optima_heights:
            print("No local optima found.")
            return

        # Нормализуем высоты (число удовлетворённых клауз)
        total_clauses = self.num_clauses
        normalized_heights = [h / total_clauses for h in local_optima_heights]

        # Находим минимальное и максимальное значения
        min_height = min(normalized_heights)
        max_height = max(normalized_heights)

        # Добавляем небольшой отступ (padding) для улучшения отображения
        padding = (max_height - min_height) * 0.05  # 5% от диапазона
        x_min = max(0, min_height - padding)
        x_max = min(1, max_height + padding)

        # Вычисляем гистограмму с обновлённым диапазоном
        num_bins = 50
        data, bins = np.histogram(normalized_heights, bins=num_bins, range=(x_min, x_max))
        # Нормализуем частоту
        data = data / np.sum(data)

        bin_centers = (bins[:-1] + bins[1:]) / 2

        plt.figure(figsize=(12, 7))
        plt.bar(bin_centers, data, width=np.diff(bins), alpha=0.7,
                edgecolor='black', align='center')

        plt.xlabel('Normalized Number of Satisfied Clauses (Height)', fontsize=14)
        plt.ylabel('Normalized Frequency of Local Optima', fontsize=14)
        plt.title('Distribution of Local Optima by Height', fontsize=16)
        plt.grid(axis='both')
        plt.show()


# Основная программа
num_variables = 10
num_clauses = 50
num_vars_in_clause = 3
num_of_instances = 100
num_configurations = 1000000

simulation = Simulation(num_variables, num_clauses, num_vars_in_clause, num_of_instances, num_configurations)

# Расчёт и визуализация распределения по высоте
logging.info("Starting simulation for Local Optima Distribution by Height")
local_optima_heights, total_local_optima = simulation.run(strictly_greater=False)  # Получаем общее число локальных оптимумов
print(f"Total number of local optima found: {total_local_optima}")  # Выводим общее количество локальных оптимумов
simulation.plot_height_distribution(local_optima_heights)
