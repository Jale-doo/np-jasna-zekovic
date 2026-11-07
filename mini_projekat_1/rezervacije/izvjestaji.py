"""Izvještavanje: gdje i kako se rezultat obrade objavljuje.

Protocol Izvjestac je ugovor za svaki način izvještavanja. Snimanje u fajl
i "slanje maila" iz originala su dvije implementacije istog ugovora.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class Izvjestaj:
    """Rezultat obrade – čisti podaci, bez ikakvog formatiranja."""

    iznosi: tuple[float, ...]

    @property
    def ukupno(self) -> float:
        return sum(self.iznosi)

    @property
    def broj_rezervacija(self) -> int:
        return len(self.iznosi)


class Izvjestac(Protocol):
    def objavi(self, izvjestaj: Izvjestaj) -> None: ...


class FajlIzvjestac:
    """Upisuje izvještaj u tekstualni fajl (zamjena za sacuvaj_izvjestaj)."""

    def __init__(self, putanja: Path | str) -> None:
        self.putanja = Path(putanja)

    def objavi(self, izvjestaj: Izvjestaj) -> None:
        linije = [f"{i}. {iznos:.2f}" for i, iznos in enumerate(izvjestaj.iznosi, start=1)]
        linije.append(f"Ukupno: {izvjestaj.ukupno:.2f}")
        self.putanja.write_text("\n".join(linije) + "\n", encoding="utf-8")


class KonzolniIzvjestac:
    """Ispisuje sažetak na ekran (zamjena za posalji_mail koji je samo printao).

    Pravi mail servis bi bio nova klasa sa istom metodom objavi().
    """

    def objavi(self, izvjestaj: Izvjestaj) -> None:
        print(f"Poslato: {izvjestaj.broj_rezervacija} rezervacija, ukupno {izvjestaj.ukupno:.2f}")
