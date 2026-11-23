"""OBSERVER: praćenje eksperimenta kroz događaje.

Eksperiment ne zna ko ga prati. Samo javlja događaje ("pocetak",
"kraj_treninga", "rezultati") svima koji su se pretplatili.
Novi način praćenja (fajl, Slack, grafik) je nova klasa sa metodom
obavijesti(), bez izmjene eksperimenta.
"""

from typing import Any, Protocol


class Posmatrac(Protocol):
    def obavijesti(self, dogadjaj: str, podaci: dict[str, Any]) -> None: ...


class KonzolniPosmatrac:
    """Ispisuje svaki događaj na ekran."""

    def obavijesti(self, dogadjaj: str, podaci: dict[str, Any]) -> None:
        if dogadjaj == "rezultati":
            tekst = ", ".join(f"{k}={v:.3f}" for k, v in podaci["rezultati"].items())
            print(f"[{podaci['model']}] rezultati: {tekst}")
        else:
            print(f"[{podaci['model']}] {dogadjaj}")


class DnevnikPosmatrac:
    """Pamti sve događaje u listu (korisno za kasniju analizu i za testove)."""

    def __init__(self) -> None:
        self.dogadjaji: list[tuple[str, dict[str, Any]]] = []

    def obavijesti(self, dogadjaj: str, podaci: dict[str, Any]) -> None:
        self.dogadjaji.append((dogadjaj, podaci))

    @property
    def nazivi(self) -> list[str]:
        return [d for d, _ in self.dogadjaji]
