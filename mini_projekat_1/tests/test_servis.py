"""Testovi servisa sa zamjenskim izvorom podataka (zahtjev zadatka)."""

import pytest
from rezervacije.model import Rezervacija
from rezervacije.servis import ObradaRezervacija

from tests.conftest import MemorijskiIzvor, SnimajuciIzvjestac


def test_obradi_racuna_iznose_i_ukupno(tri_rezervacije: list[Rezervacija]) -> None:
    servis = ObradaRezervacija(MemorijskiIzvor(tri_rezervacije))

    izvjestaj = servis.obradi()

    assert izvjestaj.iznosi == (240.0, 241.0, 325.0)
    assert izvjestaj.ukupno == pytest.approx(806.0)
    assert izvjestaj.broj_rezervacija == 3


def test_obradi_prazan_izvor_daje_nulu() -> None:
    servis = ObradaRezervacija(MemorijskiIzvor([]))

    izvjestaj = servis.obradi()

    assert izvjestaj.iznosi == ()
    assert izvjestaj.ukupno == 0


def test_svaki_izvjestac_dobija_isti_izvjestaj(tri_rezervacije: list[Rezervacija]) -> None:
    prvi, drugi = SnimajuciIzvjestac(), SnimajuciIzvjestac()
    servis = ObradaRezervacija(MemorijskiIzvor(tri_rezervacije), [prvi, drugi])

    rezultat = servis.obradi()

    assert prvi.primljeni == [rezultat]
    assert drugi.primljeni == [rezultat]


def test_izvor_se_cita_tacno_jednom(tri_rezervacije: list[Rezervacija]) -> None:
    izvor = MemorijskiIzvor(tri_rezervacije)
    servis = ObradaRezervacija(izvor, [SnimajuciIzvjestac()])

    servis.obradi()

    assert izvor.broj_poziva == 1
