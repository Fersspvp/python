import os
import random

# ------ EINSTELLUNGEN ------
jahrgaenge = range(5, 12)     # Jahrgang 5–11
klassen = ["A", "B", "C", "D"]
anzahl_pro_klasse = 10

vornamen = [
    "Max", "Lena", "Ben", "Emma", "Luis", "Mia", "Paul", "Lea",
    "Jonas", "Marie", "Finn", "Anna", "Leon", "Lina", "Noah", "Sarah"
]

nachnamen = [
    "Müller", "Schmidt", "Bauer", "Becker", "Wagner", "Hofmann",
    "Klein", "Wolf", "Schwarz", "Neumann", "Krüger", "Schuster"
]

faecher = ["Mathe", "Deutsch", "Englisch", "Sachkunde"]

# ------ FUNKTIONEN ------

def generate_name():
    return random.choice(vornamen), random.choice(nachnamen)

def generate_noten():
    return {fach: random.randint(1, 4) for fach in faecher}

def generate_fehlzeiten():
    return random.randint(0, 5), random.randint(0, 2)  # entschuldigt, unentschuldigt

# ------ HAUPT-GENERATION ------

for jahrgang in jahrgaenge:
    
    # Ordner fürs LISTEN-System
    jahrgang_liste_ordner = f"SCHUELERDATEN_PROJEKT_NEU/JAHRGANG_{jahrgang}"
    os.makedirs(jahrgang_liste_ordner, exist_ok=True)

    # Datei für Jahrgangsliste
    jahrgangsliste_path = os.path.join(jahrgang_liste_ordner, "schueller_des_jahrgangs.txt")
    jahrgangsliste_inhalt = f"Jahrgang {jahrgang} – Schülerliste\n\n"

    # Ordner fürs EINZEL-SuS-System
    jahrgang_sus_ordner = f"Schuelerdaten_Projekt_Neu/Jahrgang_{jahrgang}"
    os.makedirs(jahrgang_sus_ordner, exist_ok=True)

    for klasse in klassen:
        klasse_ordner = f"{jahrgang_sus_ordner}/Klasse_{klasse}"
        os.makedirs(klasse_ordner, exist_ok=True)

        jahrgangsliste_inhalt += f"Klasse {klasse}:\n"

        for _ in range(anzahl_pro_klasse):
            vorname, nachname = generate_name()
            name = f"{vorname} {nachname}"
            dateiname = name.upper().replace(" ", "_") + ".txt"

            noten = generate_noten()
            entschuldigt, unentschuldigt = generate_fehlzeiten()

            # Schülerdatei schreiben
            pfad = os.path.join(klasse_ordner, dateiname)
            with open(pfad, "w", encoding="utf-8") as f:
                f.write(f"# Name\n{name}\n\n")
                f.write(f"# Jahrgang\n{jahrgang}\n\n")
                f.write(f"# Klasse\n{klasse}\n\n")
                f.write(f"# Adresse\n(Beispieladresse automatisch generiert)\n\n")
                f.write("# Noten\n")
                for fach, note in noten.items():
                    f.write(f"{fach}: {note}\n")
                f.write("\n# Fehlzeiten\n")
                f.write(f"Entschuldigt: {entschuldigt}\n")
                f.write(f"Unentschuldigt: {unentschuldigt}\n")

            jahrgangsliste_inhalt += f"- {name}\n"

        jahrgangsliste_inhalt += "\n"

    # Jahrgangsliste speichern
    with open(jahrgangsliste_path, "w", encoding="utf-8") as f:
        f.write(jahrgangsliste_inhalt)

print("Schülersystem wurde vollständig generiert!")
