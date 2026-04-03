import random
import numpy as np

# ----------------- Problem Data -----------------
demands = [
    12,45,23,67,34,19,56,38,72,15,49,61,
    27,83,41,55,30,77,64,18,52,39,71,26,
    44,91,33,58,22,85,16,69,47,74,31,53
]
NUM_DRIVERS = 10
GRID_SIZE = 36
SUPPLY_PENALTY = 5

# ----------------- Utility Functions -----------------
def fitness(state):
    """Compute fitness: sum of demands minus supply penalty per driver."""
    return sum(demands[i] for i in state) - SUPPLY_PENALTY * NUM_DRIVERS

def random_state():
    """Generate a random valid state with 10 unique zones."""
    return random.sample(range(GRID_SIZE), NUM_DRIVERS)

def neighbors(state):
    """Generate all neighbors by moving one driver to a free zone."""
    n = []
    for i in range(NUM_DRIVERS):
        for z in range(GRID_SIZE):
            if z not in state:
                new_state = state.copy()
                new_state[i] = z
                n.append(new_state)
    return n

# ----------------- Hill Climbing -----------------
def hc_driver(state, variant='first', max_steps=1000):
    current = state.copy()
    current_fit = fitness(current)
    steps = 0
    while steps < max_steps:
        neigh = neighbors(current)
        if variant == 'first':
            improved = False
            for n in neigh:
                f = fitness(n)
                if f > current_fit:
                    current = n
                    current_fit = f
                    improved = True
                    steps += 1
                    break
            if not improved:
                break
        elif variant == 'stochastic':
            better = [n for n in neigh if fitness(n) > current_fit]
            if not better:
                break
            current = random.choice(better)
            current_fit = fitness(current)
            steps += 1
    return current, current_fit

def rrhc_driver(num_restarts=30, variant='first'):
    best_state = None
    best_fit = -float('inf')
    per_restart_fits = []
    for _ in range(num_restarts):
        state = random_state()
        final_state, final_fit = hc_driver(state, variant)
        per_restart_fits.append(final_fit)
        if final_fit > best_fit:
            best_state = final_state
            best_fit = final_fit
    return best_state, best_fit, per_restart_fits

# ----------------- Genetic Algorithm -----------------
def ga_fitness(chromosome):
    return sum(demands[i] for i in chromosome) - SUPPLY_PENALTY * NUM_DRIVERS

def ordered_crossover(p1, p2):
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))
    slice_ = p1[a:b+1]
    child = [gene for gene in p2 if gene not in slice_]
    child = child[:a] + slice_ + child[a:]
    return child

def ga_mutate(chromosome, pm=0.1):
    if random.random() < pm:
        current_set = set(chromosome)
        available = [z for z in range(GRID_SIZE) if z not in current_set]
        if available:
            idx = random.randrange(NUM_DRIVERS)
            chromosome[idx] = random.choice(available)
    return chromosome

def tournament_select(pop, k=3):
    contenders = random.sample(pop, k)
    return max(contenders, key=ga_fitness)

def run_driver_ga(pop_size=30, generations=100, pm=0.1):
    population = [random_state() for _ in range(pop_size)]
    best_chromo = None
    best_fit = -float('inf')
    for _ in range(generations):
        new_pop = []
        while len(new_pop) < pop_size:
            parent1 = tournament_select(population)
            parent2 = tournament_select(population)
            child = ordered_crossover(parent1, parent2)
            child = ga_mutate(child, pm)
            new_pop.append(child)
            f = ga_fitness(child)
            if f > best_fit:
                best_chromo = child.copy()
                best_fit = f
        population = new_pop
    return best_chromo, best_fit

# ----------------- Head-to-Head Comparison -----------------
num_trials = 20
rrhc_fits = []
ga_fits = []

random.seed(42)
for _ in range(num_trials):
    _, fit_rrhc, _ = rrhc_driver()
    rrhc_fits.append(fit_rrhc)
    _, fit_ga = run_driver_ga()
    ga_fits.append(fit_ga)

# Compute statistics
def stats(lst):
    return np.mean(lst), np.std(lst), np.max(lst)

rrhc_mean, rrhc_std, rrhc_best = stats(rrhc_fits)
ga_mean, ga_std, ga_best = stats(ga_fits)

# Print table
print("Head-to-Head Comparison (20 trials each):")
print(f"{'Algorithm':<6} | {'Mean':<6} | {'Std':<6} | {'Best':<6}")
print("-"*40)
print(f"{'RRHC':<6} | {rrhc_mean:<6.2f} | {rrhc_std:<6.2f} | {rrhc_best:<6}")
print(f"{'GA':<6}   | {ga_mean:<6.2f} | {ga_std:<6.2f} | {ga_best:<6}")

import matplotlib.pyplot as plt

# ----------------- Boxplot -----------------
plt.figure()
plt.boxplot([rrhc_fits, ga_fits], labels=["RRHC", "GA"])
plt.title("RRHC vs GA Fitness Comparison (20 Trials)")
plt.xlabel("Algorithm")
plt.ylabel("Best Fitness")
plt.grid()

plt.savefig("comparison_boxplot.png")  
plt.show()

# ----------------- Line Plot (Trial-wise) -----------------
plt.figure()
plt.plot(rrhc_fits, marker='o', label='RRHC')
plt.plot(ga_fits, marker='s', label='GA')

plt.title("Trial-wise Fitness Comparison")
plt.xlabel("Trial Number")
plt.ylabel("Best Fitness")
plt.legend()
plt.grid()

plt.savefig("comparison_lineplot.png")
plt.show()
