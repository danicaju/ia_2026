""" Agent Minimax.

Mòdul en el qual es desenvolupa un agent Minimax amb poda alfa-beta per resoldre el problema del
Tic Tac Toe.

Creat per: Miquel Miró Nicolau (UIB), 2024
"""
from iaLib import agent
from tictac.solucio.estat import Estat


class Agent(agent.Agent):
    def __init__(self, poda=False):
        super(Agent, self).__init__(long_memoria=1)
        self.__visitats = None
        self.__cami_exit = None
        self.__poda = poda

    def cerca(self, estat: Estat, alpha, beta, torn_max=True):
        """ Minimax amb poda opcional.

        Retorna (estat, puntuació). La puntuació és +1 si guanya MAX, -1 si
        guanya MIN i 0 si és empat.
        """
        if estat in self.__visitats:
            return self.__visitats[estat]

        if estat.es_meta():
            if estat.guanyador():
                # el joc ha acabat: guanya qui acaba de moure, és a dir, el rival del torn
                resultat = (estat, 1 if not torn_max else -1)
            else:
                resultat = (estat, 0)
            self.__visitats[estat] = resultat
            return resultat

        puntuacions = []
        podat = False

        for fill in estat.genera_fills():
            punt_fill = self.cerca(fill, alpha, beta, not torn_max)
            puntuacions.append(punt_fill)

            if torn_max:
                alpha = max(alpha, punt_fill[1])
            else:
                beta = min(beta, punt_fill[1])

            if self.__poda and alpha >= beta:
                podat = True
                break

        index = self.__arg_max(puntuacions, not torn_max)
        resultat = puntuacions[index]

        # Amb poda el valor pot ser només una cota: només es guarda si s'han mirat tots els fills.
        if not podat:
            self.__visitats[estat] = resultat

        return resultat

    @staticmethod
    def __arg_max(puntuacions, reverse=False):
        """ Índex de la puntuació més alta, o la més baixa si reverse és True. """
        major_index = 0
        major_puntuacio = puntuacions[0][1] * (-1 if reverse else 1)

        for i, (_, puntuacio) in enumerate(puntuacions):
            valor = puntuacio * (-1 if reverse else 1)
            if valor > major_puntuacio:
                major_index = i
                major_puntuacio = valor

        return major_index

    def actua(self, percepcio):
        self.__visitats = dict()
        estat_inicial = Estat(percepcio["taulell"], percepcio["torn"])

        solucio, _ = self.cerca(estat_inicial, -float("inf"), float("inf"))

        if solucio.accions_previes:
            # les jugades pròpies són les de posició parella
            cami = [
                solucio.accions_previes[i]
                for i in range(len(solucio.accions_previes))
                if i % 2 == 0
            ]
            self.__cami_exit = cami
            return "P", cami[0]

        return "E"
