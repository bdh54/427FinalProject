# Cristobal Camejo, Brendan Hendricks, Ethan Lichtblau

import numpy as np
import time
import matplotlib.pyplot as plt

# Class for 3SAT 
# n = # of variables
# m = # of clauses
# clauses = list of all the clauses we generate
class ThreeSAT:
   def __init__(self, n, m):
       self.n = n
       self.m = m 
       self.clauses = []

# Random Search 
class RandomSearch():
    # Initialize 3SAT for Random Search
    # keeps track of best solution and value
    def __init__(self, threeSat):
       self.threeSat = threeSat
       self.bestSolution = None
       self.bestValue = 0

    #Evaluate our boolean expressions, determine whether they are true or false
    def evaluate(self, assignment):
        satisfied = 0
        for clause in self.threeSat.clauses:
            for literal in clause:
                varIndex = abs(literal) - 1
                if (literal > 0) == (assignment[varIndex] == 1):
                    satisfied += 1
                    break
        return satisfied

    # Search for solutions to the 3SAT problem, combinations of values for our n variables
    # Save the best solution if one is found
    def search(self, maxTries=500):
       for _ in range(maxTries):
           solution = np.random.choice([0, 1], self.threeSat.n)
           value = self.evaluate(solution)
           if value > self.bestValue:
               self.bestValue = value
               self.bestSolution = solution.copy()
               
    def print_solution(self):
       print("Best solution:", self.bestSolution)
       print("Satisfied clauses:", self.bestValue)

# Exhaustive Search
class ExhaustiveSearch():
    
    # Initialize 3SAT for Exhaustive Search
    # keeps track of best solution and value
    def __init__(self, threeSat):
       self.threeSat = threeSat
       self.bestSolution = None
       self.bestValue = 0

    # Evaluate our boolean expressions, determine whether they are true or false   
    def evaluate(self, assignment):
        satisfied = 0
        for clause in self.threeSat.clauses:
            for literal in clause:
                varIndex = abs(literal) - 1
                if (literal > 0) == (assignment[varIndex] == 1):
                    satisfied += 1
                    break
        return satisfied
    
    # Brute forcing to find a best solution by searching through our 3SAT
    def search(self):
       for i in range(2 ** self.threeSat.n):
           solution = [(i >> j) & 1 for j in range(self.threeSat.n)]
           value = self.evaluate(solution)
           if value > self.bestValue:
               self.bestValue = value
               self.bestSolution = solution.copy()

    # Prints the solution          
    def print_solution(self):
       print("Best solution:", self.bestSolution)
       print("Satisfied clauses:", self.bestValue)

