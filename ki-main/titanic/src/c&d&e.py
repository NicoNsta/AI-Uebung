import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1) Daten einlesen
train_data = pd.read_csv('ki-main/titanic/data/train.csv')

# 2) 80/20 Split
train_df, val_df = train_test_split(train_data, test_size=0.2, random_state=42)

# 3) Age-Imputation
median_age = train_df["Age"].median(skipna=True)
train_df["Age"] = train_df["Age"].fillna(median_age)
val_df  ["Age"] = val_df["Age"].fillna(median_age)

# 4) One-Hot für Pclass + Sex + Age (Age bleibt numerisch)
features  = ["Pclass", "Sex", "Age"]
train_enc = pd.get_dummies(train_df[features], drop_first=True)
val_enc   = pd.get_dummies(val_df  [features], drop_first=True)
val_enc   = val_enc.reindex(columns=train_enc.columns, fill_value=0)

X_train, y_train = train_enc, train_df["Survived"]
X_val,   y_val   = val_enc,   val_df  ["Survived"]

# ——————————————————————————————
# Logistische Regression
lr = LogisticRegression(solver='lbfgs', max_iter=1000)
lr.fit(X_train, y_train)
pred_lr = lr.predict(X_val)
acc_lr  = accuracy_score(y_val, pred_lr)
print(f"Accuracy der logistischen Regression: {acc_lr:.4f}")

# ——————————————————————————————
# Random Forest
rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_val)
acc_rf  = accuracy_score(y_val, pred_rf)
print(f"Accuracy des Random Forest    : {acc_rf:.4f}")
