import random

# ---------------- GA Representation ----------------
NUM_COURSES = 6
NUM_ROOMS = 3
NUM_SLOTS = 4

def random_chromosome():
    """Generates a random chromosome as a list of (room, slot) for each course"""
    return [(random.randint(0, NUM_ROOMS-1), random.randint(0, NUM_SLOTS-1)) 
            for _ in range(NUM_COURSES)]

def count_conflicts(chromosome):
    """Counts number of pairs of courses in same room & same slot"""
    conflicts = 0
    for i in range(len(chromosome)):
        for j in range(i+1, len(chromosome)):
            if chromosome[i] == chromosome[j]:
                conflicts += 1
    return conflicts

def fitness(chromosome):
    """Fitness function: higher is better (max 100 if no conflicts)"""
    return 100 - 10 * count_conflicts(chromosome)

# ---------------- Generate & Print 5 Random Chromosomes ----------------
print(f"{'Chromosome':>30} | {'Conflicts':>8} | {'Fitness':>6}")
print("-"*55)
for _ in range(5):
    chrom = random_chromosome()
    conf = count_conflicts(chrom)
    fit = fitness(chrom)
    print(f"{str(chrom):>30} | {conf:>8} | {fit:>6}")
