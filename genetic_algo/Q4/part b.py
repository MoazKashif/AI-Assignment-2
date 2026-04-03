import random

# ---------- Helper Functions (reuse from part a) ----------

def decode(chromosome):
    value = 0
    for bit in chromosome:
        value = (value << 1) | bit
    return value

def fitness(chromosome):
    x = decode(chromosome)
    return -x**2 + 14*x + 5

def roulette_select(population):
    fitness_values = [fitness(ind) for ind in population]
    total = sum(fitness_values)
    
    # Edge case: if total fitness is 0 or negative
    if total <= 0:
        return random.choice(population)
    
    r = random.random() * total
    cumulative = 0
    
    for ind, fit in zip(population, fitness_values):
        cumulative += fit
        if cumulative >= r:
            return ind
    
    # Fallback 
    return population[-1]

def single_point_crossover(p1, p2):
    point = random.randint(1, 3)  
    c1 = p1[:point] + p2[point:]
    c2 = p2[:point] + p1[point:]
    return c1, c2

def mutate(chromosome, pm):
    return [1 - bit if random.random() < pm else bit for bit in chromosome]

# ---------- MAIN GA FUNCTION ----------
def run_ga(pop_size, num_generations, pm, elitism=False):
    
    # Initial random population
    population = [[random.randint(0,1) for _ in range(4)] for _ in range(pop_size)]
    
    history = []

    for gen in range(num_generations):
        
        # Evaluate population
        decoded = [decode(ind) for ind in population]
        fits = [fitness(ind) for ind in population]
        
        # Best individual
        best_idx = fits.index(max(fits))
        best = population[best_idx]
        best_fit = fits[best_idx]
        best_x = decoded[best_idx]
        
        history.append((gen, best_fit, best_x))
        
        # PRINT FULL TABLE ROW
        print(f"\nGeneration {gen}:")
        for i in range(pop_size):
            print(f"{population[i]} -> x={decoded[i]}, f={fits[i]}")
        print(f"Best: {best} -> x={best_x}, f={best_fit}")
        
        # Create next generation
        new_population = []
        
        # Elitism
        if elitism:
            new_population.append(best[:])
        
        while len(new_population) < pop_size:
            p1 = roulette_select(population)
            p2 = roulette_select(population)
            
            c1, c2 = single_point_crossover(p1, p2)
            
            c1 = mutate(c1, pm)
            c2 = mutate(c2, pm)
            
            new_population.append(c1)
            if len(new_population) < pop_size:
                new_population.append(c2)
        
        population = new_population[:pop_size]
    
    return history

# ---------- RUN ----------
random.seed(42)  # for reproducibility

history = run_ga(
    pop_size=4,
    num_generations=10,
    pm=0.1,
    elitism=False
)
