import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# 1) Daten einlesen
train_data = pd.read_csv('ki-main/titanic/data/train.csv')
test_data = pd.read_csv('ki-main/titanic/data/test.csv') # b)

# 2) Split 80/20
train_df, val_df = train_test_split(train_data, test_size=0.2, random_state=42)

# 3) Überlebensraten per Pclass
surv_rates = train_df.groupby("Pclass")["Survived"].mean()

# 4) Regel definieren: Überleben wenn Rate > 0.5
rule = (surv_rates > 0.5).astype(int)

# 5) Regel anwenden
preds = val_df["Pclass"].map(rule)
pred_survived = test_data["Pclass"].map(rule) # b)

# 6) Crosstabs nur zur Kontrolle
print("Counts je Pclass × Survived:")
print(pd.crosstab(train_df["Pclass"], train_df["Survived"]))
print("\nÜberlebensraten je Pclass (normalisiert):")
print(pd.crosstab(train_df["Pclass"], train_df["Survived"], normalize="index"))

# 7) Genauigkeit
accuracy = accuracy_score(val_df["Survived"], preds)
print(f"\nGenauigkeit auf Validierungsset: {accuracy:.4f}")


# b) Submission-DataFrame erzeugen und als CSV speichern
output = pd.DataFrame({
    'PassengerId': test_data.PassengerId,
    'Survived':    pred_survived
})
output.to_csv('ki-main/titanic/output/b)-submission.csv', index=False)
print("Your submission was successfully saved!")