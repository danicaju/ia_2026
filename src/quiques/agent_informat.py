""" Fitxer que conté l'agent informat.

S'ha d'implementar el mètode:
    actua()
"""

from itertools import count
from queue import PriorityQueue

from quiques.agent import Barca
from quiques.estat import Estat


class BarcaGreedy(Barca):
    def __init__(self):
        super(BarcaGreedy, self).__init__()
        self.__cami_exit = None

    @staticmethod
    def __heuristica(estat: Estat) -> int:
        """ Quants animals queden a l'esquerra.

        Cada viatge en pot moure com a molt dos, així que aquesta suma és una
        estimació optimista (mai sobreestima) del que falta.
        """
        return estat.quica_esq + estat.llops_esq

    def __cerca(self, estat_inicial: Estat):
        """ Greedy: la frontera s'ordena només per h(n). """
        frontera = PriorityQueue()
        tancats = set()
        ordre = count()  # desempat: evita comparar objectes Estat

        frontera.put((self.__heuristica(estat_inicial), next(ordre), estat_inicial))

        while not frontera.empty():
            _, _, estat_actual = frontera.get()

            if estat_actual in tancats or not estat_actual.es_segur():
                continue

            if estat_actual.es_meta():
                return estat_actual.cami

            for fill in estat_actual.genera_fill():
                frontera.put((self.__heuristica(fill), next(ordre), fill))

            tancats.add(estat_actual)

        return None

    def actua(self, percepcio: dict) -> tuple[str, (int, int)]:
        if self.__cami_exit is None:
            estat_inicial = Estat(
                local_barca=percepcio["Lloc"],
                llops_esq=percepcio["Llop Esq"],
                polls_esq=percepcio["Poll Esq"],
            )
            self.__cami_exit = self.__cerca(estat_inicial) or []

        if self.__cami_exit:
            quiques, llops = self.__cami_exit.pop(0)
            return "M", (quiques, llops)

        return "A", None
