import random
import matplotlib.pyplot as plt
# --- reuse previous functions (decode, fitness, etc.) ---
#NOTE: just copy paste the functions from part a here and it will work 
#also there are two run functions so run them one by one (last one is for graph)
def run_ga_once(pop_size, num_generations, pm, elitism):
    population = [[random.randint(0,1) for _ in range(4)] for _ in range(pop_size)]
    
    best_fitness = float('-inf')
    found_optimal = False
    gen_to_50 = None

    for gen in range(num_generations):
        fits = [fitness(ind) for ind in population]
        
        current_best = max(fits)
        best_fitness = max(best_fitness, current_best)
        
        if current_best >= 50 and gen_to_50 is None:
            gen_to_50 = gen
        
        if 54 in fits:
            found_optimal = True
        
        # next generation
        new_population = []
        
        if elitism:
            best_idx = fits.index(max(fits))
            new_population.append(population[best_idx][:])
        
        while len(new_population) < pop_size:
            p1 = roulette_select(population)
            p2 = roulette_select(population)
            
            c1, c2 = single_point_crossover(p1, p2)
            c1 = mutate(c1, pm)
            c2 = mutate(c2, pm)
            
            new_population.append(c1)
            if len(new_population) < pop_size:
                new_population.append(c2)
        
        population = new_population[:pop_size]

    return best_fitness, found_optimal, gen_to_50


# ---------- ELITISM VS NO ELITISM ----------
def experiment_elitism():
    trials = 30
    
    for elitism in [False, True]:
        total_best = 0
        optimal_count = 0
        total_gen50 = 0
        gen50_count = 0
        
        for _ in range(trials):
            best, found, gen50 = run_ga_once(4, 20, 0.1, elitism)
            
            total_best += best
            if found:
                optimal_count += 1
            if gen50 is not None:
                total_gen50 += gen50
                gen50_count += 1
        
        avg_best = total_best / trials
        avg_gen50 = total_gen50 / gen50_count if gen50_count > 0 else 0
        
        print(f"\nElitism = {elitism}")
        print(f"Avg Best Fitness: {avg_best:.2f}")
        print(f"Found x=7: {optimal_count}/30")
        print(f"Avg Gen to f>=50: {avg_gen50:.2f}")


# ---------- MUTATION RATE EXPERIMENT ----------
def experiment_mutation():
    trials = 30
    rates = [0.01, 0.1, 0.3, 0.5]
    
    print("\nMutation Rate Results:")
    print("pm\tAvg Best Fitness")
    
    for pm in rates:
        total_best = 0
        
        for _ in range(trials):
            best, _, _ = run_ga_once(4, 20, pm, False)
            total_best += best
        
        avg_best = total_best / trials
        print(f"{pm}\t{avg_best:.2f}")


# # ---------- RUN ----------
# random.seed(42)

# experiment_elitism()
# experiment_mutation()

# #Fitness curve: 
# import random
# import matplotlib.pyplot as plt

# reuse your existing functions:
# decode, fitness, roulette_select, single_point_crossover, mutate

def run_ga_for_graph(pop_size, num_generations, pm, elitism=False):
    population = [[random.randint(0,1) for _ in range(4)] for _ in range(pop_size)]
    
    best_fitness_per_gen = []

    for gen in range(num_generations):
        fits = [fitness(ind) for ind in population]
        best_fitness_per_gen.append(max(fits))
        
        new_population = []
        
        if elitism:
            best_idx = fits.index(max(fits))
            new_population.append(population[best_idx][:])
        
        while len(new_population) < pop_size:
            p1 = roulette_select(population)
            p2 = roulette_select(population)
            
            c1, c2 = single_point_crossover(p1, p2)
            c1 = mutate(c1, pm)
            c2 = mutate(c2, pm)
            
            new_population.append(c1)
            if len(new_population) < pop_size:
                new_population.append(c2)
        
        population = new_population[:pop_size]
    
    return best_fitness_per_gen


# RUN
random.seed(42)
fitness_values = run_ga_for_graph(4, 20, 0.1, elitism=False)

# PLOT (IMPORTANT: no color specified as per rules)
plt.plot(fitness_values, marker='o')
plt.xlabel("Generation")
plt.ylabel("Best Fitness")
plt.title("Fitness Curve (Best Fitness vs Generation)")
plt.grid()

# SAVE IMAGE
plt.savefig("fitness_curve.png")
plt.show()
