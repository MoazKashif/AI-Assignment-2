import random

# --- Problem Data ---
demands = [12,45,23,67,34,19,56,38,72,15,49,61,27,83,41,55,30,77,
           64,18,52,39,71,26,44,91,33,58,22,85,16,69,47,74,31,53]
num_drivers = 10
all_zones = list(range(36))

# --- GA Fitness ---
def ga_fitness(chromosome, demands):
    """Fitness = sum of demands for selected zones minus supply penalty per driver"""
    return sum(demands[i] for i in chromosome) - 5 * num_drivers

# --- Order Crossover (OX) ---
def ordered_crossover(p1, p2):
    """Order Crossover: preserves uniqueness"""
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))
    child = [None] * size
    # Copy slice from parent1
    child[a:b+1] = p1[a:b+1]
    # Fill remaining with parent2's values in order
    p2_idx = 0
    for i in range(size):
        if child[i] is None:
            while p2[p2_idx] in child:
                p2_idx += 1
            child[i] = p2[p2_idx]
    return child

# --- Mutation ---
def ga_mutate(chromosome, pm):
    """Swap a random gene with a zone not in chromosome with probability pm"""
    if random.random() < pm:
        current = chromosome.copy()
        zone_out = random.choice(current)
        remaining_zones = [z for z in all_zones if z not in current]
        zone_in = random.choice(remaining_zones)
        idx = current.index(zone_out)
        current[idx] = zone_in
        return current
    return chromosome

# --- Tournament Selection ---
def tournament_select(population, fitnesses, k=3):
    """Select one parent via tournament selection"""
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1], reverse=True)  # higher fitness better
    return selected[0][0]

# --- Initialize Random Population ---
def init_population(pop_size):
    population = []
    for _ in range(pop_size):
        chromo = random.sample(all_zones, num_drivers)
        population.append(chromo)
    return population

# --- Run GA Driver ---
def run_driver_ga(pop_size=30, generations=100, pm=0.1):
    population = init_population(pop_size)
    best_chromo = None
    best_fit = -float('inf')
    
    for gen in range(generations):
        fitnesses = [ga_fitness(c, demands) for c in population]
        new_pop = []
        for _ in range(pop_size // 2):
            # Select parents
            p1 = tournament_select(population, fitnesses)
            p2 = tournament_select(population, fitnesses)
            # Crossover
            child1 = ordered_crossover(p1, p2)
            child2 = ordered_crossover(p2, p1)
            # Mutation
            child1 = ga_mutate(child1, pm)
            child2 = ga_mutate(child2, pm)
            new_pop.extend([child1, child2])
        # Update population
        population = new_pop
        # Track best
        for c in population:
            f = ga_fitness(c, demands)
            if f > best_fit:
                best_fit = f
                best_chromo = c.copy()
    
    # Print best result
    driver_positions = [(i // 6, i % 6) for i in best_chromo]
    print("Best State Found:", best_chromo)
    print("Fitness:", best_fit)
    print("Driver Positions (row, col):", driver_positions)

# --- Run the GA ---
random.seed(42)  # for reproducibility
run_driver_ga()
