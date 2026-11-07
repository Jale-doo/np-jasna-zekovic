"""Testovi konkretnih implementacija (CSV izvor, fajl izvještač).

tmp_path je ugrađeni pytest fixture: privremeni folder koji se briše
nakon testa, pa testovi ne prljaju projekat.
"""

from pathlib import Path

import pytest
from rezervacije.izvjestaji import FajlIzvjestac, Izvjestaj, KonzolniIzvjestac
from rezervacije.izvori import CsvIzvor


def test_csv_izvor_preskace_zaglavlje_i_prazne_redove(tmp_path: Path) -> None:
    fajl = tmp_path / "r.csv"
    fajl.write_text("gost,noci,cijena_noci\nAna,3,80\n\nMarko, 2 , 120.5\n", encoding="utf-8")

    rezervacije = CsvIzvor(fajl).ucitaj()

    assert [r.gost for r in rezervacije] == ["Ana", "Marko"]
    assert rezervacije[1].noci == 2


def test_csv_izvor_prijavljuje_los_red(tmp_path: Path) -> None:
    fajl = tmp_path / "r.csv"
    fajl.write_text("gost,noci,cijena_noci\nAna,3\n", encoding="utf-8")

    with pytest.raises(ValueError, match="3 kolone"):
        CsvIzvor(fajl).ucitaj()


def test_fajl_izvjestac_upisuje_stavke_i_ukupno(tmp_path: Path) -> None:
    fajl = tmp_path / "izvjestaj.txt"

    FajlIzvjestac(fajl).objavi(Izvjestaj((240.0, 241.0)))

    assert fajl.read_text(encoding="utf-8") == "1. 240.00\n2. 241.00\nUkupno: 481.00\n"


def test_konzolni_izvjestac_ispisuje_sazetak(capsys: pytest.CaptureFixture[str]) -> None:
    KonzolniIzvjestac().objavi(Izvjestaj((240.0, 241.0)))

    assert "2 rezervacija, ukupno 481.00" in capsys.readouterr().out
