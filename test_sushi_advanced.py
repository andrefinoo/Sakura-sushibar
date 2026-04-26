#!/usr/bin/env python3
"""
Test avanzati per sushi_allergie.py
Verifica edge cases: case insensitivity, menu con un solo piatto rischioso,
piatto senza allergeni, assenza di duplicati, caricamento JSON reale.
"""

import json
import pytest
from pathlib import Path

try:
    from sushi_allergie import carica_menu, piatti_con_allergene, menu_a_rischio
except ImportError:
    carica_menu = None
    piatti_con_allergene = None
    menu_a_rischio = None


# ---------------------------------------------------------------------------
# Dati di test inline
# ---------------------------------------------------------------------------

PIATTI_EDGE = [
    {
        "id": "X01",
        "nome": "Piatto Sicuro",
        "categoria": "test",
        "ingredienti": ["acqua"],
        "allergeni": [],
    },
    {
        "id": "X02",
        "nome": "Piatto con Pesce",
        "categoria": "test",
        "ingredienti": ["salmone"],
        "allergeni": ["pesce"],
    },
    {
        "id": "X03",
        "nome": "Piatto Multi-Allergenico",
        "categoria": "test",
        "ingredienti": ["gambero", "farina", "uovo"],
        "allergeni": ["crostacei", "glutine", "uova"],
    },
]

PIATTI_EDGE_PER_ID = {p["id"]: p for p in PIATTI_EDGE}

MENU_EDGE = [
    {
        "id": "MX1",
        "nome": "Menu con Un Solo Piatto Rischioso",
        "prezzo": 10.00,
        "composizione": ["X01", "X02"],  # X01 Ã¨ sicuro, X02 ha pesce
    },
    {
        "id": "MX2",
        "nome": "Menu Totalmente Sicuro",
        "prezzo": 8.00,
        "composizione": ["X01"],  # solo piatto senza allergeni
    },
]


# ---------------------------------------------------------------------------
# Test struttura
# ---------------------------------------------------------------------------


def test_structure_check():
    """Verifica che tutte e tre le funzioni richieste esistano."""
    assert carica_menu is not None, (
        "ERRORE CRITICO: funzione 'carica_menu' non trovata in 'sushi_allergie.py'."
    )
    assert piatti_con_allergene is not None, (
        "ERRORE CRITICO: funzione 'piatti_con_allergene' non trovata in 'sushi_allergie.py'."
    )
    assert menu_a_rischio is not None, (
        "ERRORE CRITICO: funzione 'menu_a_rischio' non trovata in 'sushi_allergie.py'."
    )


# ---------------------------------------------------------------------------
# Test case insensitivity
# ---------------------------------------------------------------------------


def test_case_insensitive_maiuscolo():
    """'PESCE' deve trovare gli stessi piatti di 'pesce'."""
    lower = piatti_con_allergene(PIATTI_EDGE, "pesce")
    upper = piatti_con_allergene(PIATTI_EDGE, "PESCE")
    nomi_lower = sorted(p["nome"] for p in lower)
    nomi_upper = sorted(p["nome"] for p in upper)
    assert nomi_lower == nomi_upper, (
        f"Il confronto deve essere case-insensitive: "
        f"'pesce' â†’ {nomi_lower}, 'PESCE' â†’ {nomi_upper}"
    )


def test_case_insensitive_misto():
    """'Pesce' (prima lettera maiuscola) deve trovare gli stessi risultati di 'pesce'."""
    lower = piatti_con_allergene(PIATTI_EDGE, "pesce")
    mixed = piatti_con_allergene(PIATTI_EDGE, "Pesce")
    nomi_lower = sorted(p["nome"] for p in lower)
    nomi_mixed = sorted(p["nome"] for p in mixed)
    assert nomi_lower == nomi_mixed, (
        f"Il confronto deve essere case-insensitive: "
        f"'pesce' â†’ {nomi_lower}, 'Pesce' â†’ {nomi_mixed}"
    )


# ---------------------------------------------------------------------------
# Test piatto senza allergeni
# ---------------------------------------------------------------------------


def test_piatto_senza_allergeni_non_incluso():
    """Un piatto con lista allergeni vuota non deve mai apparire nei risultati."""
    risultato = piatti_con_allergene(PIATTI_EDGE, "sesamo")
    nomi = [p["nome"] for p in risultato]
    assert "Piatto Sicuro" not in nomi, (
        "Piatto Sicuro ha lista allergeni vuota â€” non deve mai apparire nel risultato"
    )


# ---------------------------------------------------------------------------
# Test menu con un solo piatto rischioso
# ---------------------------------------------------------------------------


