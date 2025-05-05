from constraint import Problem, AllDifferentConstraint

problem = Problem()

bundesländer = [
    "Schleswig-Holstein", "Hamburg", "Mecklenburg-Vorpommern", "Niedersachsen",
    "Bremen", "Brandenburg", "Berlin", "Sachsen-Anhalt", "Sachsen", "Thüringen",
    "Hessen", "NRW", "Rheinland-Pfalz", "Saarland", "Baden-Württemberg", "Bayern"
]

farben = ["rot", "grün", "blau"]  # Später evtl. 4 testen

problem.addVariables(bundesländer, farben)
