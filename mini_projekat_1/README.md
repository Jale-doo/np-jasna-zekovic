# Mini projekat 1 - refaktoring obrade rezervacija

Polazni kod je klasa `UpravljanjeRezervacijama` sa slajda 17 (nalazi se u `original/obrada.py`).
Ta klasa je radila sve: čitala fajl, računala iznos, snimala izvještaj i "slala mail".
Zbog toga nije mogla da se testira bez pravog fajla, a svaka izmjena je dirala istu klasu.

## Kako sam podijelila kod

- `rezervacije/model.py` - `Rezervacija` (gost, noći, cijena) i računanje iznosa
- `rezervacije/izvori.py` - `IzvorRezervacija` (Protocol) i `CsvIzvor` koji čita CSV
- `rezervacije/izvjestaji.py` - `Izvjestac` (Protocol), `FajlIzvjestac` i `KonzolniIzvjestac`
- `rezervacije/servis.py` - `ObradaRezervacija`, samo povezuje korake: učitaj, izračunaj, objavi
- `main.py` - ovdje se biraju konkretne klase (CSV fajl, izvještaj u fajl i na ekran)

**S:** svaka klasa ima jedan posao. Ako se promijeni format CSV-a, mijenja se samo `CsvIzvor`.

**D:** servis ne pravi sam izvor i izvještač nego ih dobija kroz konstruktor, i zna samo za
Protocol, ne za CSV. Zato u testovima mogu da mu dam lažni izvor iz memorije.

## Pokretanje

```
cd mini_projekat_1
pip install -r requirements.txt
python main.py
pytest
```

## Testovi

U `tests/conftest.py` su `MemorijskiIzvor` (vraća rezervacije iz liste, bez fajla) i
`SnimajuciIzvjestac` (samo pamti šta je dobio). Sa njima su napravljeni testovi servisa u
`tests/test_servis.py`: obračun iznosa, prazna lista, da svaki izvještač dobije rezultat i da se
izvor čita jednom. Ostali testovi provjeravaju model, čitanje CSV-a i izvještače.

## Rad sa AI

**Upiti:**
1. Šta je monolitni skript (uz prezentaciju iz 2. nedjelje i tekst zadatka)
2. Da refaktoriše kod sa slajda 17 po principima S i D, sa Protocol-om za izvor i izvještaj, i da napiše testove
3. Upit sa slajda 16 (pregled koda po SOLID principima)

**Šta sam ispravila ili provjerila:**
- AI je u `Izvjestaj` stavio `list` iako je klasa `frozen`, pa se lista i dalje mogla mijenjati. Promijenila sam u `tuple`.
- Originalni kod puca na CSV fajlu sa zaglavljem (`int("noci")`). Dodala sam preskakanje zaglavlja i praznih redova.
- Dodala sam validaciju da broj noći i cijena ne mogu biti negativni.
- Nisam prihvatila dodatne klase koje AI predlaže (posebna klasa za obračun, fabrika za izvore), jer ovdje nisu potrebne.
- Provjerila sam da nova verzija daje iste iznose kao original (240, 241, 325).
