# np-jasna-zekovic

Napredno programiranje - domaći zadaci

## Domaći 1

Instalirala sam Python 3.12 i VS Code. Za provjeru koda koristim ruff, a za testove pytest.

Funkcija prosjecna_cijena je u src/cijene.py, testovi su u tests/test_cijene.py.

Prvo `pip install -r requirements-dev.txt`, pa se testovi pokreću sa `pytest`, a ruff sa `ruff check .`

**Upit:** Napiši Python funkciju prosjecna_cijena koja vraća prosječnu cijenu iz liste. Dodaj test.

**Nedostaci:** AI je napisao samo sum(cijene) / len(cijene). To pukne kad je lista prazna.
Takođe je prihvatao negativne cijene, a True je računao kao 1. Test koji je dao provjeravao je samo
jedan običan primjer. Dodala sam provjere za to i još testova.
