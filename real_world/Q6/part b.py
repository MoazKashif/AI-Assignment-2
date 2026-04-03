import random

demands = [
    12,45,23,67,34,19,56,38,72,15,49,61,27,83,41,55,30,77,
    64,18,52,39,71,26,44,91,33,58,22,85,16,69,47,74,31,53
]
SUPPLY_PENALTY = 5
NUM_DRIVERS = 10
GRID_SIZE = 6  

def fitness(state, demands):
    """Compute fitness: sum of demands of placed drivers minus supply penalty."""
    return sum(demands[i] for i in state) - SUPPLY_PENALTY * NUM_DRIVERS

def get_neighbors(state):
    """Generate all neighbor states by moving one driver to a free zone."""
    neighbors = []
    state_set = set(state)
    free_zones = set(range(len(demands))) - state_set
    for i, driver_zone in enumerate(state):
        for new_zone in free_zones:
            neighbor = state.copy()
            neighbor[i] = new_zone
            neighbors.append(neighbor)
    return neighbors

# --- Hill Climbing Variants --- #
def hc_driver(state, demands, variant='stochastic', max_steps=1000):
    """Single HC run: variant='first_choice' or 'stochastic'"""
    current = state.copy()
    current_fit = fitness(current, demands)
    steps = 0
    
    while steps < max_steps:
        steps += 1
        neighbors = get_neighbors(current)
        neighbor_fits = [fitness(n, demands) for n in neighbors]
        
        if variant == 'first_choice':
            improved = False
            for n, f in zip(neighbors, neighbor_fits):
                if f > current_fit:
                    current, current_fit = n, f
                    improved = True
                    break
            if not improved:
                break  # local maximum
        elif variant == 'stochastic':
            better_neighbors = [n for n, f in zip(neighbors, neighbor_fits) if f > current_fit]
            if not better_neighbors:
                break  # local maximum
            current = random.choice(better_neighbors)
            current_fit = fitness(current, demands)
        else:
            raise ValueError("Unknown variant")
    
    return current, current_fit, steps

# --- Random Restart HC --- #
def rrhc_driver(num_restarts, demands, variant='stochastic'):
    best_state = None
    best_fit = -float('inf')
    per_restart_fitness = []
    
    for r in range(num_restarts):
        initial_state = random.sample(range(len(demands)), NUM_DRIVERS)
        final_state, final_fit, steps = hc_driver(initial_state, demands, variant)
        per_restart_fitness.append(final_fit)
        if final_fit > best_fit:
            best_state, best_fit = final_state, final_fit
    
    return best_state, best_fit, per_restart_fitness

# --- Utility to print driver positions in (row,col) format --- #
def state_positions(state):
    return [(i // GRID_SIZE, i % GRID_SIZE) for i in state]

# --- Run RRHC --- #
random.seed(42)
best_state, best_fit, per_restart_fitness = rrhc_driver(30, demands, variant='stochastic')

print("Best State Found:", best_state)
print("Fitness:", best_fit)
print("Driver Positions (row, col):", state_positions(best_state))
print("Best Fitness per Restart:", per_restart_fitness)
