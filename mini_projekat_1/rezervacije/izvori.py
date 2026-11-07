"""Izvori podataka: odakle dolaze rezervacije.

Protocol IzvorRezervacija je UGOVOR (apstrakcija). Servis zavisi samo od
njega, a ne od konkretnog CSV fajla – to je princip D.
Novi izvor (baza, API, JSON) dodaje se kao nova klasa, bez izmjene servisa.
"""

import csv
from pathlib import Path
from typing import Protocol

from rezervacije.model import Rezervacija


class IzvorRezervacija(Protocol):
    def ucitaj(self) -> list[Rezervacija]: ...


def red_u_rezervaciju(red: list[str]) -> Rezervacija:
    """Pretvara jedan red CSV-a ["Ana", "3", "80"] u objekat Rezervacija."""
    if len(red) != 3:
        raise ValueError(f"Očekivane 3 kolone (gost, noci, cijena), dobijeno: {red}")
    gost, noci, cijena = (polje.strip() for polje in red)
    return Rezervacija(gost=gost, noci=int(noci), cijena_noci=float(cijena))


class CsvIzvor:
    """Čita rezervacije iz CSV fajla sa zaglavljem: gost,noci,cijena_noci"""

    def __init__(self, putanja: Path | str, ima_zaglavlje: bool = True) -> None:
        self.putanja = Path(putanja)
        self.ima_zaglavlje = ima_zaglavlje

    def ucitaj(self) -> list[Rezervacija]:
        # "with" zatvara fajl i kada dođe do greške (original ga nije zatvarao).
        with self.putanja.open(encoding="utf-8", newline="") as f:
            redovi = [red for red in csv.reader(f) if red and any(p.strip() for p in red)]
        if self.ima_zaglavlje:
            redovi = redovi[1:]
        return [red_u_rezervaciju(red) for red in redovi]
