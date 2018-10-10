from SemanticTableaux import SemanticTableaux
from multiprocessing import Pool

def solve(x):
    SemanticTableaux().solve(x)

p = Pool(5)
p.map(solve, ["input/p1.txt", "input/p2.txt", "input/p3.txt", "input/p4.txt"])