import math 
import random

def sigmoid(x):
    # numerically stable sigmoid (no overflow)
    if x >= 0:
        z = math.exp(-x)
        return 1 / (1 + z)
    else:
        z = math.exp(x)
        return z / (1 + z)

def decide_flap(genome, bird_y, gap_y):
    # normalize inputs to [0,1] to avoid huge activations
    bird_y_n = bird_y / 600.0
    gap_y_n = gap_y / 600.0

    # split numbers 
    w_input_hidden = genome[:10] 
    b_hidden = genome[10:15] 
    w_hidden_output = genome[15:20] 
    b_output = genome[20]

    # compute hidden layer 
    hidden = [] 
    for j in range(5): 
        w1 = w_input_hidden[2*j] 
        w2 = w_input_hidden[2*j + 1] 
        h = sigmoid(w1 * bird_y_n + w2 * gap_y_n + b_hidden[j]) 
        hidden.append(h) 

    # compute output 
    total = sum(h * w for h, w in zip(hidden, w_hidden_output)) + b_output 
    out = sigmoid(total)
    return out > 0.5

def roulette_wheel_selection(population, fitnesses): 
    total_fitness = sum(fitnesses)
    # if everyone scored 0 (or negative), pick a random parent
    if total_fitness <= 0:
        return random.choice(population)

    pick = random.uniform(0, total_fitness) 
    current = 0 
    for genome, fit in zip(population, fitnesses): 
        current += fit 
        if current > pick: 
            return genome
    # return last individual
    return population[-1]

def crossover_pair(parent1, parent2): 
    point = random.randint(1, len(parent1) - 1) 
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(genome, mutation_rate=0.15, mutation_strength=0.2):
    new_genome = [] 
    for gene in genome: 
        if random.random() < mutation_rate: 
            gene += random.uniform(-mutation_strength, mutation_strength) 
        new_genome.append(gene) 
    return new_genome

def next_generation(population, fitnesses, mutation_rate=0.15, mutation_strength=0.2): 
    new_population = [] 
    pop_size = len(population)

    # keep the best genome (elitism)
    best_idx = max(range(pop_size), key=lambda i: fitnesses[i])
    elite = population[best_idx][:]
    while len(new_population) < pop_size: 
        parent1 = roulette_wheel_selection(population, fitnesses) 
        parent2 = roulette_wheel_selection(population, fitnesses)
        child1, child2 = crossover_pair(parent1, parent2) 
        child1 = mutate(child1, mutation_rate, mutation_strength) 
        child2 = mutate(child2, mutation_rate, mutation_strength)
        new_population.append(child1) 
        if len(new_population) < pop_size: 
            new_population.append(child2) 
    # ensure elite survives
    new_population[0] = elite
    return new_population