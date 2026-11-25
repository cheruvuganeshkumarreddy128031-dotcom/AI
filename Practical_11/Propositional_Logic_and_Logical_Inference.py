
facts = {"raining", "windy"}

print("=" * 60)
print("PRACTICAL 11: PROPOSITIONAL LOGIC AND LOGICAL INFERENCE")
print("=" * 60)
print("\nSTEP 1: INITIAL FACTS")
print("Initial facts:", facts)

rules = {
    "raining": "road_wet",
    "road_wet": "drive_carefully",
    "drive_carefully": "reduce_speed",
    "windy": "secure_loose_objects"
}

print("\nSTEP 2: LOGICAL RULES")
for condition, conclusion in rules.items():
    print(f"IF {condition} THEN {conclusion}")

print("\nSTEP 3: FORWARD CHAINING INFERENCE")
print("-" * 60)

changed = True
iteration = 1

while changed:
    changed = False
    print(f"\nIteration {iteration}")
    new_facts_found = False

    for condition, conclusion in rules.items():

        if condition in facts and conclusion not in facts:
            print(f"Rule applied: IF {condition} THEN {conclusion}")
       
            facts.add(conclusion)
            print(f"New fact derived: {conclusion}")
            changed = True
            new_facts_found = True

    if not new_facts_found:
        print("No new facts derived. Inference is complete.")
    iteration += 1


print("\nSTEP 4: FACTS AFTER INFERENCE")
print("-" * 60)
for fact in sorted(facts):
    print(fact)


print("\nSTEP 5: REASONING CHAINS")
print("-" * 60)
print("raining -> road_wet -> drive_carefully -> reduce_speed")
print("windy -> secure_loose_objects")


print("\nSTEP 6: FINAL CONCLUSION")
print("-" * 60)
print("Initial facts: raining, windy")
print("Final derived facts:")
for fact in ["road_wet", "drive_carefully", "reduce_speed", "secure_loose_objects"]:
    if fact in facts:
        print(f"- {fact}")

print("\nInference method: Forward Chaining")
print("Practical completed successfully.")
print("=" * 60)
