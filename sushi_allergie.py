import json

def carica_menu(percorso: str) -> dict:
    """
    Carica il file JSON e restituisce il dizionario parsed.
    Gestisce FileNotFoundError e json.JSONDecodeError con messaggi chiari.
    """
    dati = None
    try:
        with open(percorso, "r", encoding="utf-8") as f:
            dati = json.load(f)
    except FileNotFoundError:
        print("File non trovato — verificare il percorso")
    except json.JSONDecodeError as e:
        print(f"JSON non valido: {e.msg} alla riga {e.lineno}, colonna {e.colno}")
    return dati


def piatti_con_allergene(piatti: list, allergene: str) -> list:
    """
    Restituisce la lista dei piatti (dict) che contengono l'allergene.
    Il confronto è case-insensitive: "Pesce" e "pesce" sono equivalenti.
    """
    risultato = []
    for piatto in piatti:
        if allergene.lower() in [a.lower() for a in piatto["allergeni"]]:
            risultato.append(piatto)
    return risultato


def menu_a_rischio(menu_tipici: list, piatti_per_id: dict, allergene: str) -> list:
    """
    Restituisce una lista di tuple (menu, piatti_problematici) per ogni
    menu tipico che contiene almeno un piatto con l'allergene specificato.
    """
    risultato = []
    for menu in menu_tipici:
        piatti_problematici = []
        for id_piatto in menu["composizione"]:
            piatto = piatti_per_id.get(id_piatto)
            if piatto and allergene.lower() in [a.lower() for a in piatto["allergeni"]]:
                piatti_problematici.append(piatto)
        if piatti_problematici:
            risultato.append((menu, piatti_problematici))
    return risultato

def main():
    """Carica il menu, chiede l'allergene, stampa i risultati."""
    dati = carica_menu("menu_sakura.json")
    if dati is None:
        return

    allergene = input("Inserisci un allergene: ").strip()

    piatti = dati["piatti"]
    piatti_per_id = {p["id"]: p for p in piatti}
    menu_tipici = dati["menu_tipici"]

    piatti_trovati = piatti_con_allergene(piatti, allergene)

    print("\nPIATTI DA EVITARE ")
    for p in piatti_trovati:
        allergeni_str = ", ".join(p["allergeni"])
        print(f"  • {p['nome']} ({p['categoria']}) — allergeni: {allergeni_str}")

    menu_rischio = menu_a_rischio(menu_tipici, piatti_per_id, allergene)

    print("\nMENU TIPICI DA EVITARE")
    for menu, problematici in menu_rischio:
        nomi_problematici = ", ".join(p["nome"] for p in problematici)
        print(f"  • {menu['nome']} (€{menu['prezzo']})")
        print(f"      piatti problematici: {nomi_problematici}")



if __name__ == "__main__":
    main()