""" Solució a la decodificació d'una cadena de caràcters emprant algoritmes genètics.

Author: Miquel Miró Nicolau (UIB), 2026
"""

import random

from iaLib import agent
from tqdm import tqdm

from genetic.solucio.individu import Individu

MIDA_POBLACIO = 600
GENERACIONS = 300
RATI_MUTACIO = 0.2


class Genetic(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=1)

    def pinta(self, display):
        print(self._posicio_pintar)

    def actua(self, percepcio: dict) -> str:
        text_xifrat = percepcio["text"]

        poblacio = [Individu(aleatori=True) for _ in range(MIDA_POBLACIO)]

        for _ in tqdm(range(GENERACIONS), desc="Generacions"):
            poblacio = sorted(poblacio, key=lambda individu: individu.fitness(text_xifrat))

            elit = poblacio[: int(MIDA_POBLACIO // 3)]

            nova_poblacio = []
            while len(nova_poblacio) < MIDA_POBLACIO:
                pare1, pare2 = random.choices(elit, k=2)
                fill = pare1.reproduccio(pare2)

                if random.random() < RATI_MUTACIO:
                    fill = fill.mutacio()

                nova_poblacio.append(fill)

            poblacio = nova_poblacio

        millor = min(poblacio, key=lambda individu: individu.fitness(text_xifrat))
        return millor.desxifra(text_xifrat)
