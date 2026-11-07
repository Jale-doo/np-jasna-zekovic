"""Zamjenski (lažni) objekti za testove.

MemorijskiIzvor i SnimajuciIzvjestac NE nasljeđuju Protocol – dovoljno je
da imaju iste metode (strukturno tipiziranje, "duck typing").
Zato servis može da ih koristi umjesto pravog CSV fajla i pravog izvještaja.
"""

import pytest
from rezervacije.izvjestaji import Izvjestaj
from rezervacije.model import Rezervacija


class MemorijskiIzvor:
    """Lažni izvor: vraća unaprijed zadate rezervacije, bez diska."""

    def __init__(self, rezervacije: list[Rezervacija]) -> None:
        self.rezervacije = rezervacije
        self.broj_poziva = 0

    def ucitaj(self) -> list[Rezervacija]:
        self.broj_poziva += 1
        return list(self.rezervacije)


class SnimajuciIzvjestac:
    """Lažni izvještač: samo pamti šta je dobio, da test može da provjeri."""

    def __init__(self) -> None:
        self.primljeni: list[Izvjestaj] = []

    def objavi(self, izvjestaj: Izvjestaj) -> None:
        self.primljeni.append(izvjestaj)


@pytest.fixture
def tri_rezervacije() -> list[Rezervacija]:
    return [
        Rezervacija("Ana", 3, 80.0),  # 240.0
        Rezervacija("Marko", 2, 120.5),  # 241.0
        Rezervacija("Jelena", 5, 65.0),  # 325.0
    ]
