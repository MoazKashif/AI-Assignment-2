import random

N = 8

# ---------------- FITNESS FUNCTION ----------------
def count_conflicts(board):
    conflicts = 0
    for i in range(N):
        for j in range(i+1, N):
            if board[i] == board[j] or abs(board[i]-board[j]) == abs(i-j):
                conflicts += 1
    return conflicts

# ---------------- STOCHASTIC HC FOR N-QUEENS ----------------
def stochastic_hc_nqueens(board):
    current_board = board[:]
    current_conflicts = count_conflicts(current_board)
    
    while True:
        neighbors = []
        # generate all swap neighbors that improve conflicts
        for i in range(N):
            for j in range(i+1, N):
                neighbor = current_board[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                conflicts = count_conflicts(neighbor)
                if conflicts < current_conflicts:
                    neighbors.append((neighbor, conflicts))
        if not neighbors:
            break  # no improving neighbor found
        # pick one improving neighbor randomly
        current_board, current_conflicts = random.choice(neighbors)
        if current_conflicts == 0:
            break
    return current_board, current_conflicts

# ---------------- RANDOM RESTART HC ----------------
def solve_nqueens_rrhc(num_restarts=100):
    for restart in range(1, num_restarts+1):
        board = list(range(N))
        random.shuffle(board)
        final_board, conflicts = stochastic_hc_nqueens(board)
        if conflicts == 0:
            return restart, final_board
    return None, None  # solution not found

# ---------------- PRINT BOARD ----------------
def print_board(board):
    for row in board:
        line = ['.'] * N
        line[row] = 'Q'
        print(' '.join(line))
    print()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    random.seed(42)
    restarts_needed, solution = solve_nqueens_rrhc(num_restarts=100)
    if solution:
        print(f"Solution found after {restarts_needed} restart(s):\n")
        print_board(solution)
    else:
        print("No solution found within restart limit.")
