import random

# ------------------- Landscape -------------------
landscape = [5, 8, 6, 12, 9, 7, 17, 14, 10, 6, 19, 15, 11, 8]

# ------------------- Q1 HC functions -------------------
def first_choice_hc(landscape, start):
    current = start
    path = [current]
    while True:
        moved = False
        # Check LEFT first
        if current > 0 and landscape[current-1] > landscape[current]:
            current -= 1
            path.append(current)
            moved = True
        # Check RIGHT if no move
        elif current < len(landscape)-1 and landscape[current+1] > landscape[current]:
            current += 1
            path.append(current)
            moved = True
        if not moved:
            break
    return path, current

def stochastic_hc(landscape, start):
    current = start
    path = [current]
    while True:
        neighbours = []
        if current > 0:
            neighbours.append(current-1)
        if current < len(landscape)-1:
            neighbours.append(current+1)
        uphill = [n for n in neighbours if landscape[n] > landscape[current]]
        if not uphill:
            break
        current = random.choice(uphill)
        path.append(current)
    return path, current

# ------------------- Helper: Find Local Maxima -------------------
def find_local_maxima(landscape):
    maxima = []
    for i in range(len(landscape)):
        left = landscape[i-1] if i > 0 else float('-inf')
        right = landscape[i+1] if i < len(landscape)-1 else float('-inf')
        if landscape[i] > left and landscape[i] > right:
            maxima.append(i)
    return maxima

# ------------------- Random Restart Hill Climbing -------------------
def random_restart_hc(landscape, num_restarts=20, variant='first choice'):
    all_results = []
    best_state = None
    best_value = float('-inf')
    
    hc_func = first_choice_hc if variant=='first choice' else stochastic_hc

    for r in range(1, num_restarts+1):
        start = random.randint(0, len(landscape)-1)
        path, terminal = hc_func(landscape, start)
        value = landscape[terminal]
        all_results.append((start, terminal, path))
        
        if value > best_value:
            best_value = value
            best_state = terminal
        
        found_max = 'Yes' if value == max(landscape) else 'No'
        print(f"Restart {r:2}: Start={start+1}, Terminal={terminal+1}, f-value={value}, Global Max={found_max}")
    
    return best_state, best_value, all_results

# ------------------- MAIN -------------------
def main():
    print("\n--- Local Maxima in the Landscape ---")
    maxima = find_local_maxima(landscape)
    print([m+1 for m in maxima])  # +1 to show states starting from 1

    print("\n--- Random Restart HC (First Choice) ---")
    best_state, best_value, all_results = random_restart_hc(landscape, num_restarts=20, variant='first choice')
    print(f"\nBest State: {best_state+1}, f-value: {best_value}")

    print("\n--- Random Restart HC (Stochastic) ---")
    best_state, best_value, all_results = random_restart_hc(landscape, num_restarts=20, variant='stochastic')
    print(f"\nBest State: {best_state+1}, f-value: {best_value}")

if __name__ == "__main__":
    main()  