# Class to randomly create clauses
class RandomInstanceGeneration:
   
    # Initialize, check to make sure we don't have too many clauses
    def __init__(self, n, m):
       self.n = n
       self.m = m
       self.maxClauses = 8 * (n * (n-1) * (n-2) // 6)
       if m > self.maxClauses:
           raise ValueError(f"Too many clauses requested. Maximum possible is {self.maxClauses}")

    # Generates a random clause for the 3SAT      
    def generate(self):
       clauses = set()
       while len(clauses) < self.m:
           vars = tuple(sorted(np.random.choice(range(1, self.n + 1), 3, replace=False)))
           signs = tuple(np.random.choice([-1, 1], 3))
           clause = tuple(v * s for v, s in zip(vars, signs))
           clauses.add(clause)
       return list(clauses)

if __name__ == "__main__":
    print("\n=== Running Random Search Experiment ===")
   
    # Main experiment parameters
    nValues = [10, 15, 20, 25, 30]
    mValues = []
    for n in nValues:
        mValues.extend([
            int(n * 3), int(n * 4), int(n * 4.26), 
            int(n * 4.5), int(n * 5)
        ])
    trials = 500
    randomResults = []

   # Main experiment loop
    for n in nValues:
        for m in mValues:
            if m > 8 * (n * (n-1) * (n-2) // 6):
                continue
            
            successes = 0
            avgTime = 0

           
            for _ in range(trials):
                
                # Initialize necessary 3SAT pieces  
                instanceGen = RandomInstanceGeneration(n, m)
                clauses = instanceGen.generate()
                threeSat = ThreeSAT(n, m)
                threeSat.clauses = clauses
                
                # Find out time to search
                start = time.time()
                randomSearch = RandomSearch(threeSat)
                randomSearch.search()
                end = time.time()
                
                # If value is equal to best, add to success counter
                if randomSearch.bestValue == m:
                    successes += 1
                avgTime += (end - start)
            
            # Get average time and success rate
            avgTime /= trials
            successRate = successes / trials

            # Print results
            print(f"Random Search - n={n}, m/n={m/n:.2f}, success_rate={successRate:.2f}, avg_time={avgTime:.4f}s")
            randomResults.append((n, m/n, successRate, avgTime))

    # Plot Random Search Results
    plt.figure(figsize=(10, 6))
    
    #Plot results for success rates 
    for n in nValues:
        nResults = []
        for n_, r, successRate, _ in randomResults:
            if n_ == n:
                nResults.append((r, successRate))
        ratios, successRates = zip(*nResults)
        plt.plot(ratios, successRates, 'o-', label=f'n={n}')

    plt.axvline(x=4.26, color='red', linestyle='--', label='Critical Ratio')
    plt.xlabel('m/n ratio')
    plt.ylabel('Success Rate')
    plt.title('3SAT Phase Transition - Random Search')
    plt.legend()
    plt.grid(True)
    plt.show()

    #Plot the results for average time
    plt.figure(figsize=(10, 6))
    for ratio in ratios:
        ratioResults = []
        for n_, r, _, avgTime in randomResults:
            if r == ratio:
                ratioResults.append((n_, avgTime))
        ns, avgTimes = zip(*ratioResults)
        plt.plot(ns, avgTimes, 'o-', label=f'm/n={ratio:.2f}')

    plt.xlabel('Number of Variables (n)')
    plt.ylabel('Average Time (s)')
    plt.title('Solving Time vs Problem Size - Random Search')
    plt.legend()
    plt.yscale('log')
    plt.grid(True)
    plt.show()

    print("\n=== Running Verification with Exhaustive Search ===")
    
    # Verification parameters
    nValues = [5, 10]
    mValues = []
    for n in nValues:
        mValues.extend([
            int(n * 3), int(n * 4), int(n * 4.26), 
            int(n * 4.5), int(n * 5)
        ])
    trials = 50  # Fewer trials for exhaustive
    exhaustiveResults = []

    # Verification loop
    for n in nValues:
        for m in mValues:
            if m > 8 * (n * (n-1) * (n-2) // 6):
                continue
            
            successes = 0
            avgTime = 0
            
            for _ in range(trials):

                # Initialize necessary 3SAT pieces 
                instanceGen = RandomInstanceGeneration(n, m)
                clauses = instanceGen.generate()
                threeSat = ThreeSAT(n, m)
                threeSat.clauses = clauses
                
                # Find out time to search
                start = time.time()
                exhaustiveSearch = ExhaustiveSearch(threeSat)
                exhaustiveSearch.search()
                end = time.time()
                
                # If value is equal to best, add to success counter
                if exhaustiveSearch.bestValue == m:
                    successes += 1
                avgTime += (end - start)
            
            # Get average time and success rate
            avgTime /= trials
            successRate = successes / trials

            #Print results
            print(f"Exhaustive Search - n={n}, m/n={m/n:.2f}, success_rate={successRate:.2f}, avg_time={avgTime:.4f}s")
            exhaustiveResults.append((n, m/n, successRate, avgTime))

    # Plot Exhaustive Search Results
    plt.figure(figsize=(10, 6))

    #Plot the success rates
    for n in nValues:
        nResults = []
        for n_, r, successRate, _ in exhaustiveResults:
            if n_ == n:
                nResults.append((r, successRate))
        ratios, successRates = zip(*nResults)
        plt.plot(ratios, successRates, 'o-', label=f'n={n}')

    plt.axvline(x=4.26, color='red', linestyle='--', label='Critical Ratio')
    plt.xlabel('m/n ratio')
    plt.ylabel('Success Rate')
    plt.title('3SAT Phase Transition - Exhaustive Search')
    plt.legend()
    plt.grid(True)
    plt.show()

    #Plot the average times
    plt.figure(figsize=(10, 6))
    for ratio in ratios:
        ratioResults = []
        for n_, r, _, avgTime in exhaustiveResults:
            if r == ratio:
                ratioResults.append((n_, avgTime))
        ns, avgTimes = zip(*ratioResults)
        plt.plot(ns, avgTimes, 'o-', label=f'm/n={ratio:.2f}')

    plt.xlabel('Number of Variables (n)')
    plt.ylabel('Average Time (s)')
    plt.title('Solving Time vs Problem Size - Exhaustive Search')
    plt.legend()
    plt.yscale('log')
    plt.grid(True)
    plt.show()