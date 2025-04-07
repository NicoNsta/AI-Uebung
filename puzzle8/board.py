
# board.py
# ------------------------------------------
# Author: Michael Blaich
# Datum: 21.03.2025
# Beschreibung: Implementierung der Board-Klasse für das 8-Puzzle-Problem.
# ------------------------------------------
import random


class Board:
    """
    Repräsentiert ein 8-Puzzle-Board.

    Methoden:
    - parity(): Prüft, ob das Puzzle lösbar ist.
    - h1(), h2(): Platzhalter für Heuristikfunktionen.
    - possible_actions(): Liefert gültige Nachfolgezustände.
    - is_solved(): Prüft, ob das Ziel erreicht ist.
    """

    N = 8  # Problemgröße

    def __init__(self, board=None):
        """
        Initialisiert das Board.
        Wenn kein Board übergeben wird, wird ein zufälliges, lösbares Board
        erzeugt.
        """
        if board:
            self.board = list(board)
        else:
            self.board = list(range(1, Board.N + 2))
            while True:
                random.shuffle(self.board)
                if self.parity():
                    break

    def __str__(self):
        """
        Gibt das Board als String aus.
        """
        return f"Puzzle{{board={self.board}}}"

    def __eq__(self, other):
        """
        Zwei Boards sind gleich, wenn ihr Zustand gleich ist.
        """
        return isinstance(other, Board) and self.board == other.board

    def __hash__(self):
        """
        Ermöglicht das Nutzen von Board in Sets oder als Dictionary-Keys.
        """
        return hash(tuple(self.board))


    def parity(self):
        """
        Paritätsprüfung:
        Gibt True zurück, wenn das Board lösbar ist.
        TODO: Implementiere die Berechnung der Parität
        """
        # Erstelle eine Liste ohne das leere Feld (0)
        tiles = [tile for tile in self.board if tile != 0] 

        # Zähle die Anzahl der falschen Paare
        count = 0 
        for y in range(len(tiles)):
            for x in range(y):
                if tiles[x] > tiles[y]: 
                    count += 1 

        # Rückgabe: True bei gerader Parität, False bei ungerader
        return count % 2 == 0 


    def h1(self):
        """
        Heuristikfunktion h1 (siehe Aufgabenstellung).
        TODO: Implementiere einfache Heuristik
        """
        count = 0
        for i, tile in enumerate(self.board):
            if tile == 0:
                continue # Ohne 0
            if tile != i:
                count += 1
        return count


    def h2(self):
        """
        Heuristikfunktion h2 (siehe Aufgabenstellung).
        TODO: Implementiere verbesserte Heuristik
        """

        dist = 0
        for i, tile in enumerate(self.board):
            if tile == 0:
                continue
            goal_index = tile  # weil tile soll auf Index tile stehen
            x1, y1 = i % 3, i // 3 # i % 3 gibt die Spalte, i // 3 die Zeile
            x2, y2 = goal_index % 3, goal_index // 3 # Zielposition
            dist += abs(x1 - x2) + abs(y1 - y2) # Manhattan-Distanz --> Anzahl der Schritte
        return dist


    def possible_actions(self):
        """
        Gibt eine Liste aller möglichen Folge-Boards zurück,
        die durch einen gültigen Zug entstehen.
        TODO: Diese Methode muss noch implementiert werden.
        """
        # Finde die Position des leeren Feldes (0)
        zero = self.board.index(0)
        x, y = zero % 3, zero // 3
        # Mögliche Bewegungsrichtungen (rechts, unten, links, oben)
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        result = []
        # Erzeuge neue Boards für jede mögliche Bewegung
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Überprüfe, ob die neue Position im Board liegt
            if 0 <= nx < 3 and 0 <= ny < 3:
                # Berechne den Index der neuen Position (2D in 1D)
                n_index = ny * 3 + nx
                # Erstelle eine Kopie des aktuellen Boards
                new_board = self.board.copy()
                # Tausche die Positionen des leeren Feldes und der Zielposition
                new_board[zero], new_board[n_index] = new_board[n_index], new_board[zero]
                # Füge das neue Board zur Ergebnisliste hinzu
                result.append(Board(new_board))
        return result

    def is_solved(self):
        """
        Prüft, ob das Board im Zielzustand ist (0,1,2,3,...,8).
        TODO: Implementiere die Prüfung ob das Board gelöst ist.
        """
        return self.board == list(range(9))


def main():
    b = Board([7, 2, 4, 5, 0, 6, 8, 3, 1])  # Startzustand manuell setzen
    # b = Board()  # Lösbares Puzzle zufällig generieren
    print("Startzustand:", b)

    print("Parität:,", b.parity())

    print("Heuristik h1: ", b.h1())
    print("Heuristik h2: ", b.h2())

    for child in b.possible_actions():
        print(child)

    print("Ist gelöst:", b.is_solved())


if __name__ == "__main__":
    main()
