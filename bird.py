from random import randint
from mpmath import exp

# 2 entrées, niveau de l'oiseau et niveau de l'obstacle
# 3 neurones cachés
# 1 sortie, monter ou ne pas monter (0 ou 1)

# nombres d'arrêtes : 2*17 + 17*1 = 51
# nombres de biais : 17 + 1 = 18

# nombres d'arrêtes : 2*3 + 3*1 = 9
# nombres de biais : 3 + 1 = 4

NB_ARRETES = 9
NB_BIAIS = 4

class Bird:
    def __init__(self, weights :list =[], biais: list =[] ):
        self.w = weights
        self.b = biais
        if weights == [] and biais == []:
            self.init_random()
        
    def init_random(self):
        self.w = [randint(-100, 100) for i in range(NB_ARRETES)]
        self.b = [randint(-100, 100) for i in range(NB_BIAIS)]

    def f(self, x):
        return 1/(1+exp(-x))

    def move(self, inputs):
        # inputs = [niveau oiseau, niveau obstacle]
        hidden = []
        for i in range(NB_BIAIS-1):
            somme = self.f((inputs[0]+self.b[i]) * self.w[i*2] + (inputs[1]+self.b[i]) * self.w[i*2 + 1])
            if somme > 0.5:
                hidden.append(1)
            else:
                hidden.append(-1)
        
        somme_sortie = 0
        for i in range(NB_BIAIS-1):
            somme_sortie += hidden[i] * self.w[i+(NB_ARRETES + 1 - NB_BIAIS)]
        somme_sortie += self.b[NB_BIAIS-1]  # biais de la sortie
        somme_sortie = self.f(somme_sortie)

        if somme_sortie > 0.5:
            return 1  # monter
        else:
            return 0  # ne pas monter