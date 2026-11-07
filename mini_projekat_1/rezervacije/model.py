"""Domenski model: šta je rezervacija i kako se računa njen iznos.

Odgovornost (S): samo podaci o rezervaciji i pravila koja važe za nju.
Ovaj modul ne zna ništa o fajlovima, CSV-u, ekranu ili mailu.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rezervacija:
    gost: str
    noci: int
    cijena_noci: float

    def __post_init__(self) -> None:
        # Validacija na jednom mjestu: neispravna rezervacija ne može ni nastati.
        if not self.gost.strip():
            raise ValueError("Ime gosta ne smije biti prazno")
        if self.noci <= 0:
            raise ValueError("Broj noćenja mora biti pozitivan")
        if self.cijena_noci < 0:
            raise ValueError("Cijena noćenja ne smije biti negativna")

    @property
    def iznos(self) -> float:
        return self.noci * self.cijena_noci
