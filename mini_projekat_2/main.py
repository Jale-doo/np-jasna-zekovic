"""Demonstracija: tri modela na skupu iris.

Pokretanje:  python main.py
"""

from eksperimenti.eksperiment import IrisEksperiment
from eksperimenti.modeli import MODELI
from eksperimenti.posmatraci import KonzolniPosmatrac

METRIKE = ["tacnost", "f1", "preciznost"]


def main() -> None:
    posmatrac = KonzolniPosmatrac()
    svi_rezultati = {}
    for naziv in MODELI:  # linearni, stablo, knn
        eksperiment = IrisEksperiment(naziv, METRIKE, [posmatrac])
        svi_rezultati[naziv] = eksperiment.pokreni()
        print()

    print(f"{'model':<10}" + "".join(f"{m:>12}" for m in METRIKE))
    for naziv, rez in svi_rezultati.items():
        print(f"{naziv:<10}" + "".join(f"{rez[m]:>12.3f}" for m in METRIKE))


if __name__ == "__main__":
    main()
