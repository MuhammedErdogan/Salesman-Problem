from operator import itemgetter
import random

# stock amount of products
itemStock = [30, 40, 20, 40, 20]

# prices given by cities for products
priceX1City = [1, 3, 3, 2, 10]
priceX2City = [4, 8, 12, 6, 5]
priceX3City = [6, 2, 3, 10, 12]
priceX4City = [4, 5, 5, 2, 6]
priceX5City = [4, 15, 5, 4, 3]

# the best individual we've had at the end of all generations
peek = [[], [], [], [], [], [0]]


def calculate_f1(sold_match):
    diff = max(sold_match) - min(sold_match)
    rate = max((20 - diff), 0) / 100
    return rate


def calculate_f2(ind):
    temp_count_list = []
    for b in range(5):
        temp_count_list.append(sum(ind[b]))
    rate = max(0, 20 - (max(temp_count_list) - min(temp_count_list))) / 100
    return rate


def calculate_f3(gains):
    flag = 0
    for g in range(4):
        if gains[g] == 0:
            flag += 1
    return flag == 0


def calculate_total_gain(ind):
    x1_gain = 0
    x2_gain = 0
    x3_gain = 0
    x4_gain = 0
    x5_gain = 0

    sold_matrix = ind.copy()

    for j in range(5):
        # calculate total earnings for each city
        x1_gain += sold_matrix[0][j] * priceX1City[j]
        x2_gain += sold_matrix[1][j] * priceX2City[j]
        x3_gain += sold_matrix[2][j] * priceX3City[j]
        x4_gain += sold_matrix[3][j] * priceX4City[j]
        x5_gain += sold_matrix[4][j] * priceX5City[j]

    gainArray = [x1_gain, x2_gain, x3_gain, x4_gain, x5_gain]

    fb = sum(gainArray)

    f1 = 0
    for k in range(5):
        f1 += gainArray[k] * calculate_f1(sold_matrix[k])

    f2 = fb * calculate_f2(sold_matrix)

    f3 = 0
    if calculate_f3(gainArray):
        f3 = 100

    totalGain = fb + f1 + f2 + f3

    return [totalGain, fb, f1, f2, f3]


def init():
    generation = []

    for _ in range(1000):

        # matrices created to keep the number of products sold in each city
        sold_match_x1 = []
        sold_match_x2 = []
        sold_match_x3 = []
        sold_match_x4 = []
        sold_match_x5 = []

        # generate random product numbers for first generation
        for j in range(5):
            init_value = int(itemStock[j])

            current_random_item_amount = random.randint(0, init_value)
            total_random_selection = current_random_item_amount
            sold_match_x1.append(current_random_item_amount)

            current_random_item_amount = random.randint(0, init_value - total_random_selection)
            total_random_selection += current_random_item_amount
            sold_match_x2.append(current_random_item_amount)

            current_random_item_amount = random.randint(0, init_value - total_random_selection)
            total_random_selection += current_random_item_amount
            sold_match_x3.append(current_random_item_amount)

            current_random_item_amount = random.randint(0, init_value - total_random_selection)
            total_random_selection += current_random_item_amount
            sold_match_x4.append(current_random_item_amount)

            current_random_item_amount = int(init_value - total_random_selection)
            sold_match_x5.append(current_random_item_amount)

        # define a matrix of product quantities sold in all cities
        temp_sold_match_matrix = [sold_match_x1.copy(), sold_match_x2.copy(), sold_match_x3.copy(),
                                  sold_match_x4.copy(), sold_match_x5.copy()]

        individual = temp_sold_match_matrix.copy()
        individual.append(calculate_total_gain(temp_sold_match_matrix)[0])

        generation.append(individual)  # add individual to first generation

    return generation


def cross_over(individual_1, individual_2):  # cross two randomly selected individuals to create a new hybrid individual
    new_individual = [[], [], [], [], []]

    for product in range(5):
        if random.randint(0, 1) == 1:
            for city in range(5):
                new_individual[city].append(individual_1[city][product])
        else:
            for city in range(5):
                new_individual[city].append(individual_2[city][product])

    return new_individual


def type_1_mutate(individual):  # add and subtract a mutually random value for two products
    individualMutated = individual.copy()
    for product in range(5):
        index = random.randrange(0, 4)
        index1 = random.randint(0, 4)
        count = random.randint(0, 10)

        if individual[index][product] - count >= 0:
            individual[index][product] -= count
            individualMutated[index1][product] += count

    return individualMutated


def type_2_mutate(individual):  # randomly swap the number of items sold in two cities
    individualMutated = individual.copy()
    index1 = random.randrange(0, 4)
    index2 = random.randint(0, 4)
    individualMutated[index1], individualMutated[index2] = \
        individual[index2], individual[index1]

    return individualMutated


def type_3_mutate(individual):  # Swap the numbers of two randomly selected products of the same type
    individualMutated = individual.copy()
    for product in range(5):
        index = random.randrange(0, 4)
        index1 = random.randint(0, 4)
        individual[index][product], individualMutated[index1][product] = \
            individualMutated[index1][product], individual[index][product]

    return individualMutated


def create_new_generation(generation):
    sorted_gen = sorted(generation, key=itemgetter(5))  # sort matrix by total gain
    sorted_gen.reverse()
    selected_gen = sorted_gen[0:250]  # select the top 250 individuals

    for j in range(125):  # randomly select 125 individuals
        selected_gen.append(generation[random.randint(0, len(generation) - 1)].copy())

    for j in range(len(selected_gen)):  # delete total gain values from previous generation in matrices
        del (selected_gen[j][5])

    best = [[], [], [], [], [], 0]
    generation.clear()

    for _ in range(2000):  # Create 2000 hybrid individuals
        # randomly selecting 2 individuals to cross from selected individuals
        temp_ind_1 = selected_gen[random.randint(0, len(selected_gen) - 1)]
        temp_ind_2 = selected_gen[random.randint(0, len(selected_gen) - 1)]

        individual = cross_over(temp_ind_1, temp_ind_2)  # new hybrid individual

        individual = type_1_mutate(individual)  # apply type 1 mutation

        if random.randint(0, 2) == 1:  # apply type 2 mutation at 33 percent
            individual = type_2_mutate(individual)

        if random.randint(0, 2) == 1:  # apply type 3 mutation at 33 percent
            individual = type_3_mutate(individual)

        gain = calculate_total_gain(individual)  # calculate the entire earnings matrix for the current individual

        individual.append(gain[0])  # add the total gain to the end of the matrix

        # if this individual's total earnings are higher, update the best individual of this generation
        if individual[5] > best[5]:
            best = individual.copy()

        generation.append(individual)  # add the obtained individual to this generation

    return best


inited_generation = init()  # create first generation

for _ in range(100):
    best_solution = create_new_generation(inited_generation)

    if best_solution[5] > peek[5][0]:  # update the best individual of all generation
        peek = best_solution.copy()
        gain_matrix = calculate_total_gain(peek)  # calculate all gain matrix of peek
        peek[5] = gain_matrix

        print(peek[0:5])
        print("fb:", gain_matrix[1], " f1:", gain_matrix[2],
              " f2:", gain_matrix[3], " f3:", gain_matrix[4])
        print("total:", gain_matrix[0], "\n")
