"""FACTORY: kreiranje modela prema nazivu.

Problem: bez fabrike bi glavni kod imao lanac
    if naziv == "knn": ... elif naziv == "stablo": ... elif ...
Rješenje: registar (rječnik naziv -> funkcija koja pravi model).
Novi model se dodaje jednom funkcijom sa @registruj_model, a
kreiraj_model() se ne mijenja (princip O).
"""

from collections.abc import Callable
from typing import Any, Protocol

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


class Model(Protocol):
    """Sve što ima fit i predict je model (svi sklearn klasifikatori)."""

    def fit(self, X: Any, y: Any) -> Any: ...
    def predict(self, X: Any) -> Any: ...


MODELI: dict[str, Callable[[], Model]] = {}


def registruj_model(naziv: str) -> Callable[[Callable[[], Model]], Callable[[], Model]]:
    """Dekorator koji upisuje funkciju-proizvođača u registar MODELI."""

    def dekorator(proizvodjac: Callable[[], Model]) -> Callable[[], Model]:
        MODELI[naziv] = proizvodjac
        return proizvodjac

    return dekorator


@registruj_model("linearni")
def _linearni() -> Model:
    # Logistička regresija je linearni model za klasifikaciju.
    model: Model = LogisticRegression(max_iter=1000)
    return model


@registruj_model("stablo")
def _stablo() -> Model:
    model: Model = DecisionTreeClassifier(random_state=42)
    return model


@registruj_model("knn")
def _knn() -> Model:
    model: Model = KNeighborsClassifier(n_neighbors=5)
    return model


def kreiraj_model(naziv: str) -> Model:
    if naziv not in MODELI:
        dostupni = ", ".join(sorted(MODELI))
        raise ValueError(f"Nepoznat model: {naziv!r}. Dostupni: {dostupni}")
    return MODELI[naziv]()
