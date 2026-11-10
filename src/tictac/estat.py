import copy

class Estat:
    def __init__(self, taulell, torn, ultimaPosicio = None):
        self.taulell = taulell
        self.torn = torn
        self.ultimaPosicio = ultimaPosicio

    def accions_possibles(self):
        accions = []
        for x in range(len(self.taulell))
            for y in range(len(self.taulell))
                if (self.taulell[x][y] == ' '):
                    accions.append((x,y))
        return accions

    def genera_fill(self, accio, tablero_original):
        tauler_nou = copy.deepcopy(tablero_original)