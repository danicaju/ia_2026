""" Fitxer que conté l'agent barca en profunditat.

S'ha d'implementar el mètode:
    actua()
"""
from quiques.agent import Barca
from quiques.estat import Estat


class BarcaProfunditat(Barca):
    def __init__(self):
        super(BarcaProfunditat, self).__init__()
        self.__cami_exit = None

    def __cerca(self, estat_inicial: Estat):
        """ DFS amb pila: l'últim estat que entra és el primer que surt. """
        frontera = [estat_inicial]
        tancats = set()

        while frontera:
            estat_actual = frontera.pop()

            if estat_actual in tancats or not estat_actual.es_segur():
                continue

            if estat_actual.es_meta():
                return estat_actual.cami

            # reversed: per explorar els fills d'esquerra a dreta
            for fill in reversed(estat_actual.genera_fill()):
                frontera.append(fill)

            tancats.add(estat_actual)

        return None

    def actua(self, percepcio: dict) -> str | tuple[str, (int, int)]:
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
