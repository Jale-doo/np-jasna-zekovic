"""Ulazna tačka programa ("composition root").

Ovo je JEDINO mjesto gdje se biraju konkretne klase. Ako sutra podaci
stižu iz baze, mijenja se samo ovaj fajl – servis ostaje isti.

Pokretanje:  python main.py [putanja_do_csv]
"""

import sys

from rezervacije.izvjestaji import FajlIzvjestac, KonzolniIzvjestac
from rezervacije.izvori import CsvIzvor
from rezervacije.servis import ObradaRezervacija


def main() -> None:
    putanja = sys.argv[1] if len(sys.argv) > 1 else "podaci/rezervacije.csv"
    servis = ObradaRezervacija(
        izvor=CsvIzvor(putanja),
        izvjestaci=[FajlIzvjestac("izvjestaj.txt"), KonzolniIzvjestac()],
    )
    servis.obradi()


if __name__ == "__main__":
    main()
