import random

# ---------------- DECODE FUNCTION ----------------
def decode(chromosome):
    """Convert 4-bit binary list to integer."""
    value = 0
    for bit in chromosome:
        value = (value << 1) | bit
    return value

# ---------------- FITNESS FUNCTION ----------------
def fitness(chromosome):
    """Compute f(x) = -x^2 + 14x + 5"""
    x = decode(chromosome)
    return -x**2 + 14*x + 5

# ---------------- ROULETTE SELECTION ----------------
def roulette_select(population):
    """Select one individual using fitness-proportionate selection."""
    fitness_values = [fitness(ind) for ind in population]
    total_fitness = sum(fitness_values)
    
    r = random.random() * total_fitness
    cumulative = 0
    
    for ind, fit in zip(population, fitness_values):
        cumulative += fit
        if cumulative >= r:
            return ind

# ---------------- SINGLE POINT CROSSOVER ----------------
def single_point_crossover(parent1, parent2, point):
    """Perform crossover at given point."""
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# ---------------- MUTATION ----------------
def mutate(chromosome, pm):
    """Bit-flip mutation with probability pm."""
    mutated = []
    for bit in chromosome:
        if random.random() < pm:
            mutated.append(1 - bit)  # flip bit
        else:
            mutated.append(bit)
    return mutated

# ---------------- TESTING FUNCTIONS ----------------
test_chromosomes = [
    [0,1,1,0],
    [1,0,0,1],
    [1,1,0,0],
    [0,0,1,1]
]

print("Testing decode and fitness:\n")
for chrom in test_chromosomes:
    x = decode(chrom)
    f = fitness(chrom)
    print(f"Chromosome: {chrom} -> x = {x}, f(x) = {f}")

# Test crossover
print("\nTesting crossover:")
p1 = [1,0,1,1]
p2 = [0,1,0,0]
c1, c2 = single_point_crossover(p1, p2, 2)
print("Parent1:", p1)
print("Parent2:", p2)
print("Child1 :", c1)
print("Child2 :", c2)

# Test mutation
print("\nTesting mutation:")
chrom = [1,1,0,0]
print("Before:", chrom)
print("After :", mutate(chrom, 0.5))

# Test roulette selection
print("\nTesting roulette selection:")
population = test_chromosomes
selected = roulette_select(population)
print("Selected individual:", selected)
