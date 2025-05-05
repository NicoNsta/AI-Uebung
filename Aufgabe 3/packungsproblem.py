from constraint import Problem

# CSP-Klasse: definiert Variablen & Constraints für das Packungsproblem
class PackungSolver:
    def __init__(self, board_width, board_height, rectangles):
        """
        :param board_width: Breite des großen Feldes
        :param board_height: Höhe des großen Feldes
        :param rectangles: Liste von (ID, Breite, Höhe)
        """
        self.W = board_width
        self.H = board_height
        self.rects = rectangles
        self.prob = Problem()

    def setup(self):
        # 1) Variablen anlegen: für jedes Rechteck x, y, rot
        for rid, rw, rh in self.rects:
            self.prob.addVariable(f"{rid}_x", range(self.W))
            self.prob.addVariable(f"{rid}_y", range(self.H))
            self.prob.addVariable(f"{rid}_rot", [0, 1])  # 0=normal,1=gedreht

        # 2) Constraint: jedes Rechteck muss ins Feld passen
        for rid, rw, rh in self.rects:
            def fits(x, y, rot, rw=rw, rh=rh):
                w, h = (rw, rh) if rot == 0 else (rh, rw)
                return x + w <= self.W and y + h <= self.H
            self.prob.addConstraint(
                fits, (f"{rid}_x", f"{rid}_y", f"{rid}_rot")
            )

        # 3) Constraint: keine Überlappungen zwischen je zwei Rechtecken
        n = len(self.rects)
        for i in range(n):
            id_i, wi, hi = self.rects[i]
            for j in range(i+1, n):
                id_j, wj, hj = self.rects[j]

                def no_overlap(xi, yi, ri, xj, yj, rj,
                               wi=wi, hi=hi, wj=wj, hj=hj):
                    # tatsächliche Breite/Höhe je nach Rotation
                    w_i, h_i = (wi, hi) if ri == 0 else (hi, wi)
                    w_j, h_j = (wj, hj) if rj == 0 else (hj, wj)
                    # A ganz links, rechts, oberhalb oder unterhalb von B?
                    return (
                        xi + w_i <= xj or  # A links von B
                        xj + w_j <= xi or  # A rechts von B
                        yi + h_i <= yj or  # A oberhalb von B
                        yj + h_j <= yi     # A unterhalb von B
                    )

                self.prob.addConstraint(
                    no_overlap,
                    (
                        f"{id_i}_x", f"{id_i}_y", f"{id_i}_rot",
                        f"{id_j}_x", f"{id_j}_y", f"{id_j}_rot"
                    )
                )

    def solve(self):
        """Gibt eine Position+Rotation für alle Rechtecke oder None zurück."""
        return self.prob.getSolution()


# Imperative Klasse: baut das Board auf und füllt es mit CSP-Ergebnis
class PackungBoard:
    def __init__(self, width, height):
        self.W = width
        self.H = height
        self.board = [[0] * self.W for _ in range(self.H)]

    def place(self, rid, x, y, rw, rh, rot):
        """Platziert ein Rechteck mit ID rid, Größe rw×rh an (x,y), rotiert wenn nötig."""
        if rot == 1:
            rw, rh = rh, rw
        # Annahme: CSP garantiert gültige Plätze
        for yy in range(y, y + rh):
            for xx in range(x, x + rw):
                self.board[yy][xx] = rid

    def display(self):
        """Gibt die Board-Matrix auf der Konsole aus."""
        for row in self.board:
            print(" ".join(str(cell) for cell in row))


if __name__ == "__main__":
    # Definition der sechs Rechtecke: (ID, Breite, Höhe)
    rects = [
        (1, 6, 4),
        (2, 8, 1),
        (3, 4, 1),
        (4, 5, 2),
        (5, 2, 2),
        (6, 3, 2),
    ]

    # 1) CSP einrichten und lösen
    solver = PackungSolver(board_width=7, board_height=8, rectangles=rects)
    solver.setup()
    solution = solver.solve()

    # 2) Ergebnis mit Imperativmodell visualisieren
    board = PackungBoard(width=7, height=8)
    if solution:
        for rid, rw, rh in rects:
            x = solution[f"{rid}_x"]
            y = solution[f"{rid}_y"]
            rot = solution[f"{rid}_rot"]
            board.place(rid, x, y, rw, rh, rot)
        print("Gefülltes Feld:")
    else:
        print("Keine Lösung gefunden.")

    board.display()
