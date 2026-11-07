"""Servis koji povezuje korake obrade.

Servis NE kreira sam izvor ni izvještače – dobija ih kroz konstruktor
(injekcija zavisnosti). Zato u testu možemo dati lažni izvor iz memorije.
"""

from collections.abc import Sequence

from rezervacije.izvjestaji import Izvjestac, Izvjestaj
from rezervacije.izvori import IzvorRezervacija


class ObradaRezervacija:
    def __init__(self, izvor: IzvorRezervacija, izvjestaci: Sequence[Izvjestac] = ()) -> None:
        self.izvor = izvor
        self.izvjestaci = list(izvjestaci)

    def obradi(self) -> Izvjestaj:
        rezervacije = self.izvor.ucitaj()
        izvjestaj = Izvjestaj(iznosi=tuple(r.iznos for r in rezervacije))
        for izvjestac in self.izvjestaci:
            izvjestac.objavi(izvjestaj)
        return izvjestaj
