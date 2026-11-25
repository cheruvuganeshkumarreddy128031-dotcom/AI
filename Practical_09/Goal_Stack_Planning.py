

initial_state = {
    "on": {"C": "A"},         
    "on_table": {"A", "B"},    
    "clear": {"B", "C"},      
}

goal_stack = [
    ("ON", "A", "B"),
    ("ON", "B", "C"),
]

class BlocksWorldState:
    def __init__(self, on, on_table, clear):
        self.on = dict(on)
        self.on_table = set(on_table)
        self.clear = set(clear)

    def clone(self):
        return BlocksWorldState(self.on, self.on_table, self.clear)

    def is_clear(self, block):
        return block in self.clear

    def is_on_table(self, block):
        return block in self.on_table

    def is_on(self, x, y):
        return self.on.get(x) == y

    def describe(self):
        parts = []
        for b, base in self.on.items():
            parts.append(f"{b} on {base}")
        for b in self.on_table:
            parts.append(f"{b} on Table")
        return ", ".join(sorted(parts))

def move(state, block, dest):
    """STRIPS operator: move(block, dest)
    Preconditions: block is clear, dest is clear (or Table), block not already on dest
    Effects: block on dest; old location of block becomes clear;
             dest is no longer clear (unless dest == Table)."""
    plan_step = f"MOVE({block} -> {dest})"
    old_base = state.on.get(block, "Table" if state.is_on_table(block) else None)

   
    if block in state.on:
        del state.on[block]
    state.on_table.discard(block)

   
    if old_base and old_base != "Table":
        state.clear.add(old_base)

    if dest == "Table":
        state.on_table.add(block)
    else:
        state.on[block] = dest
        state.clear.discard(dest)

    state.clear.add(block) 
    return plan_step

def goal_stack_plan(state, goals):
    """Simplified goal-stack planning algorithm."""
    stack = list(goals) 
    plan = []
    trace = []
    step_no = 0

    while stack:
        goal = stack.pop()
        step_no += 1
        predicate, x, y = goal
        trace.append(f"Step {step_no}: Consider goal {predicate}({x}, {y})")

        if predicate == "ON":
            if state.is_on(x, y):
                trace.append(f"  -> already satisfied: {x} is on {y}")
                continue

           
            sub_goals = []
            if not state.is_clear(y) and y != "Table":
                sub_goals.append(("CLEAR", y, None))
            if not state.is_clear(x):
                sub_goals.append(("CLEAR", x, None))

            if sub_goals:
                trace.append(f"  -> preconditions not met, pushing sub-goals: {sub_goals}")
                stack.append(goal) 
                stack.extend(reversed(sub_goals))
            else:
                action = move(state, x, y)
                plan.append(action)
                trace.append(f"  -> action applied: {action}")
                trace.append(f"     state now: {state.describe()}")

        elif predicate == "CLEAR":
            if state.is_clear(x):
                trace.append(f"  -> already satisfied: {x} is clear")
                continue

           
            on_top = None
            for b, base in state.on.items():
                if base == x:
                    on_top = b
                    break
            if on_top:
                action = move(state, on_top, "Table")
                plan.append(action)
                trace.append(f"  -> action applied: {action}")
                trace.append(f"     state now: {state.describe()}")

    return plan, trace

if __name__ == "__main__":
    print("=" * 65)
    print("STRIPS / GOAL-STACK PLANNING - BLOCKS WORLD")
    print("=" * 65)

    state = BlocksWorldState(**initial_state)
    print("\nInitial State :", state.describe())
    print("Goal Stack    :", goal_stack)
    print("-" * 65)

    plan, trace = goal_stack_plan(state, goal_stack)

    print("\nPlanning Trace:")
    for line in trace:
        print(line)

    print("-" * 65)
    print("\nFinal Plan (sequence of actions):")
    for i, action in enumerate(plan, start=1):
        print(f"  {i}. {action}")

    print("\nFinal State   :", state.describe())
    print("=" * 65)
