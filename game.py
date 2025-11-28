from bird import Bird
from random import randint
from time import time, sleep
from os import system, name

def clear_screen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

class Game:
    def __init__(self, width=24, height=24):
        self.width = width
        self.height = height
        self.plateau = [[0 for _ in range(width)] for _ in range(height)]
        self.bird_position = height // 2
        self.plateau[self.bird_position][width // 10] = 1  # Position initiale de l'oiseau
        self.ajout_tuyau()
    
    def ajout_tuyau(self):
        #On rajoute un tuyau que si les 5 dernieres colonnes sont vides
        tuyau = self.position_tuyau()
        if tuyau == None: 
            tuyau = self.height//5
        else:
            tuyau = tuyau[1]
        nb_lignes = randint(5, 10)
        if all(self.plateau[i][self.width - j - 1] == 0 for i in range(self.height) for j in range(nb_lignes)):
            #création des 2 bouts de tuyau
            espace = 4
            gap_start = randint(self.height//3, self.height - espace - self.height//3)
            for i in range(self.height):
                if i < gap_start or i > gap_start + espace:
                    self.plateau[i][self.width - 1] = -1  # Tuyau représenté par -1

    def position_tuyau(self):
        # Position du bas du tuyau le plus proche
        for j in range(self.width):
            for i in range(self.height):
                if self.plateau[i][j] == -1:
                    for i2 in range(i+1, self.width):
                        if self.plateau[i2][j] == 0:
                            return ((i2-1), j)
        return None

    def position_oiseau(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.plateau[i][j] == 1:
                    return i, j
        return None
    
    def afficher(self, id, gen):
        clear_screen()
        # Vert : tuyau, Bleu : oiseau,  bleu : espace vide
        print("Gen : ", gen)
        print(id)
        for row in self.plateau:
            print("".join(reversed(['🟦' if cell == 0 else '🐤' if cell == 1 else '🟩' for cell in row])))
        print("\n")

    def run_population(self, population, taille, affichage=False):
        # Simuler le jeu pour chaque oiseau dans la population
        scores = []
        oiseau = 0
        for bird in population.pop:
            fini = False
            score = 0
            while not fini: 
                # Logique de simulation pour chaque oiseau
                pos = self.position_oiseau()
                tuy = self.position_tuyau()
                if bird.move(((self.height//2 - pos[0]),(tuy[0]- pos[0]))) == 1:
                    mouvement = max(0, self.bird_position - 1)  # Monter
                else:
                    mouvement = min(self.height - 1, self.bird_position + 1)  # Descendre

                # Vérifier les collisions et mettre à jour le score
                if self.plateau[mouvement][self.width // 10+1] == -1:
                    diff = (abs(tuy[0]-pos[0])/self.height)
                    assert diff < 1
                    scores.append(score-diff)
                    fini = True
                if score > 1000:
                    scores.append(score)
                    fini = True
                else:
                    self.plateau[self.bird_position][self.width//10]  = 0
                    self.bird_position = mouvement
                    self.plateau[self.bird_position][self.width//10]  = 1
                    if tuy[1] == pos[1]:
                        score += 1
                    # Mettre à jour le plateau, garder les tuyaux en mouvement, etc. et la position de l'oiseau
                    self.plateau = [row[1:] + [0] for row in self.plateau]  # Déplacer les tuyaux vers la gauche
                    self.plateau[self.bird_position][self.width//10 - 1] = 0
                    self.plateau[self.bird_position][self.width//10]  = 1
                    self.ajout_tuyau()
                    if oiseau<3 and (population.gen%10 == 0 or population.gen == 1) and affichage: #  
                        self.afficher(oiseau, population.gen)
                        sleep(0.1)
            oiseau += 1
            self.__init__(taille[0], taille[1])
        return scores

                





