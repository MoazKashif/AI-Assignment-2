# part c 
import random

# Updated landscape with plateau at states 5,6,7
landscape = [4, 9, 6, 11, 15, 15, 15, 7, 13, 5, 16, 12]

# ---------------- FIRST CHOICE HC (with plateau detection and sideways) ----------------
def first_choice_hc(landscape, start, sideways_limit=0):
    current = start
    path = [current]
    sideways_count = 0

    while True:
        moved = False

        # LEFT neighbor
        if current > 1:
            left_val = landscape[current-2]
            curr_val = landscape[current-1]
            if left_val > curr_val:
                current -= 1
                path.append(current)
                moved = True
                sideways_count = 0  # reset sideways
            elif left_val == curr_val and sideways_limit > 0 and sideways_count < sideways_limit:
                current -= 1
                path.append(current)
                moved = True
                sideways_count += 1
                print(f"Sideways move to {current} (LEFT) from state {current+1})")
        
        # RIGHT neighbor (only if not moved)
        if not moved and current < len(landscape):
            right_val = landscape[current]
            curr_val = landscape[current-1]
            if right_val > curr_val:
                current += 1
                path.append(current)
                moved = True
                sideways_count = 0
            elif right_val == curr_val and sideways_limit > 0 and sideways_count < sideways_limit:
                current += 1
                path.append(current)
                moved = True
                sideways_count += 1
                print(f"Sideways move to {current} (RIGHT) from state {current-1})")

        # Plateau detection
        if not moved:
            neighbors = []
            if current > 1:
                neighbors.append(current-1)
            if current < len(landscape):
                neighbors.append(current+1)
            equal_neighbors = [n for n in neighbors if landscape[n-1] == landscape[current-1]]
            if equal_neighbors:
                print(f"Plateau detected at state {current} with equal neighbors {equal_neighbors}")
            break

        if sideways_limit > 0 and sideways_count >= sideways_limit:
            print(f"Sideways move cap reached at state {current}")
            break

    return path, current

# ---------------- STOCHASTIC HC (with plateau detection and sideways) ----------------
def stochastic_hc(landscape, start, sideways_limit=0):
    current = start
    path = [current]
    sideways_count = 0

    while True:
        neighbors = []
        if current > 1:
            neighbors.append(current-1)
        if current < len(landscape):
            neighbors.append(current+1)

        curr_val = landscape[current-1]
        uphill = [n for n in neighbors if landscape[n-1] > curr_val]
        equal = [n for n in neighbors if landscape[n-1] == curr_val]

        if uphill:
            current = random.choice(uphill)
            path.append(current)
            sideways_count = 0
        elif sideways_limit > 0 and equal and sideways_count < sideways_limit:
            current = random.choice(equal)
            path.append(current)
            sideways_count += 1
            print(f"Sideways move to {current} from state {path[-2]}")
        else:
            if equal:
                print(f"Plateau detected at state {current} with equal neighbors {equal}")
            break

    return path, current

# ---------------- MAIN ----------------
def main():
    print("Start | Algorithm | Path | Terminal | Steps")
    print("-"*60)
    
    sideways_limit = 10

    plateau_counts_fc = 0
    plateau_counts_st = 0

    for start in range(1, 13):
        print(f"\n--- Starting State {start} ---")

        # First-Choice HC with sideways moves
        path_fc, term_fc = first_choice_hc(landscape, start, sideways_limit)
        print(f"First-Choice HC — Path: {path_fc}, Terminal: {term_fc}, Steps: {len(path_fc)-1}")
        if len(path_fc) == 1 or (term_fc in path_fc and landscape[term_fc-1] == landscape[path_fc[-2]-1]):
            plateau_counts_fc += 1

        # Stochastic HC with sideways moves
        path_st, term_st = stochastic_hc(landscape, start, sideways_limit)
        print(f"Stochastic HC — Path: {path_st}, Terminal: {term_st}, Steps: {len(path_st)-1}")
        if len(path_st) == 1 or (term_st in path_st and landscape[term_st-1] == landscape[path_st[-2]-1]):
            plateau_counts_st += 1

    print("\nSummary of runs stuck on plateau:")
    print(f"First-Choice HC: {plateau_counts_fc} runs")
    print(f"Stochastic HC: {plateau_counts_st} runs")

if __name__ == "__main__":
    main()
