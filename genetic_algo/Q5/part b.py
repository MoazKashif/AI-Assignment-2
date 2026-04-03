import random

# ------------------------ HELPER FUNCTIONS ------------------------
rooms = [0, 1, 2]
slots = [0, 1, 2, 3]

# Generate random valid chromosome
def random_chromosome():
    return [(random.choice(rooms), random.choice(slots)) for _ in range(6)]

# Count conflicts in a schedule
def count_conflicts(chromosome):
    conflicts = 0
    n = len(chromosome)
    for i in range(n):
        for j in range(i+1, n):
            if chromosome[i] == chromosome[j]:
                conflicts += 1
    return conflicts

# Fitness function
def fitness(chromosome):
    return 100 - 10 * count_conflicts(chromosome)

# ------------------------ CROSSOVER ------------------------
def crossover(p1, p2, point):
    """Single-point crossover"""
    o1 = p1[:point] + p2[point:]
    o2 = p2[:point] + p1[point:]
    return o1, o2

# ------------------------ REPAIR ------------------------
def repair(chromosome):
    """Reassign conflicting courses to random conflict-free slots"""
    seen = {}
    for i, gene in enumerate(chromosome):
        if gene in seen:
            # Conflict detected: reassign to random conflict-free slot
            available = [(r,s) for r in rooms for s in slots if (r,s) not in chromosome[:i]]
            if available:
                chromosome[i] = random.choice(available)
            else:
                # If no free slot, assign completely random
                chromosome[i] = (random.choice(rooms), random.choice(slots))
        else:
            seen[gene] = True
    return chromosome

# ------------------------ MUTATION ------------------------
def mutate(chromosome, pm):
    """Per-gene mutation with probability pm"""
    for i in range(len(chromosome)):
        if random.random() < pm:
            chromosome[i] = (random.choice(rooms), random.choice(slots))
    return chromosome

# ------------------------ DEMONSTRATION ------------------------

# Example crossover
parent1 = [(0,0),(1,1),(2,2),(0,1),(1,0),(2,3)]
parent2 = [(1,0),(0,1),(1,1),(2,2),(0,0),(1,3)]
print("Parent1:", parent1)
print("Parent2:", parent2)

child1, child2 = crossover(parent1, parent2, 3)
print("\nAfter Crossover (point=3):")
print("Child1:", child1, "Conflicts:", count_conflicts(child1))
print("Child2:", child2, "Conflicts:", count_conflicts(child2))

# Example repair
conflicting_chrom = [(0,0),(0,0),(1,1),(1,1),(2,2),(2,2)]
print("\nConflicting Chromosome:", conflicting_chrom, "Conflicts:", count_conflicts(conflicting_chrom))
repaired = repair(conflicting_chrom.copy())
print("After Repair:", repaired, "Conflicts:", count_conflicts(repaired))

# Example mutation
mutated = mutate(repaired.copy(), 0.2)
print("\nAfter Mutation (pm=0.2):", mutated, "Conflicts:", count_conflicts(mutated))
