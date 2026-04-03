import random

# ----------------- Problem Definition -----------------
demands = [12,45,23,67,34,19, 56,38,72,15,49,61,
           27,83,41,55,30,77,64,18,52,39,71,26,
           44,91,33,58,22,85,16,69,47,74,31,53]
supply_penalty = 5
num_drivers = 10
num_zones = 36

# ----------------- Fitness Function -----------------
def fitness(state):
    """Compute objective value: sum of demands minus supply penalties."""
    return sum(demands[i] for i in state) - supply_penalty * num_drivers

# ----------------- Neighbour Function -----------------
def get_neighbors(state):
    """Return all neighbors by moving one driver to a free zone."""
    neighbors = []
    for driver_zone in state:
        for new_zone in range(num_zones):
            if new_zone not in state:
                neighbor = state.copy()
                neighbor.remove(driver_zone)
                neighbor.add(new_zone)
                neighbors.append(neighbor)
    return neighbors

# ----------------- Test 3 Random States -----------------
for i in range(3):
    state = set(random.sample(range(num_zones), num_drivers))
    fit = fitness(state)
    neighbors = get_neighbors(state)
    
    # Check that all neighbors have size 10 and are unique
    all_valid = all(len(n) == num_drivers for n in neighbors)
    
    print(f"State {i+1}: {sorted(state)}")  # sorted for readability
    print(f"Fitness: {fit}")
    print(f"Number of neighbors: {len(neighbors)}")
    print(f"All neighbors valid (size 10)? {all_valid}\n")
