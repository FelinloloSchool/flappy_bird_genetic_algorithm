from bird import Bird
from population import Population
from game import Game
from time import time

if __name__ == "__main__":
    a = time()
    pop = Population(100, 0)
    for _ in range(10000):
        pop.test_generation(affichage=True, affichage_maximum=3, taille = 24)
        pop.next_generation()
    b = time()

    print(f"Temps total : {b-a}")