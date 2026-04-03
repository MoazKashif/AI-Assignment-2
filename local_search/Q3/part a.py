import random

# ---------------- FIRST CHOICE HC WITH FAILURE DIAGNOSIS ----------------
def diagnose_hc(landscape, start):
    current = start
    path = [current]
    visited = set([current])
    
    while True:
        neighbors = []
        if current > 0:
            neighbors.append(current-1)
        if current < len(landscape)-1:
            neighbors.append(current+1)
        
        uphill = [n for n in neighbors if landscape[n] > landscape[current]]
        equal = [n for n in neighbors if landscape[n] == landscape[current]]
        
        # Ridge detection: same state visited twice
        for n in uphill + equal:
            if n in visited:
                current = n
                path.append(current)
                failure = "ridge"
                print(f"Terminated at state {current+1} with f={landscape[current]}. Failure mode: {failure}")
                return path, current, failure
        
        if uphill:
            current = uphill[0]  # first-choice HC
            path.append(current)
            visited.add(current)
            continue
        elif equal:
            current = equal[0]
            path.append(current)
            failure = "plateau"
            print(f"Terminated at state {current+1} with f={landscape[current]}. Failure mode: {failure}")
            return path, current, failure
        else:
            failure = "local maximum"
            print(f"Terminated at state {current+1} with f={landscape[current]}. Failure mode: {failure}")
            return path, current, failure

# ---------------- TEST LANDSCAPES ----------------
local_max_landscape = [2, 4, 6, 5, 3]
plateau_landscape = [1, 3, 5, 5, 2]
ridge_landscape = [3, 6, 3, 6, 3]  

# ---------------- RUN DIAGNOSE ----------------
print("Testing Local Maximum:")
diagnose_hc(local_max_landscape, start=0)

print("\nTesting Plateau:")
diagnose_hc(plateau_landscape, start=0)

print("\nTesting Ridge:")
diagnose_hc(ridge_landscape, start=1)
