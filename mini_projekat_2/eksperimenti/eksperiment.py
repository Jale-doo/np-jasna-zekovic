"""TEMPLATE METHOD: fiksan tok eksperimenta.

Osnovna klasa Eksperiment u metodi pokreni() određuje REDOSLIJED koraka:
    ucitaj -> pripremi -> treniraj -> evaluiraj
Podklasa prepisuje samo korake koji se razlikuju (ucitaj, treniraj,
po potrebi pripremi). Redoslijed se ne može pokvariti u podklasi.

Ovdje se spajaju i ostali šabloni:
- metrike se biraju po nazivu (Strategy),
- tokom rada se obavještavaju posmatrači (Observer),
- IrisEksperiment pravi model preko fabrike (Factory),
- trening se mjeri dekoratorom (Decorator).
"""

from abc import ABC, abstractmethod
from typing import Any

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from eksperimenti.metrike import evaluiraj
from eksperimenti.modeli import Model, kreiraj_model
from eksperimenti.posmatraci import Posmatrac
from eksperimenti.vrijeme import mjeri_vrijeme

Podaci = tuple[Any, Any, Any, Any]  # X_trening, X_test, y_trening, y_test


class Eksperiment(ABC):
    def __init__(self, naziv: str, metrike: list[str], posmatraci: list[Posmatrac] | None = None):
        self.naziv = naziv
        self.metrike = metrike
        self.posmatraci: list[Posmatrac] = list(posmatraci or [])

    # --- Observer ---------------------------------------------------------
    def pretplati(self, posmatrac: Posmatrac) -> None:
        self.posmatraci.append(posmatrac)

    def _objavi(self, dogadjaj: str, **podaci: Any) -> None:
        for p in self.posmatraci:
            p.obavijesti(dogadjaj, {"model": self.naziv, **podaci})

    # --- Template Method: OVO je fiksan okvir ------------------------------
    def pokreni(self) -> dict[str, float]:
        self._objavi("pocetak")
        X_tr, X_te, y_tr, y_te = self.ucitaj()
        X_tr, X_te = self.pripremi(X_tr, X_te)
        model = self.treniraj(X_tr, y_tr)
        self._objavi("kraj_treninga")
        rezultati = self.evaluiraj(model, X_te, y_te)
        self._objavi("rezultati", rezultati=rezultati)
        return rezultati

    # --- Koraci -------------------------------------------------------------
    @abstractmethod
    def ucitaj(self) -> Podaci: ...

    def pripremi(self, X_tr: Any, X_te: Any) -> tuple[Any, Any]:
        return X_tr, X_te  # podrazumijevano: bez pripreme

    @abstractmethod
    def treniraj(self, X: Any, y: Any) -> Model: ...

    def evaluiraj(self, model: Model, X: Any, y: Any) -> dict[str, float]:
        predvidjeno = model.predict(X)
        return {m: evaluiraj(m, y, predvidjeno) for m in self.metrike}


class IrisEksperiment(Eksperiment):
    """Konkretan eksperiment: skup iris, model se bira po nazivu."""

    def __init__(
        self,
        naziv_modela: str,
        metrike: list[str],
        posmatraci: list[Posmatrac] | None = None,
        test_udio: float = 0.3,
    ):
        super().__init__(naziv_modela, metrike, posmatraci)
        self.test_udio = test_udio

    def ucitaj(self) -> Podaci:
        X, y = load_iris(return_X_y=True)
        # stratify=y: u treningu i testu je isti odnos sve tri vrste cvijeta
        podjela: Podaci = tuple(
            train_test_split(X, y, test_size=self.test_udio, random_state=42, stratify=y)
        )
        return podjela

    def pripremi(self, X_tr: Any, X_te: Any) -> tuple[Any, Any]:
        # Skaliranje se "uči" samo na treningu, da test ostane neviđen.
        skaler = StandardScaler().fit(X_tr)
        return skaler.transform(X_tr), skaler.transform(X_te)

    @mjeri_vrijeme
    def treniraj(self, X: Any, y: Any) -> Model:
        model = kreiraj_model(self.naziv)
        model.fit(X, y)
        return model
