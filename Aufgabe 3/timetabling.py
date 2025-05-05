from constraint import Problem, AllDifferentConstraint

problem = Problem()

lehrer = ["Maier", "Müller", "Schmid", "Huber"]
fächer = ["Deutsch", "Englisch", "Mathematik", "Physik"]
räume = [1, 2, 3, 4]

# Jeder Lehrer bekommt genau ein Fach – alle unterschiedlich
for name in lehrer:
    problem.addVariable(f"{name}_Fach", fächer)
problem.addConstraint(AllDifferentConstraint(), [f"{name}_Fach" for name in lehrer])

# Jeder Lehrer bekommt genau einen Raum – alle unterschiedlich
for name in lehrer:
    problem.addVariable(f"{name}_Raum", räume)
problem.addConstraint(AllDifferentConstraint(), [f"{name}_Raum" for name in lehrer])

# 1. Herr Maier prüft nie in Raum 4.
problem.addConstraint(lambda raum: raum != 4,["Maier_Raum"])

# 2. Herr Müller prüft immer Deutsch.
problem.addConstraint(lambda fach: fach == "Deutsch", ["Müller_Fach"])

# 3. Herr Schmid und Herr Müller prüfen nicht in benachbarten Räumen.
problem.addConstraint(lambda schmid_raum, müller_raum: abs(schmid_raum - müller_raum) > 1, ["Schmid_Raum", "Müller_Raum"])

# 4. Frau Huber prüft Mathematik.
problem.addConstraint(lambda fach: fach == "Mathematik", ["Huber_Fach"])

# 5. Physik wird immer in Raum 4 geprüft.
for name in lehrer:
    problem.addConstraint(lambda fach, raum: fach != "Physik" or raum == 4, [f"{name}_Fach", f"{name}_Raum"])

# 6. Deutsch und Englisch werden nicht in Raum 1 geprüft.
for name in lehrer:
    problem.addConstraint(lambda fach, raum: fach not in ["Deutsch", "Englisch"] or raum != 1, [f"{name}_Fach", f"{name}_Raum"])


lösungen = problem.getSolutions()

for lösung in lösungen:
    print("----- Lösung -----")
    for name in lehrer:
        fach = lösung[f"{name}_Fach"]
        raum = lösung[f"{name}_Raum"]
        print(f"{name} prüft {fach} in Raum {raum}")