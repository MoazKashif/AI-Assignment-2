# Part a 
import random

# Landscape (index 0 = state 1)
landscape = [4, 9, 6, 11, 8, 15, 10, 7, 13, 5, 16, 12]

# ---------------- FIRST CHOICE HC ----------------
def first_choice_hc(landscape, start):
    current = start
    path = [current]

    while True:
        moved = False

        # check LEFT first
        if current > 1 and landscape[current-2] > landscape[current-1]:
            current = current - 1
            path.append(current)
            moved = True

        # if not moved, check RIGHT
        elif current < len(landscape) and landscape[current] > landscape[current-1]:
            current = current + 1
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
        neighbours = []

        if current > 1:
            neighbours.append(current - 1)

        if current < len(landscape):
            neighbours.append(current + 1)

        # only better neighbours
        uphill = [n for n in neighbours if landscape[n-1] > landscape[current-1]]

        if not uphill:
            break

        current = random.choice(uphill)
        path.append(current)

    return path, current

# ---------------- MAIN ----------------
def main():
    print("Start | Algorithm | Path | Terminal | Steps")
    print("----------------------------------------------------------")

    for s in range(1, 13):
        path, terminal = first_choice_hc(landscape, s)
        print(f"Start={s} — Algorithm=FirstChoice — Path={path} — Terminal={terminal} — Steps={len(path)-1}")

        path, terminal = stochastic_hc(landscape, s)
        print(f"Start={s} — Algorithm=Stochastic — Path={path} — Terminal={terminal} — Steps={len(path)-1}")
    count = 0

    for _ in range(50):
       path, terminal = stochastic_hc(landscape, 4)
       if terminal == 11:
          count += 1

    print("Reached 11:", count, "out of 50")


if __name__ == "__main__":
    main()   


