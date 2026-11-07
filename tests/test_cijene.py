import math

import pytest

from src.cijene import prosjecna_cijena


def test_prosjek_cijelih_brojeva() -> None:
    assert prosjecna_cijena([80, 120, 100]) == 100.0


def test_prosjek_decimalnih_zaokruzen_na_dvije_decimale() -> None:
    assert prosjecna_cijena([10.0, 10.0, 10.01]) == 10.0
    assert prosjecna_cijena([19.99, 5.01]) == 12.5


def test_jedna_cijena() -> None:
    assert prosjecna_cijena([75.5]) == 75.5


def test_radi_i_sa_generatorom_i_tuple() -> None:
    assert prosjecna_cijena(c for c in [50, 150]) == 100.0
    assert prosjecna_cijena((50, 150)) == 100.0


def test_prazna_lista_baca_valueerror() -> None:
    with pytest.raises(ValueError, match="prazna"):
        prosjecna_cijena([])


@pytest.mark.parametrize("losa", [-1, -0.01])
def test_negativna_cijena_baca_valueerror(losa: float) -> None:
    with pytest.raises(ValueError, match="negativna"):
        prosjecna_cijena([100, losa])


@pytest.mark.parametrize("losa", [math.nan, math.inf])
def test_nan_i_beskonacno_bacaju_valueerror(losa: float) -> None:
    with pytest.raises(ValueError, match="konačan"):
        prosjecna_cijena([100, losa])


@pytest.mark.parametrize("losa", ["80", None, True])
def test_element_koji_nije_broj_baca_typeerror(losa: object) -> None:
    with pytest.raises(TypeError):
        prosjecna_cijena([100, losa])  # type: ignore[list-item]
