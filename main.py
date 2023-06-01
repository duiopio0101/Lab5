import random

# Параметри задачі
num_classes = random.randint(2, 3)
num_teachers = random.randint(3, 4)
num_lessons_per_week = random.randint(23, 25)
num_lesson_types = random.randint(6, 8)
num_days = 5

lesson_types = ['Math', 'Science', 'English', 'Art', 'Music', 'Physical Education', 'Choreography']
special_rooms = ['Gym', 'Dance Studio', 'Music Room']
class_teachers = ['Галамага Н.В.', 'Бондарець О.П.', 'Нестерович Л.С.', 'Бугай Ю.М.']
teachers = ['Галамага Н.В.', 'Бондарець О.П.', 'Нестерович Л.С.', 'Бугай Ю.М.']

# Генерація початкової популяції
def create_initial_population(population_size):
    population = []
    for _ in range(population_size):
        schedule = []
        for class_id in range(num_classes):
            class_schedule = []
            for day in range(num_days):
                for lesson in range(1, num_lessons_per_week // num_days + 1):
                    lesson_type = random.randint(0, num_lesson_types - 1)
                    teacher_ids = random.sample(range(num_teachers), num_teachers)
                    room_id = random.randint(0, num_classes - 1)
                    class_schedule.append((lesson + day * (num_lessons_per_week // num_days), lesson_type, teacher_ids[class_id], room_id))
            schedule.append(class_schedule)
        population.append(schedule)
    return population


# Оцінка пристосованості розкладу
def evaluate_fitness(schedule):
    fitness = 0
    for class_schedule in schedule:
        # Перевірка кількості уроків на день
        daily_lessons = [0] * num_days
        for lesson, _, _, _ in class_schedule:
            day = (lesson - 1) % num_days
            daily_lessons[day] += 1
        if any(num_lessons > num_lessons_per_week // num_days for num_lessons in daily_lessons):
            fitness += 1

        # Перевірка "вікон" у розкладі
        num_windows = sum(1 for i in range(num_lessons_per_week - 1) if class_schedule[i][0] + 1 != class_schedule[i + 1][0])
        fitness += num_windows

        # Перевірка використання спеціалізованих приміщень
        used_special_rooms = set()
        for lesson, lesson_type, teacher_id, room_id in class_schedule:
            if lesson_type >= num_lesson_types - len(special_rooms):
                if room_id < num_classes or room_id >= num_classes + len(special_rooms):
                    fitness += 1
                elif room_id in used_special_rooms:
                    fitness += 1
                else:
                    used_special_rooms.add(room_id)
            else:
                if room_id >= num_classes:
                    fitness += 1

    return fitness


# Схрещування двох розкладів
def crossover(schedule1, schedule2):
    child_schedule = []
    for class_id in range(num_classes):
        child_class_schedule = []
        for lesson, lesson_type, teacher_id, room_id in schedule1[class_id]:
            if random.random() < 0.5:
                child_class_schedule.append((lesson, lesson_type, teacher_id, room_id))
            else:
                child_class_schedule.append((lesson, lesson_type, teacher_id, room_id))
        child_schedule.append(child_class_schedule)
    return child_schedule


# Мутація розкладу
def mutate(schedule):
    mutated_schedule = []
    for class_id in range(num_classes):
        mutated_class_schedule = []
        for lesson, lesson_type, teacher_id, room_id in schedule[class_id]:
            if random.random() < 0.1:  # ймовірність мутації
                lesson_type = random.randint(0, num_lesson_types - 1)
                teacher_ids = random.sample(range(num_teachers), num_teachers)
                room_id = random.randint(0, num_classes - 1)
                mutated_class_schedule.append((lesson, lesson_type, teacher_ids[class_id], room_id))
            else:
                mutated_class_schedule.append((lesson, lesson_type, teacher_id, room_id))
        mutated_schedule.append(mutated_class_schedule)
    return mutated_schedule


# Генетичний алгоритм
def genetic_algorithm(population_size, num_generations):
    population = create_initial_population(population_size)

    for generation in range(num_generations):
        fitness_scores = [evaluate_fitness(schedule) for schedule in population]

        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0])]
        selected_population = sorted_population[:population_size // 2]

        new_population = []

        # Схрещування і мутація для створення наступної популяції
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            child = crossover(parent1, parent2)
            mutated_child = mutate(child)
            new_population.append(mutated_child)

        population = new_population

    best_schedule = max(population, key=evaluate_fitness)
    return best_schedule


# Параметри генетичного алгоритму
population_size = 50
num_generations = 100

# Запуск генетичного алгоритму
best_schedule = genetic_algorithm(population_size, num_generations)

# Виведення оптимального розкладу
print("Оптимальний розклад:")

for day in range(num_days):
    print(f"День {day + 1}:")
    print("Клас 1".ljust(20) + " " * 4 + "Клас 2")
    class_1_schedule = best_schedule[0][day * (num_lessons_per_week // num_days):(day + 1) * (num_lessons_per_week // num_days)]
    class_2_schedule = best_schedule[1][day * (num_lessons_per_week // num_days):(day + 1) * (num_lessons_per_week // num_days)]

    for i in range(num_lessons_per_week // num_days):
        class_1_lesson = class_1_schedule[i]
        class_2_lesson = class_2_schedule[i]

        class_1_lesson_str = f"Урок {i+1} | Предмет - {lesson_types[class_1_lesson[1]]} | " \
                             f"Вчитель - {teachers[class_1_lesson[2]]} | " \
                             f"Приміщення - {special_rooms[class_1_lesson[3]] if class_1_lesson[1] >= num_lesson_types - len(special_rooms) else 'Класна кімната'}"

        class_2_lesson_str = f"Урок {i+1} | Предмет - {lesson_types[class_2_lesson[1]]} | " \
                             f"Вчитель - {teachers[class_2_lesson[2]]} | " \
                             f"Приміщення - {special_rooms[class_2_lesson[3]] if class_2_lesson[1] >= num_lesson_types - len(special_rooms) else 'Класна кімната'}"

        print(class_1_lesson_str.ljust(20) + " " * 4 + class_2_lesson_str)

    print("--------------------")

fitness = evaluate_fitness(best_schedule)
print(f"Оцінка якості розкладу: {fitness}")
