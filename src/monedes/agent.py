""" Mòdul que conté l'agent per jugar al joc de les monedes.

Percepcions:
    ClauPercepcio.MONEDES
Solució:
    " XXXC"
"""

from queue import PriorityQueue

from iaLib import agent

from monedes.solucio.estat import Estat

SOLUCIO = " XXXC"


class AgentMoneda(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=0)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)

    def cerca(self, estat_inicial: Estat) -> None:
        """ A*: la frontera s'ordena per f(n) = g(n) + h(n). """
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        self.__oberts.put((estat_inicial.calc_heuristica(), estat_inicial))

        actual = estat_inicial
        while not self.__oberts.empty():
            _, actual = self.__oberts.get()

            if actual in self.__tancats:
                continue

            if actual.es_meta():
                self.__accions = actual.accions_previes
                return

            for estat_fill in actual.genera_fills():
                self.__oberts.put((estat_fill.calc_heuristica(), estat_fill))

            self.__tancats.add(actual)

        self.__accions = []

    def actua(self, percepcio):
        if self.__accions is None:
            estat_inicial = Estat(list(percepcio["Monedes"]), 0)
            self.cerca(estat_inicial)

        if self.__accions:
            accio, posicio = self.__accions.pop(0)
            return accio, posicio

        return "R", None
