# board.py
# ------------------------------------------
# Author: Michael Blaich
# Datum: 21.03.2025
# Beschreibung: Template für die Implementierung des A* Algorithmus
# ------------------------------------------
import heapq
from collections import deque
from board import Board
from typing import Optional


class Node:
    """
    Repräsentiert einen Knoten im Suchbaum für den A*-Algorithmus.

    Attribute:
        board (Board): Der aktuelle Zustand des Spielfelds.
        parent (Node, optional): Der Vorgängerknoten (Elternknoten) in der Pfadsuche.
        g (int): Die bisherigen Pfadkosten von Start bis zu diesem Knoten.
        h (int): Der geschätzte Abstand zum Zielzustand (Heuristik).
        f (int): Die geschätzten Gesamtkosten f = g + h.
    """

    def __init__(self, board: Board, parent: 'Node' = None, g=0):
        self.board = board
        self.parent = parent
        self.g = g  # Pfadkosten
        self.h = board.h2()  # Heuristikwert
        self.f = self.g + self.h  # f = g + h

    def __lt__(self, other):
        """
        Vergleichsmethode für die Prioritätswarteschlange.
        Knoten mit kleineren f-Werten werden bevorzugt.
        """
        return self.f < other.f  # Für PriorityQueue


def reconstruct_path(node: Node) -> deque[Board]:
    """
    Rekonstruiert den Pfad vom Startzustand bis zum Zielzustand.
    TODO: Implementiere das erstellen des Pfades.
    """
    path = deque()
    while node:
        # Füge das aktuelle Board am Anfang in die Liste (Path) ein.
        path.appendleft(node.board)
        # Gehe zum Elternknoten zurück.
        node = node.parent
    return path


def a_star(start_board: Board) -> Optional[deque[Board]]:
    """
    Führt den A*-Algorithmus zur Lösung des 8-Puzzle-Problems aus.
    TODO: Implementiere den A*-Algorithmus.
    Es empfiehlt sich hierbei heapq für die open_list und set() für die
    closed_list zu verwenden.
    """

    open_list = []
    # Prioritätswarteschlange für die offenen Knoten (open_list) --> Kleinester Wert (f = g + h) zuerst. --> Wir genutzen h2 (siehe Node-Klasse)
    heapq.heappush(open_list, Node(start_board))
    closed_list = set()

    while open_list:
        # Hole den Knoten mit dem kleinsten f-Wert aus der open_list. --> Der Knoten wird aus der Liste entfernt.
        current_node = heapq.heappop(open_list)
        current_board = current_node.board

        # Überprüfe, ob das aktuelle Board das Ziel erreicht hat.
        # Wenn ja, gebe den Pfad zurück.
        if current_board.is_solved():
            return reconstruct_path(current_node)

        # Füge den aktuellen Knoten zur closed_list hinzu.
        # closed_list ist ein Set, um doppelte Boards zu vermeiden.
        closed_list.add(current_board)

        # Iteriere über alle möglichen Nachfolgezustände (Nachbarn).
        for neighbor in current_board.possible_actions():
            # Wenn der Nachbar bereits in der closed_list ist, überspringe ihn.
            if neighbor in closed_list:
                continue

            # Berechne die neuen Pfadkosten für den Nachbarn.
            new_g = current_node.g + 1
            # Erstelle einen neuen Knoten für den Nachbarn.
            neighbor_node = Node(neighbor, parent=current_node, g=new_g)

            # Verhindert doppelte (schlechtere) Pfade in open_list
            # Wenn der Nachbar bereits in der open_list ist und die neuen Kosten (g) nicht besser sind --> überspringe ihn.
            if any(n.board == neighbor and n.f <= neighbor_node.f for n in open_list):
                continue

            heapq.heappush(open_list, neighbor_node)

    return None  # Kein Pfad gefunden
