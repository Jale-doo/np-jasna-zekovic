"""Testovi za svaki šablon posebno + jedan test na pravom skupu iris."""

from typing import Any

import pytest
from eksperimenti.eksperiment import Eksperiment, IrisEksperiment, Podaci
from eksperimenti.metrike import evaluiraj
from eksperimenti.modeli import kreiraj_model
from eksperimenti.posmatraci import DnevnikPosmatrac
from eksperimenti.vrijeme import mjeri_vrijeme
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# --- Factory ----------------------------------------------------------------


@pytest.mark.parametrize(
    ("naziv", "klasa"),
    [
        ("linearni", LogisticRegression),
        ("stablo", DecisionTreeClassifier),
        ("knn", KNeighborsClassifier),
    ],
)
def test_fabrika_pravi_odgovarajuci_model(naziv: str, klasa: type) -> None:
    assert isinstance(kreiraj_model(naziv), klasa)


def test_fabrika_nepoznat_model_daje_jasnu_gresku() -> None:
    with pytest.raises(ValueError, match="Nepoznat model: 'svm'"):
        kreiraj_model("svm")


def test_fabrika_svaki_put_pravi_novi_objekat() -> None:
    assert kreiraj_model("knn") is not kreiraj_model("knn")


# --- Strategy ---------------------------------------------------------------


def test_metrika_tacnost_na_poznatom_primjeru() -> None:
    assert evaluiraj("tacnost", [0, 1, 1, 0], [0, 1, 0, 0]) == pytest.approx(0.75)


def test_nepoznata_metrika_daje_jasnu_gresku() -> None:
    with pytest.raises(ValueError, match="Nepoznata metrika"):
        evaluiraj("auc", [0, 1], [0, 1])


# --- Decorator --------------------------------------------------------------


def test_dekorator_cuva_rezultat_i_ime(capsys: pytest.CaptureFixture[str]) -> None:
    @mjeri_vrijeme
    def saberi(a: int, b: int) -> int:
        return a + b

    assert saberi(2, 3) == 5
    assert saberi.__name__ == "saberi"
    assert "saberi je trajalo" in capsys.readouterr().out


# --- Template Method + Observer (zamjenski eksperiment, bez sklearn-a) -------


class LazniModel:
    """Uvijek predviđa klasu 1."""

    def fit(self, X: Any, y: Any) -> "LazniModel":
        return self

    def predict(self, X: Any) -> list[int]:
        return [1] * len(X)


class LazniEksperiment(Eksperiment):
    def __init__(self, posmatraci: list[Any]) -> None:
        super().__init__("lazni", ["tacnost"], posmatraci)
        self.koraci: list[str] = []

    def ucitaj(self) -> Podaci:
        self.koraci.append("ucitaj")
        return [[0], [0]], [[0], [0], [0], [0]], [1, 1], [1, 1, 0, 0]

    def treniraj(self, X: Any, y: Any) -> LazniModel:
        self.koraci.append("treniraj")
        return LazniModel()


def test_template_method_poziva_korake_redom_i_racuna_metrike() -> None:
    eksperiment = LazniEksperiment([])

    rezultati = eksperiment.pokreni()

    assert eksperiment.koraci == ["ucitaj", "treniraj"]
    assert rezultati == {"tacnost": 0.5}  # pogađa 2 od 4


def test_posmatrac_dobija_dogadjaje_redom() -> None:
    dnevnik = DnevnikPosmatrac()

    LazniEksperiment([dnevnik]).pokreni()

    assert dnevnik.nazivi == ["pocetak", "kraj_treninga", "rezultati"]
    assert dnevnik.dogadjaji[-1][1] == {"model": "lazni", "rezultati": {"tacnost": 0.5}}


def test_vise_posmatraca_dobija_iste_dogadjaje() -> None:
    prvi, drugi = DnevnikPosmatrac(), DnevnikPosmatrac()
    eksperiment = LazniEksperiment([prvi])
    eksperiment.pretplati(drugi)

    eksperiment.pokreni()

    assert prvi.dogadjaji == drugi.dogadjaji


# --- Sve zajedno na pravom skupu iris ---------------------------------------


@pytest.mark.parametrize("naziv", ["linearni", "stablo", "knn"])
def test_iris_svaki_model_ima_dobru_tacnost(naziv: str) -> None:
    rezultati = IrisEksperiment(naziv, ["tacnost", "f1"]).pokreni()

    assert rezultati["tacnost"] > 0.85
    assert set(rezultati) == {"tacnost", "f1"}