def test_menu_con_un_solo_piatto_rischioso():
    """
    Un menu deve essere segnalato anche se contiene UN SOLO piatto con l'allergene.
    Il cliente non puÃ² ordinare il menu perchÃ© contiene quel piatto.
    """
    risultato = menu_a_rischio(MENU_EDGE, PIATTI_EDGE_PER_ID, "pesce")
    nomi_menu = [r[0]["nome"] for r in risultato]
    assert "Menu con Un Solo Piatto Rischioso" in nomi_menu, (
        "Menu con Un Solo Piatto Rischioso contiene X02 (pesce) â€” "
        "deve essere segnalato anche se ha un solo piatto problematico su due"
    )


def test_menu_totalmente_sicuro_non_incluso():
    """Un menu composto solo da piatti senza l'allergene non deve essere segnalato."""
    risultato = menu_a_rischio(MENU_EDGE, PIATTI_EDGE_PER_ID, "pesce")
    nomi_menu = [r[0]["nome"] for r in risultato]
    assert "Menu Totalmente Sicuro" not in nomi_menu, (
        "Menu Totalmente Sicuro non contiene pesce â€” non deve comparire nel risultato"
    )


def test_piatti_problematici_corretti():
    """
    I piatti problematici restituiti per un menu devono essere solo quelli
    con l'allergene â€” non tutti i piatti del menu.
    """
    risultato = menu_a_rischio(MENU_EDGE, PIATTI_EDGE_PER_ID, "pesce")
    # Cerca il menu con un solo piatto rischioso
    match = [r for r in risultato if r[0]["id"] == "MX1"]
    assert len(match) == 1
    _, piatti_problematici = match[0]
    nomi_problematici = [p["nome"] for p in piatti_problematici]
    assert "Piatto con Pesce" in nomi_problematici, (
        "X02 (Piatto con Pesce) deve essere nella lista dei piatti problematici"
    )
    assert "Piatto Sicuro" not in nomi_problematici, (
        "X01 (Piatto Sicuro) non ha allergeni â€” non deve apparire tra i piatti problematici"
    )


# ---------------------------------------------------------------------------
# Test carica_menu con il file JSON reale
# ---------------------------------------------------------------------------


def test_carica_menu_file_reale():
    """carica_menu deve caricare menu_sakura.json senza errori e restituire un dict."""
    json_path = Path(__file__).parent / "menu_sakura.json"
    assert json_path.exists(), (
        f"File menu_sakura.json non trovato in {json_path.parent}. "
        "Assicurati che il file sia nella stessa cartella di sushi_allergie.py"
    )
    dati = carica_menu(str(json_path))
    assert isinstance(dati, dict), f"carica_menu deve restituire un dict, ricevuto {type(dati)}"
    assert "piatti" in dati, "Il dizionario deve avere la chiave 'piatti'"
    assert "menu_tipici" in dati, "Il dizionario deve avere la chiave 'menu_tipici'"
    assert len(dati["piatti"]) > 0, "La lista 'piatti' non deve essere vuota"
    assert len(dati["menu_tipici"]) > 0, "La lista 'menu_tipici' non deve essere vuota"


def test_menu_vegano_sicuro_da_pesce_sul_file_reale():
    """
    Sul file reale, il Menu Vegano non deve comparire cercando 'pesce',
    ma deve comparire cercando 'soia' (contiene edamame e zuppa di miso).
    """
    json_path = Path(__file__).parent / "menu_sakura.json"
    if not json_path.exists():
        pytest.skip("menu_sakura.json non trovato â€” test saltato")

    dati = carica_menu(str(json_path))
    piatti_per_id = {p["id"]: p for p in dati["piatti"]}

    # Menu Vegano non compare per "pesce"
    ris_pesce = menu_a_rischio(dati["menu_tipici"], piatti_per_id, "pesce")
    nomi_pesce = [r[0]["nome"] for r in ris_pesce]
    assert "Menu Vegano" not in nomi_pesce, (
        "Menu Vegano non ha pesce â€” non deve comparire cercando 'pesce'"
    )

    # Menu Vegano compare per "soia" (edamame e zuppa di miso)
    ris_soia = menu_a_rischio(dati["menu_tipici"], piatti_per_id, "soia")
    nomi_soia = [r[0]["nome"] for r in ris_soia]
    assert "Menu Vegano" in nomi_soia, (
        "Menu Vegano contiene Edamame e Zuppa di Miso (soia) â€” "
        "deve comparire cercando 'soia'. "
        "Attenzione: 'vegano' non equivale a 'privo di tutti gli allergeni'."
    )