"""Testovi domenskog modela – ne trebaju ni izvor ni izvještač."""

import pytest
from rezervacije.model import Rezervacija


def test_iznos_je_noci_puta_cijena() -> None:
    assert Rezervacija("Ana", 3, 80.0).iznos == 240.0


@pytest.mark.parametrize(
    ("gost", "noci", "cijena"),
    [("Ana", 0, 80.0), ("Ana", -1, 80.0), ("Ana", 2, -5.0), ("  ", 2, 80.0)],
)
def test_neispravna_rezervacija_baca_gresku(gost: str, noci: int, cijena: float) -> None:
    with pytest.raises(ValueError):
        Rezervacija(gost, noci, cijena)
