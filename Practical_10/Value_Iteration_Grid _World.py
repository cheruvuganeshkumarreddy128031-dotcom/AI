

ROWS, COLS = 4, 4

GOAL = (0, 3)
PIT = (1, 3)
WALL = (1, 1)

REWARD_STEP = -0.04
REWARD_GOAL = 1.0
REWARD_PIT = -1.0

GAMMA = 0.9
THETA = 1e-4

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

ACTION_DELTA = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}


PERPENDICULAR = {
    "UP": ["LEFT", "RIGHT"],
    "DOWN": ["LEFT", "RIGHT"],
    "LEFT": ["UP", "DOWN"],
    "RIGHT": ["UP", "DOWN"],
}

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS and (r, c) != WALL

def next_state(state, action):
    dr, dc = ACTION_DELTA[action]
    r, c = state[0] + dr, state[1] + dc
    if in_bounds(r, c):
        return (r, c)
    return state 

def reward(state):
    if state == GOAL:
        return REWARD_GOAL
    if state == PIT:
        return REWARD_PIT
    return REWARD_STEP

def is_terminal(state):
    return state == GOAL or state == PIT

def expected_value(state, action, V):
    total = 0.0
    intended_prob = 0.8
    perpendicular_prob = 0.1
    transitions = [(action, intended_prob)] + [(pa, perpendicular_prob) for pa in PERPENDICULAR[action]]
    for a, p in transitions:
        ns = next_state(state, a)
        total += p * V[ns]
    return total

def value_iteration():
    V = {(r, c): 0.0 for r in range(ROWS) for c in range(COLS) if (r, c) != WALL}
    iteration = 0
    while True:
        delta = 0.0
        new_V = V.copy()
        for state in V:
            if is_terminal(state):
                new_V[state] = reward(state)
                continue
            action_values = [
                reward(state) + GAMMA * expected_value(state, a, V)
                for a in ACTIONS
            ]
            best_value = max(action_values)
            new_V[state] = best_value
            delta = max(delta, abs(best_value - V[state]))
        V = new_V
        iteration += 1
        if delta < THETA:
            break
    return V, iteration

def extract_policy(V):
    policy = {}
    for state in V:
        if is_terminal(state):
            policy[state] = "."
            continue
        best_action = max(ACTIONS, key=lambda a: expected_value(state, a, V))
        policy[state] = best_action
    return policy

ARROWS = {"UP": "^", "DOWN": "v", "LEFT": "<", "RIGHT": ">", ".": "."}

def print_grid(values_or_policy, is_policy=False):
    for r in range(ROWS):
        row_str = []
        for c in range(COLS):
            state = (r, c)
            if state == WALL:
                row_str.append("#####")
            elif is_policy:
                row_str.append(f"  {ARROWS[values_or_policy[state]]}  ")
            else:
                row_str.append(f"{values_or_policy[state]:+.2f}")
        print("|".join(row_str))
    print("-" * 35)

if __name__ == "__main__":
    print("=" * 60)
    print("VALUE ITERATION - 4x4 STOCHASTIC GRID WORLD")
    print("=" * 60)
    print(f"\nGoal (+{REWARD_GOAL}) at {GOAL} | Pit ({REWARD_PIT}) at {PIT} | Wall at {WALL}")
    print(f"Step reward: {REWARD_STEP} | Discount (gamma): {GAMMA}")
    print("Transition model: 0.8 intended direction, 0.1/0.1 perpendicular slip")

    V, iterations = value_iteration()
    policy = extract_policy(V)

    print(f"\nConverged after {iterations} iterations (theta = {THETA})")
    print("\nOptimal State Values V(s):")
    print("-" * 35)
    print_grid(V, is_policy=False)

    print("\nOptimal Policy (pi*):")
    print("-" * 35)
    print_grid(policy, is_policy=True)
    print("=" * 60)
