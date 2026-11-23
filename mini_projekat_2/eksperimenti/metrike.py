"""STRATEGY: zamjenjive metrike iza istog potpisa.

Svaka metrika je funkcija (y_tacno, y_predvidjeno) -> float.
Pošto u Pythonu funkcija može da se čuva u rječniku, rječnik METRIKE
bira strategiju po nazivu umjesto lanca if/elif.
"""

from collections.abc import Callable, Sequence
from typing import Any

from sklearn.metrics import accuracy_score, f1_score, precision_score

Metrika = Callable[[Sequence[Any], Sequence[Any]], float]


def tacnost(y: Sequence[Any], p: Sequence[Any]) -> float:
    """Udio tačno pogođenih primjera."""
    return float(accuracy_score(y, p))


def f1(y: Sequence[Any], p: Sequence[Any]) -> float:
    """F1 mjera, prosjek po klasama (macro), jer iris ima 3 klase."""
    return float(f1_score(y, p, average="macro"))


def preciznost(y: Sequence[Any], p: Sequence[Any]) -> float:
    return float(precision_score(y, p, average="macro", zero_division=0))


METRIKE: dict[str, Metrika] = {"tacnost": tacnost, "f1": f1, "preciznost": preciznost}


def evaluiraj(naziv: str, y: Sequence[Any], p: Sequence[Any]) -> float:
    if naziv not in METRIKE:
        raise ValueError(f"Nepoznata metrika: {naziv!r}. Dostupne: {', '.join(METRIKE)}")
    return METRIKE[naziv](y, p)
