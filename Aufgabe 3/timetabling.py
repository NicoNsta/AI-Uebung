import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


from constraint import Problem

class BundeslaenderFarbung:
    def __init__(self, laender, nachbarn):
        self.laender = laender
        self.nachbarn = nachbarn
        self.problem = Problem()

    def setup(self, farben):
        self.problem.addVariables(self.laender, farben)
        for a, b in self.nachbarn:
            self.problem.addConstraint(lambda x, y: x != y, (a, b))

    def solve(self):
        return self.problem.getSolution()




class BundeslaenderGraphMitHintergrund:
    """
    Zeichnet die 16 deutschen Bundesländer als Graph auf einer Hintergrundkarte (landkarte.jpg),
    mit neutralen Abkürzungen (keine HH/HB, sondern z. B. HA für Hamburg, BM für Bremen).
    """

    def __init__(self, hintergrundbild):
        self.hintergrundbild = hintergrundbild
        self.G = nx.Graph()
        self._add_states()
        self._add_borders()
        self._set_positions()

    def _add_states(self):
        self.bundeslaender = [
            "SH", "HA", "MV", "NI", "BM", "BB", "BE", "ST",
            "SN", "TH", "HE", "NW", "RP", "SL", "BW", "BY"
        ]
        self.G.add_nodes_from(self.bundeslaender)

    def _add_borders(self):
        self.borders = [
            ("SH", "HA"), ("SH", "NI"),
            ("HA", "NI"),
            ("MV", "BB"),
            ("NI", "BM"), ("NI", "ST"), ("NI", "HE"), ("NI", "NW"), ("NI", "TH"),
            ("BM", "NI"),
            ("BB", "BE"), ("BB", "ST"), ("BB", "SN"),
            ("ST", "SN"), ("ST", "TH"),
            ("SN", "TH"), ("SN", "BY"),
            ("TH", "HE"), ("TH", "BY"),
            ("HE", "NW"), ("HE", "RP"), ("HE", "BY"),
            ("NW", "RP"),
            ("RP", "SL"), ("RP", "BW"),
            ("BW", "BY")
        ]
        self.G.add_edges_from(self.borders)

    def _set_positions(self):
        self.pos = {
            # bereits perfekte Positionen (oben & unten)
            "SH": (0.43, 0.88),
            "HA": (0.47, 0.80), 
            "MV": (0.68, 0.84),
            "NI": (0.45, 0.68),
            "BM": (0.38, 0.75),
            "SL": (0.22, 0.29),
            "BW": (0.40, 0.20),
            "BY": (0.60, 0.25),
            "BB": (0.79, 0.62),
            "BE": (0.72, 0.68),
            "ST": (0.59, 0.60),
            "SN": (0.73, 0.49),
            "TH": (0.54, 0.47),
            "HE": (0.40, 0.45),
            "NW": (0.25, 0.55),
            "RP": (0.25, 0.37),
        }

    def draw(self, coloring):
        img = mpimg.imread(self.hintergrundbild)

        plt.figure(figsize=(10, 10))
        plt.imshow(img, extent=[0, 1, 0, 1], aspect='auto')

        node_colors = [
            coloring.get(node, "white") if coloring else "white"
            for node in self.G.nodes()
        ]

        nx.draw(
            self.G,
            pos=self.pos,
            with_labels=True,
            node_color=node_colors,
            edge_color="gray",
            node_size=1000,
            font_size=9,
            font_weight="bold"
        )

        plt.title("Bundesländer mit Nachbarschaften (auf Karte)", fontsize=14)
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    graph = BundeslaenderGraphMitHintergrund("Aufgabe 3/landkarte.jpg")

    csp = BundeslaenderFarbung(graph.bundeslaender, graph.borders)
    csp.setup(["red", "green", "blue"])
    coloring = csp.solve()

    if coloring:
        print("Lösung mit 3 Farben gefunden!")
    else:
        print("Keine Lösung mit 3 Farben. Versuche mit 4 Farben...")
        csp = BundeslaenderFarbung(graph.bundeslaender, graph.borders)
        csp.setup(["red", "green", "lightblue", "pink"])
        coloring = csp.solve()

    graph.draw(coloring)

