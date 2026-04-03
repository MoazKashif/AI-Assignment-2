import random

# ---------------- FITNESS FUNCTION ----------------
def count_conflicts(board):
    """Count the number of attacking pairs of queens."""
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i+1, n):
            if board[i] == board[j] or abs(board[i]-board[j]) == abs(i-j):
                conflicts += 1
    return conflicts

# ---------------- STOCHASTIC HC FOR N-QUEENS ----------------
def stochastic_hc_nqueens(board, max_sideways=50):
    """Perform Stochastic HC with optional sideways moves."""
    current_board = board.copy()
    current_conflicts = count_conflicts(current_board)
    sideways_moves = 0

    while current_conflicts > 0:
        # Generate all candidate swaps
        n = len(current_board)
        candidates = []
        for i in range(n):
            for j in range(i+1, n):
                new_board = current_board.copy()
                new_board[i], new_board[j] = new_board[j], new_board[i]
                new_conflicts = count_conflicts(new_board)
                if new_conflicts < current_conflicts:
                    candidates = [(new_board, new_conflicts)]
                    break  # accept first better
                elif new_conflicts == current_conflicts:
                    candidates.append((new_board, new_conflicts))
            if candidates:
                break

        if not candidates:
            # No improving or plateau moves left
            break

        # Randomly pick one candidate (best or plateau)
        next_board, next_conflicts = random.choice(candidates)

        # Sideways move check
        if next_conflicts == current_conflicts:
            sideways_moves += 1
            if sideways_moves > max_sideways:
                break
        else:
            sideways_moves = 0  # reset on improvement

        current_board = next_board
        current_conflicts = next_conflicts

    return current_board, current_conflicts

# ---------------- RANDOM RESTART N-QUEENS ----------------
def solve_nqueens_rrhc(num_restarts, n=8):
    """Random Restart Stochastic HC for N-Queens."""
    for restart in range(1, num_restarts+1):
        board = [random.randint(0, n-1) for _ in range(n)]
        solution, conflicts = stochastic_hc_nqueens(board)
        if conflicts == 0:
            return restart, solution
    return None, None

# ---------------- RUN BENCHMARK ----------------
def benchmark_nqueens():
    ks = [5, 10, 25, 50, 100]
    trials = 30
    n = 8
    print(f"{'Restarts (k)':<12}{'Success Rate':<15}{'Avg Restarts':<15}")
    for k in ks:
        successes = 0
        total_restarts = 0
        for _ in range(trials):
            restart_used, solution = solve_nqueens_rrhc(k, n)
            if solution is not None:
                successes += 1
                total_restarts += restart_used
        success_rate = successes / trials
        avg_restarts = (total_restarts / successes) if successes > 0 else 0
        print(f"{k:<12}{success_rate:<15.2f}{avg_restarts:<15.2f}")

# ---------------- VISUALIZATION ----------------
def print_board(board):
    n = len(board)
    for r in range(n):
        line = ""
        for c in range(n):
            line += "Q " if board[c] == r else ". "
        print(line)
    print("\n")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    random.seed(42)

    # Example: single solution visualization
    restart_used, solution = solve_nqueens_rrhc(100)
    if solution:
        print(f"Solution found after {restart_used} restart(s):\n")
        print_board(solution)
    else:
        print("No solution found within restart limit.")

    print("\nBenchmark Results:")
    benchmark_nqueens()
