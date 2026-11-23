"""DECORATOR: mjerenje vremena bez izmjene funkcije koja se mjeri.

@mjeri_vrijeme obavija funkciju: zapamti vrijeme, pozove originalnu
funkciju, ispiše koliko je trajala i vrati njen rezultat nepromijenjen.
"""

import time
from collections.abc import Callable
from functools import wraps


# [**P, R] znači: omotač prima iste argumente (P) i vraća isti tip (R) kao fn
def mjeri_vrijeme[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)  # čuva ime i docstring originalne funkcije
    def omotac(*args: P.args, **kwargs: P.kwargs) -> R:
        pocetak = time.perf_counter()
        rezultat = fn(*args, **kwargs)
        trajanje = time.perf_counter() - pocetak
        print(f"{fn.__name__} je trajalo {trajanje * 1000:.1f} ms")
        return rezultat

    return omotac
