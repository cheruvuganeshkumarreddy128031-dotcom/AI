

N = 8
backtrack_count = 0
consistency_checks = 0

def is_consistent(row, col, placement):
    """Check row/col/diagonal consistency against already-placed queens."""
    global consistency_checks
    for r, c in enumerate(placement[:row]):
        consistency_checks += 1
        if c is None:
            continue
        if c == col:
            return False
        if abs(c - col) == abs(r - row): 
            return False
    return True

def forward_check(domains, row, col, n):
    """Remove col & diagonal values from domains of rows below `row`.
    Returns the removed values so they can be restored on backtrack,
    and a boolean indicating if all remaining domains are non-empty."""
    removed = {}
    for r in range(row + 1, n):
        to_remove = set()
        for c in domains[r]:
            if c == col or abs(c - col) == (r - row):
                to_remove.add(c)
        if to_remove:
            removed[r] = to_remove
            domains[r] -= to_remove
        if not domains[r]:
            return removed, False
    return removed, True

def backtrack(row, placement, domains, n):
    global backtrack_count
    if row == n:
        return True

    for col in sorted(domains[row]):
        if is_consistent(row, col, placement):
            placement[row] = col
            removed, ok = forward_check(domains, row, col, n)
            if ok and backtrack(row + 1, placement, domains, n):
                return True

         
            for r, vals in removed.items():
                domains[r] |= vals
            placement[row] = None
            backtrack_count += 1
    return False

def solve_n_queens(n):
    placement = [None] * n
    domains = [set(range(n)) for _ in range(n)]
    success = backtrack(0, placement, domains, n)
    return placement if success else None

def print_board(placement, n):
    for r in range(n):
        row_cells = []
        for c in range(n):
            row_cells.append("Q" if placement[r] == c else ".")
        print(" ".join(row_cells))

if __name__ == "__main__":
    print("=" * 55)
    print(f"N-QUEENS CSP (N = {N})")
    print("Backtracking + Forward Checking")
    print("=" * 55)

    solution = solve_n_queens(N)
    if solution:
        print("\nSolution Found:\n")
        print_board(solution, N)
        print("\nQueen positions (row -> column):")
        for r, c in enumerate(solution):
            print(f"  Row {r} -> Column {c}")
    else:
        print("No solution found.")

    print("-" * 55)
    print(f"Backtracks performed    : {backtrack_count}")
    print(f"Consistency checks made : {consistency_checks}")
    print("=" * 55)
