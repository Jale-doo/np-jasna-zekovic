"""Domaći 1: funkcija prosjecna_cijena."""

import math
from collections.abc import Iterable


def prosjecna_cijena(cijene: Iterable[float]) -> float:
    """Vraća aritmetičku sredinu cijena, zaokruženu na 2 decimale.

    >>> prosjecna_cijena([80, 120, 100])
    100.0

    Raises:
        ValueError: ako nema cijena, ako je neka cijena negativna ili nije broj.
        TypeError: ako element nije broj (npr. string "80").
    """
    lista = list(cijene)  # Iterable se može proći samo jednom (npr. generator)
    if not lista:
        raise ValueError("Lista cijena je prazna – prosjek nije definisan")

    for c in lista:
        if isinstance(c, bool) or not isinstance(c, (int, float)):
            raise TypeError(f"Cijena mora biti broj, dobijeno: {c!r}")
        if math.isnan(c) or math.isinf(c):
            raise ValueError(f"Cijena mora biti konačan broj, dobijeno: {c!r}")
        if c < 0:
            raise ValueError(f"Cijena ne smije biti negativna: {c}")

    return round(sum(lista) / len(lista), 2)
