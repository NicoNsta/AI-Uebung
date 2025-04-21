# idfs.py
# ------------------------------------------
# Author: Michael Blaich
# Datum: 21.03.2025
# Beschreibung: Implementierung der Iterativen Tiefensuche für
# das 8-Puzzle-Problem.
# ------------------------------------------
from board import Board
from collections import deque


def dfs(cur_board, path, limit, visited):
    """
    TODO: Implementiere die Rekursive Tiefensuche mit Limitierung.
    """
    # Wenn das aktuelle Board das Ziel erreicht hat, gebe den Pfad zurück.
    if cur_board.is_solved():
        return path

    # Wenn das Limit erreicht ist, gebe None zurück.
    if limit == 0:
        return None 

    visited.add(cur_board)

    # Iteriere über alle möglichen Nachfolgezustände.
    for neighbor in cur_board.possible_actions():
        # Wenn das Folge-Board schon besucht wurde, überspringe es (Zyklen vermeiden).
        if neighbor in visited:
            continue
        path.append(neighbor)
        # Rekursiver Aufruf mit reduziertem Limit.
        result = dfs(neighbor, path, limit - 1, visited)
        # Wenn eine Lösung gefunden wurde, gebe den Pfad zurück.
        if result is not None:
            return result
        # Rückgängig machen: Board aus dem Pfad entfernen
        path.pop()
    # Aktuelles Board als besucht zurücknehmen (für andere Pfade zulassen).
    visited.remove(cur_board)
    # Keine Lösung gefunden:
    return None


def idfs(start_board: Board, limit=1000):  # max. Tiefe arbiträr gesetzt
    """
    Iterative Tiefensuche mit Schleife zur Erhöhung des Tiefenlimits.
    Gibt den Lösungspfad als deque zurück oder None, wenn keine Lösung gefunden
    wurde.
    """
    for depth in range(limit):
        path = deque([start_board])
        visited = set()
        result = dfs(start_board, path, depth, visited)
        if result:
            return result
    return None
