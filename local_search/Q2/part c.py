import random

# Original landscape
landscape = [5, 8, 6, 12, 9, 7, 17, 14, 10, 6, 19, 15, 11, 8]

# ---------------- FIRST CHOICE HC ----------------
def first_choice_hc(landscape, start):
    current = start
    path = [current]
    while True:
        moved = False
        # check LEFT first
        if current > 0 and landscape[current-1] > landscape[current]:
            current -= 1
            path.append(current)
            moved = True
        # check RIGHT if not moved
        elif current < len(landscape)-1 and landscape[current+1] > landscape[current]:
            current += 1
            path.append(current)
            moved = True
        if not moved:
            break
    return path, current

# ---------------- STOCHASTIC HC ----------------
def stochastic_hc(landscape, start):
    current = start
    path = [current]
    while True:
        neighbors = []
        if current > 0:
            neighbors.append(current-1)
        if current < len(landscape)-1:
            neighbors.append(current+1)
        uphill = [n for n in neighbors if landscape[n] > landscape[current]]
        if not uphill:
            break
        current = random.choice(uphill)
        path.append(current)
    return path, current

# ---------------- RANDOM RESTART HC ----------------
def random_restart_hc(landscape, num_restarts, variant='first choice', plateau_states=[]):
    best_state = None
    best_value = float('-inf')
    results = []
    plateau_count = 0

    for r in range(num_restarts):
        start = random.randint(0, len(landscape)-1)
        if variant == 'first choice':
            path, terminal = first_choice_hc(landscape, start)
        else:
            path, terminal = stochastic_hc(landscape, start)

        value = landscape[terminal]
        results.append((start, terminal, path))
        
        # Check if terminated on plateau
        if terminal in plateau_states:
            plateau_count += 1

        if value > best_value:
            best_value = value
            best_state = terminal

    return best_state, best_value, results, plateau_count

# ---------------- MAIN ----------------
def main():
    random.seed(42)

    # Plateau modification: states 7 and 8 have same f-value
    plateau_landscape = landscape.copy()
    plateau_landscape[6] = 17  # state 7
    plateau_landscape[7] = 17  # state 8
    plateau_states = [6, 7]    # 0-based indices

    # Run RRHC on original landscape
    best_state_orig, best_value_orig, results_orig, plateau_count_orig = random_restart_hc(
        landscape, num_restarts=20, variant='first choice', plateau_states=[]
    )

    # Run RRHC on plateau-modified landscape
    best_state_plateau, best_value_plateau, results_plateau, plateau_count = random_restart_hc(
        plateau_landscape, num_restarts=20, variant='first choice', plateau_states=plateau_states
    )

    # Count global maximum discoveries
    global_max = 11  # 0-based index = 10
    def count_global(results):
        return sum(1 for start, term, path in results if term == global_max)

    global_orig = count_global(results_orig)
    global_plateau = count_global(results_plateau)

    # Print table
    print("\n--- Global Maximum Discovery Rate ---")
    print(f"{'Landscape':<15}{'Global Max Found (out of 20)':<30}{'Plateau Count':<15}")
    print(f"{'Original':<15}{global_orig:<30}{'-':<15}")
    print(f"{'With Plateau':<15}{global_plateau:<30}{plateau_count:<15}")

if __name__ == "__main__":
    main()
