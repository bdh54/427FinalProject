CSC427 Final Project
Mitsu Ogihara
deadline: 11:59 PM, Monday, December 2, 2024
The project aims to develop heuristic solutions for 3SAT and test their efficiency.
1 3SAT
A Boolean formula is in the 3-conjunctive normal form (3CNF) if it is the con- junction (AND) of 3-literal disjunctive clauses (OR of three literals), where a literal is a variable or its negation. An example of 3CNF formulas is:
(x1 ∨x2 ∨x3)∧(x1 ∨x2 ∨x4)∧(x2 ∨x4 ∨x3).
A truth assignment for a Boolean formula with variables x1, . . . , xm is a collection of m individual assignments to the variables. For the formula in the above, sixteen possible truth assignments exist. We often write φ(A) to present the value of φ when it takes the assignment A.
3SAT is a problem of deciding the satisfiability of 3CNF formulas. The 3SAT problem is NP-complete. The completeness places 3SAT in the group of most difficult problems in NP. It is unlikely that we have efficient deter- ministic algorithms to solve 3SAT.
2 Heuristics
We can think of the following heuristics.
1. DPLL (Davis-Putnam-Logemann-Loveland): This is a divide-and-conquer algorithm to search for a satisfying assignment. At each branching
1
point, a variable still appearing in the formula is chosen for receiving a value assignment. The following strategy is used to choose the variable (and its assignment if no branching is necessary):
(a) Pure Rule: If any variable appears only positive or only negative, you can choose the variable and assign, to the variable, the value that satisfies the literals (i.e., the assignment is TRUE if the vari- able appears only positively, FALSE if the variable appears only negatively).
(b) Unit Rule: If any clause has only one literal, choose the assignment that satisfies the literal.
(c) Two-clause Rule: Create two branches if the formula has a 2- literal clause (α ∨ β). One branch is the one satisfying α, and the other is the one satisfying not satisfying α and satisfying β.
(d) If none of the above are applicable, select a variable that appears the most in the formula and create two branches, one with the as- signment TRUE to the variable and the other with the assignment FALSE to the variable.
After making the assignment(s), simplify the formula by reducing each literal whose variable has received a value:
• If a literal received the value TRUE in a clause, remove the clause as being satisfied.
• If a literal received the value FALSE in a clause, remove the literal from the clause.
• If a clause without literals has appeared, no extensions of the present partial assignment are satisfying assignments, so give up the branch.
• If the formula has no more clauses remaining, assert that the for- mula is satisfiable and report the partial assignment.
2. Random Search: Select an assignment by choosing one from the 2n candidate assignments with an equal probability. Then repeat the fol- lowing at most n times:
(a) If the present assignment is satisfying, the search has been suc- cessful; report the assignment.
2

3
3.
(b) Otherwise, pick an arbitrary clause that is not satisfied, pick an arbitrary literal in the clause, and flip the assignment for the vari- able.
Repeat the random search a given number of times. Assert that the formula is unsatisfiable if none of the attempts produced a satisfying assignment.
Exhaustive Search: Given a formula with n variables, say, x1 , . . . , xn , execute the exhaustive search by creating branches using the variable with the smallest index among those remaining variables. If one sat- isfies the formula, the formula is satisfiable; otherwise, the formula is unsatisfiable.
Random Instances
A formula over n may have 8 · · · (n(n − 1)(n − 2)/6) different three-literal clauses (the number of choices for three distinct variables times eight possible positive/negative assignments). A random 3CNF formula can be constructed by selecting some m clauses from the candidate pool and connecting them with ∧. This gives an idea for a random instance generation for 3SAT: receive n and m and randomly select m clauses.
It is known that the satisfiability of a random formula generated in this manner is heavily affected by the ratio m/n; the higher the ratio, the less likely that the formula is satisfiable. Specifically, 4.26 is known to be a critical ratio. For all k = m/n < 4.26, a random formula generated with the ratio is likely satisfiable. For all k = m/n > 4.26, a random formula generated with the ratio is likely unsatisfiable. This drastic difference is called the phase transition in 3SAT. It is thus interesting to conduct instance generation using a range of ratios covering the critical quantity 4.26.
4
1. 2. 3.
Your Assignment
Write a code for either DPLL or Random Search.
Write a code for Exhaustive Search (for verification and benchmarking). Write a code for Random Instance Generation.
3

4. Conduct experiments with a range of values for n and a set of values for m/n.
5. Write a report presenting the results from the experiment. Be sure to include your code design.
6. Submit the code and the report.
