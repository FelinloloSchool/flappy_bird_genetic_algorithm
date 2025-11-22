from bird import Bird
from game import Game
from random import randint
from time import sleep

class Population:
    def __init__(self, nb, id):
        self.id = id
        self.pop = []
        self.scores = [0 for _ in range(nb)]
        for i in range(nb):
            self.pop.append(Bird())
        with open(f"config_{self.id}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(["  ".join([" ".join([str(i) for i in b.b])," ".join([str(i) for i in b.w])]) for b in self.pop]))
        self.gen = 1

    def test_generation(self, affichage=False, affichage_maximum=0, taille = 24):
        self.scores = Game().run_population(self, (taille, taille), affichage)
        scores_sorted = sorted(self.scores, reverse=True)
        if affichage_maximum > 0:
            print(f"--- Meilleurs scores de la génération {self.gen} ---")
            for i in range(min(affichage_maximum, len(scores_sorted))):
                print(f"Oiseau {i+1} : Score = {scores_sorted[i]}")
            print("Moyenne : ", sum(scores_sorted)/len(scores_sorted))
            if affichage:
                sleep(1)

    def next_generation(self):
        scored_birds = list(zip(self.pop, self.scores))
        scored_birds.sort(key=lambda x: x[1], reverse=True)
        top_half = scored_birds[:len(scored_birds)//2] 
        new_pop = []
        for bird, score in top_half:
            new_pop.append(bird)
            # Crossover et mutation pour créer un nouvel oiseau
            weights1 = bird.w
            biais1 = bird.b
            partner = top_half[randint(0, len(top_half)-1)][0]
            weights2 = partner.w
            biais2 = partner.b
            weight_partner1 = randint(0, 100)/100
            new_weights = [weights1[i]*weight_partner1+weights2[i]*(1-weight_partner1) for i in range(len(weights1))]
            new_biais = [biais1[i]*weight_partner1+biais2[i]*(1-weight_partner1) for i in range(len(biais1))]
            # Mutation
            for i in range(len(new_weights)):
                if randint(0, 100) < 10:  # 10% de chance de mutation
                    new_weights[i] += randint(-20, 20)
            for i in range(len(new_biais)):
                if randint(0, 100) < 10:  # 10% de chance de mutation
                    new_biais[i] += randint(-20, 20)
            new_pop.append(Bird(new_weights, new_biais))
        self.pop = new_pop
        self.gen += 1
        with open(f"config_{self.id}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(["  ".join([" ".join([str(i) for i in b.b])," ".join([str(i) for i in b.w])]) for b in self.pop]))