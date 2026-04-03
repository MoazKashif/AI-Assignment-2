import random

# ------------------ Helper Functions ------------------
def random_chromosome():
    """Generate a random chromosome: list of 6 (room, slot) tuples."""
    return [(random.randint(0, 2), random.randint(0, 3)) for _ in range(6)]

def count_conflicts(chromosome):
    """Count number of course conflicts (same room, same time)."""
    conflicts = 0
    n = len(chromosome)
    for i in range(n):
        for j in range(i+1, n):
            if chromosome[i] == chromosome[j]:
                conflicts += 1
    return conflicts

def fitness(chromosome):
    """Fitness = 100 - 10*conflicts."""
    return 100 - 10*count_conflicts(chromosome)

def tournament_selection(pop):
    """Tournament selection (size=2)."""
    i1, i2 = random.sample(range(len(pop)), 2)
    return pop[i1] if fitness(pop[i1]) >= fitness(pop[i2]) else pop[i2]

def crossover(p1, p2, point):
    """Single-point crossover."""
    child1 = p1[:point] + p2[point:]
    child2 = p2[:point] + p1[point:]
    return child1, child2

def repair(chromosome):
    """Repair conflicting genes to a conflict-free assignment."""
    seen = set()
    n = len(chromosome)
    for i in range(n):
        if chromosome[i] in seen:
            # Reassign randomly to a non-conflicting slot if possible
            available = [(r, s) for r in range(3) for s in range(4) if (r, s) not in seen]
            if available:
                chromosome[i] = random.choice(available)
            else:
                # Assign randomly if no conflict-free slot exists
                chromosome[i] = (random.randint(0, 2), random.randint(0, 3))
        seen.add(chromosome[i])
    return chromosome

def mutate(chromosome, pm):
    """Mutate chromosome per-gene with probability pm."""
    for i in range(len(chromosome)):
        if random.random() < pm:
            chromosome[i] = (random.randint(0, 2), random.randint(0, 3))
    return chromosome

# ------------------ Full GA Function ------------------
def run_scheduling_ga(pop_size=20, generations=50, pm=0.1):
    # Initialize population
    population = [random_chromosome() for _ in range(pop_size)]
    best_per_generation = []

    for gen in range(generations):
        new_pop = []
        # Keep track of best individual this generation
        best_ind = max(population, key=fitness)
        best_per_generation.append(fitness(best_ind))

        # Check if solution found
        if count_conflicts(best_ind) == 0:
            print(f"Solution found at generation {gen}: {best_ind}")
            break

        # Create next generation
        while len(new_pop) < pop_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            point = random.randint(1, 5)  # crossover point between 1 and 5
            child1, child2 = crossover(parent1, parent2, point)
            # Repair after crossover
            child1 = repair(child1)
            child2 = repair(child2)
            # Mutate
            child1 = mutate(child1, pm)
            child2 = mutate(child2, pm)
            new_pop.extend([child1, child2])
        # Trim in case of overfill
        population = new_pop[:pop_size]

    # Final best schedule
    best_schedule = max(population, key=fitness)
    print("\nBest Schedule Found:")
    for idx, (room, slot) in enumerate(best_schedule):
        print(f"C{idx+1}: Room {room+1}, Slot {slot+1}")
    print("Conflicts:", count_conflicts(best_schedule))
    return best_schedule, best_per_generation

# ------------------ Run GA ------------------
best_schedule, fitness_curve = run_scheduling_ga(pop_size=20, generations=50, pm=0.1)

