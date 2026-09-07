
import os
from collections import deque

import matplotlib.pyplot as plt


# -----------------------------
# 1. Definition der Grunddaten
# -----------------------------
# Hier werden alle Knoten und Zielpunkte mit ihren x/y-Koordinaten gespeichert.
# Diese Koordinaten werden später für die grafische Darstellung des Pfads verwendet.

startpunkt = (675, 400)

knotenpunkte = {
    "knoten_1": (680, 318),  # Flur nach Eingang
    "knoten_2": (556, 314),  # Aufenthalt
    "knoten_3": (488, 354),  # vor dem Speisesaal
    "knoten_4": (327, 349),  # vor den Aufzügen
    "knoten_nord": (624, 185),
}

checkpoints = {
    "ost_1": (769, 330),
    "ost_2": (880, 340),
    "nord_1": (511, 185),
    "nord_2": (777, 176),
    "nord_west_1": (163, 82),
    "west_1": (165, 349),
    "west_2": (96, 348),
    "sued_west": (255, 485),
}

# Verbindungsliste: jeder Eintrag beschreibt einen Abschnitt zwischen zwei Punkten.
# Diese Abschnitte bilden die Kanten des Graphen.
# Example: "verbindung9": ["knoten_3", "knoten_4"] bedeutet, dass es einen
# begehbaren Weg von knoten_3 nach knoten_4 gibt.
verbindungen = {
    "verbindung1": ["startpunkt", "knoten_1"],
    "verbindung2": ["knoten_1", "ost_1"],
    "verbindung3": ["ost_1", "ost_2"],
    "verbindung4": ["knoten_1", "knoten_2"],
    "verbindung5": ["knoten_2", "knoten_nord"],
    "verbindung6": ["knoten_nord", "nord_1"],
    "verbindung7": ["knoten_nord", "nord_2"],
    "verbindung8": ["knoten_2", "knoten_3"],
    "verbindung9": ["knoten_3", "knoten_4"],
    "verbindung10": ["knoten_4", "nord_west_1"],
    "verbindung11": ["knoten_4", "west_1"],
    "verbindung12": ["knoten_4", "sued_west"],
    "verbindung13": ["west_1", "west_2"],
}


# ------------------------------------------------
# 2. Graph-Aufbau: Erstelle eine Adjazenzliste
# ------------------------------------------------
def build_graph(verbindungen):
    """Erzeuge aus den Verbindungsabschnitten einen Graphen."""
    graph = {}

    # Jede Verbindung ist eine Liste mit zwei Elementen: [startpunkt, endpunkt].
    for verbindung in verbindungen.values():
        punkt_a = verbindung[0]  # erster Endpunkt des Abschnitts
        punkt_b = verbindung[1]  # zweiter Endpunkt des Abschnitts

        # Stelle sicher, dass beide Punkte als Knoten im Graphen existieren.
        if punkt_a not in graph:
            graph[punkt_a] = []
        if punkt_b not in graph:
            graph[punkt_b] = []

        # Füge die Verbindung in beide Richtungen hinzu.
        # Der Graph ist ungerichtet: von punkt_a kann man zu punkt_b und umgekehrt.
        graph[punkt_a].append(punkt_b)
        #graph[punkt_b].append(punkt_a)

    return graph


# ------------------------------------------------
# 3. Pfadfindung: Breitensuche (BFS)
# ------------------------------------------------
def find_path(graph, start, goal):
    """Finde einen Pfad vom Startpunkt zum Ziel im Graphen."""
    visited = set()  # bereits besuchte Knoten

    # Die Queue enthält Tupel (aktueller Knoten, bisheriger Pfad).
    queue = deque([(start, [start])])
    visited.add(start)

    while queue:
        current, path = queue.popleft()

        # Wenn der aktuelle Knoten das Ziel ist, haben wir einen Weg gefunden.
        if current == goal:
            return path

        # Untersuche alle Nachbarn des aktuellen Knotens.
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)

                # Erzeuge den neuen Pfad für den Nachbarn anhand des aktuellen Pfads.
                queue.append((neighbor, path + [neighbor]))

    # Wenn die Queue leer ist und kein Ziel gefunden wurde, gibt es keinen Pfad.
    return None


# ------------------------------------------------
# 4. Karte laden
# ------------------------------------------------
def load_map():
    """Lade das Bild des Grundrisses aus dem aktuellen Verzeichnis."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "Grundriss_mit_Knotenpunkten.png")
    return plt.imread(image_path)


# ------------------------------------------------
# 5. Pfad zeichnen
# ------------------------------------------------
def draw_path(karte, weg, punkt_koordinaten):
    """Zeichne den gefundenen Weg auf die Karte."""
    if not weg or len(weg) < 2:
        return

    coords = []
    for punkt in weg:
        # Nur Punkte berücksichtigen, die auch Koordinaten haben.
        if punkt in punkt_koordinaten:
            coords.append(punkt_koordinaten[punkt])

    if len(coords) < 2:
        return

    xs = [x for x, _ in coords]
    ys = [y for _, y in coords]

    plt.figure(figsize=(10, 8))
    plt.imshow(karte)
    plt.plot(xs, ys, color="red", linewidth=2.5)
    plt.scatter(xs, ys, color="red", zorder=3)
    plt.axis("off")
    plt.show()


# ------------------------------------------------
# 6. Hauptprogramm
# ------------------------------------------------
def main():
    # Zeige den aktuellen Arbeitsordner und seine Dateien an.
    print("Aktueller Ordner:")
    print(os.getcwd())

    print("\nDateien in diesem Ordner:")
    print(os.listdir())

    # Lade den Hintergrundplan als Bild.
    karte = load_map()

    # Frage den Benutzer nach dem Zielpunkt.
    nutzer_eingabe = input(
        "Geben Sie bitte den Zielpunkt ein (ost_1, ost_2, nord_1, nord_2, nord_west_1, west_1, west_2, sued_west):__ "
    ).strip()
    print(nutzer_eingabe)

    # Baue den Graphen aus den Verbindungseinträgen.
    graph = build_graph(verbindungen)
    ziel = nutzer_eingabe

    # Suche den Pfad vom Startpunkt zum Ziel.
    weg = find_path(graph, "startpunkt", ziel)

    # Kombiniere die Koordinaten aller bekannten Punkte in ein Dictionary.
    punkt_koordinaten = {**knotenpunkte, **checkpoints, "startpunkt": startpunkt}

    print(f"Pfad: {weg}")

    if weg is None:
        print("Kein Pfad gefunden.")
        return

    # Zeichne den Pfad auf die geladene Karte.
    draw_path(karte, weg, punkt_koordinaten)


if __name__ == "__main__":
    main()

