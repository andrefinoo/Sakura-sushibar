#!/usr/bin/env python3
"""
Test base per sushi_allergie.py
Verifica le funzionalitÃ  standard: esistenza delle funzioni, filtraggio corretto,
caso con allergene assente e struttura dell'output di menu_a_rischio.
"""

import pytest

try:
    from sushi_allergie import piatti_con_allergene, menu_a_rischio
except ImportError:
    piatti_con_allergene = None
    menu_a_rischio = None


# ---------------------------------------------------------------------------
# Dati di test (indipendenti dal file JSON, per test isolati e veloci)
# ---------------------------------------------------------------------------

PIATTI = [
    {
        "id": "P01",
        "nome": "Salmone Nigiri",
        "categoria": "nigiri",
        "ingredienti": ["riso da sushi", "salmone", "wasabi"],
        "allergeni": ["pesce", "sesamo"],
    },
    {
        "id": "P03",
        "nome": "Gambero Nigiri",
        "categoria": "nigiri",
        "ingredienti": ["riso da sushi", "gambero cotto", "wasabi"],
        "allergeni": ["crostacei", "sesamo"],
    },
    {
        "id": "P06",
        "nome": "Kappa Maki",
        "categoria": "maki",
        "ingredienti": ["riso da sushi", "cetriolo", "alga nori"],
        "allergeni": ["sesamo"],
    },
    {
        "id": "P07",
        "nome": "Edamame",
        "categoria": "antipasto",
        "ingredienti": ["edamame", "sale marino"],
        "allergeni": ["soia"],
    },
    {
        "id": "P14",
        "nome": "Sashimi di Salmone",
        "categoria": "sashimi",
        "ingredienti": ["salmone fresco"],
        "allergeni": ["pesce"],
    },
]

MENU = [
    {
        "id": "M01",
        "nome": "Menu Sakura",
        "prezzo": 25.90,
        "composizione": ["P01", "P06", "P07"],
    },
    {
        "id": "M04",
        "nome": "Menu Vegano",
        "prezzo": 19.90,
        "composizione": ["P06", "P07"],
    },
    {
        "id": "M03",
        "nome": "Menu Mare",
        "prezzo": 32.00,
        "composizione": ["P01", "P03", "P14"],
    },
]

PIATTI_PER_ID = {p["id"]: p for p in PIATTI}


# ---------------------------------------------------------------------------
# Test struttura
# ---------------------------------------------------------------------------


def test_structure_check():
    """Verifica che le funzioni richieste esistano con i nomi corretti."""
    assert piatti_con_allergene is not None, (
        "ERRORE CRITICO: funzione 'piatti_con_allergene' non trovata in 'sushi_allergie.py'. "
        "Controlla che il file si chiami esattamente 'sushi_allergie.py' e che la funzione "
        "sia definita con questo nome esatto."
    )
    assert menu_a_rischio is not None, (
        "ERRORE CRITICO: funzione 'menu_a_rischio' non trovata in 'sushi_allergie.py'. "
        "Controlla che il file si chiami esattamente 'sushi_allergie.py' e che la funzione "
        "sia definita con questo nome esatto."
    )


# ---------------------------------------------------------------------------
# Test piatti_con_allergene
# ---------------------------------------------------------------------------


def test_piatti_con_allergene_pesce():
    """Filtrare per 'pesce' deve restituire esattamente i piatti con quell'allergene."""
    risultato = piatti_con_allergene(PIATTI, "pesce")
    nomi = [p["nome"] for p in risultato]
    assert "Salmone Nigiri" in nomi, "Salmone Nigiri contiene pesce e deve apparire nel risultato"
    assert "Sashimi di Salmone" in nomi, "Sashimi di Salmone contiene pesce e deve apparire nel risultato"
    assert "Gambero Nigiri" not in nomi, "Gambero Nigiri contiene crostacei, non pesce"
    assert "Kappa Maki" not in nomi, "Kappa Maki non contiene pesce"
    assert "Edamame" not in nomi, "Edamame non contiene pesce"


def test_piatti_con_allergene_assente():
    """Un allergene non presente nel menu deve restituire una lista vuota."""
    risultato = piatti_con_allergene(PIATTI, "arachidi")
    assert risultato == [], (
        f"Con allergene 'arachidi' (non presente) ci si aspetta [], "
        f"ricevuto {risultato}"
    )


def test_piatti_con_allergene_restituisce_lista():
    """piatti_con_allergene deve sempre restituire una lista (mai None)."""
    risultato = piatti_con_allergene(PIATTI, "sesamo")
    assert isinstance(risultato, list), (
        f"piatti_con_allergene deve restituire una list, ricevuto {type(risultato)}"
    )


# ---------------------------------------------------------------------------
# Test menu_a_rischio
# ---------------------------------------------------------------------------


def test_menu_a_rischio_pesce():
    """Menu che contengono piatti con 'pesce' devono apparire nel risultato."""
    risultato = menu_a_rischio(MENU, PIATTI_PER_ID, "pesce")
    nomi_menu = [r[0]["nome"] for r in risultato]
    assert "Menu Sakura" in nomi_menu, (
        "Menu Sakura contiene Salmone Nigiri (pesce) e deve essere segnalato"
    )
    assert "Menu Mare" in nomi_menu, (
        "Menu Mare contiene Salmone Nigiri e Sashimi di Salmone (pesce) e deve essere segnalato"
    )


def test_menu_vegano_sicuro_da_pesce():
    """Il Menu Vegano non ha piatti con 'pesce' e non deve apparire nel risultato."""
    risultato = menu_a_rischio(MENU, PIATTI_PER_ID, "pesce")
    nomi_menu = [r[0]["nome"] for r in risultato]
    assert "Menu Vegano" not in nomi_menu, (
        "Menu Vegano non contiene pesce â€” non deve essere segnalato"
    )


def test_menu_a_rischio_struttura_output():
    """
    menu_a_rischio deve restituire una lista di tuple (menu_dict, lista_piatti_problematici).
    Il secondo elemento deve essere una lista non vuota di piatti.
    """
    risultato = menu_a_rischio(MENU, PIATTI_PER_ID, "pesce")
    assert len(risultato) > 0, "Con allergene 'pesce' ci si aspetta almeno un menu a rischio"
    primo = risultato[0]
    assert isinstance(primo, (tuple, list)), (
        f"Ogni elemento del risultato deve essere una tupla o lista (menu, piatti), "
        f"ricevuto {type(primo)}"
    )
    menu_dict, piatti_problematici = primo
    assert isinstance(menu_dict, dict), "Il primo elemento della coppia deve essere il dict del menu"
    assert isinstance(piatti_problematici, list), "Il secondo elemento deve essere la lista dei piatti problematici"
    assert len(piatti_problematici) > 0, "La lista dei piatti problematici non deve essere vuota"