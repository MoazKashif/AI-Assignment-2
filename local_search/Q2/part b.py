import random

landscape = [5, 8, 6, 12, 9, 7, 17, 14, 10, 6, 19, 15, 11, 8]

# Reuse First-Choice HC from Q1
def first_choice_hc(landscape, start):
    current = start
    path = [current]
    while True:
        moved = False
        if current > 0 and landscape[current-1] > landscape[current]:
            current = current - 1
            path.append(current)
            moved = True
        elif current < len(landscape)-1 and landscape[current+1] > landscape[current]:
            current = current + 1
            path.append(current)
            moved = True
        if not moved:
            break
    return path, current

# Random Restart HC
def random_restart_hc(landscape, num_restarts, variant='first choice'):
    best_state = None
    best_value = float('-inf')
    all_results = []

    for _ in range(num_restarts):
        start = random.randint(0, len(landscape)-1)
        if variant == 'first choice':
            path, terminal = first_choice_hc(landscape, start)
        else:
            raise NotImplementedError("Only first choice variant used here")
        f_val = landscape[terminal]
        all_results.append((start, terminal, path))
        if f_val > best_value:
            best_value = f_val
            best_state = terminal

    return best_state, best_value, all_results

# Experiment
restart_counts = [1, 3, 5, 10, 20]
trials = 100
global_max_state = 11  # index-based (0..13) if needed, here we keep 1-based

empirical_probs = []

for n in restart_counts:
    found_count = 0
    for _ in range(trials):
        best_state, _, _ = random_restart_hc(landscape, n, variant='first choice')
        if best_state == global_max_state - 1:  # adjust for 0-indexed list
            found_count += 1
    empirical_probs.append(found_count / trials)

print("Empirical probabilities of finding global maximum (state 11):")
for n, prob in zip(restart_counts, empirical_probs):
    print(f"Restarts={n} → Probability={prob:.2f}")
