import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam
from TitanicNN import TitanicNN  # ggf. Pfad anpassen

# 1) Hyperparameter-Kombinationen und Einstellungen
combos = [
    (1e-3, 32),
    (1e-4, 32),
    (1e-3, 64),
    (1e-4, 64),
]
repeats = 10
epochs = 50

# 2) Ergebnisse speichern
results = {}

for lr, bs in combos:
    train_runs = []       # Liste der Trainings-Loss-Kurven
    val_runs   = []       # Liste der Validierungs-Loss-Kurven
    min_val    = []       # Minimale val_loss je Lauf
    final_val  = []       # Finaler val_loss je Lauf

    for _ in range(repeats):
        # a) Instanz und Modell aufsetzen
        nn = TitanicNN('ki-main/titanic/data/train.csv')
        nn.build_model()
        nn.model.compile(
            loss='binary_crossentropy',
            optimizer=Adam(learning_rate=lr),
            metrics=['accuracy']
        )
        # b) Training
        nn.train(epochs=epochs, batch_size=bs)
        h = nn.history.history

        # c) Kurven und Kennzahlen sammeln
        train_runs.append(h['loss'])
        val_runs.append(h['val_loss'])
        min_val.append(min(h['val_loss']))
        final_val.append(h['val_loss'][-1])

    # d) Statistik berechnen
    train_arr = np.array(train_runs)
    val_arr   = np.array(val_runs)
    stats = {
        'mean_train':    train_arr.mean(axis=0),
        'mean_val':      val_arr.mean(axis=0),
        'min_val_mean':  np.mean(min_val),
        'min_val_std':   np.std(min_val),
        'final_val_mean':np.mean(final_val),
        'final_val_std': np.std(final_val),
        'min_val_list':  min_val,
        'final_val_list':final_val,
        'all_train':     train_runs,
        'all_val':       val_runs
    }
    results[(lr, bs)] = stats

# 3) Übersichtlicher Kombi-Plot (nur Mittelwerte + Marker fürs beste val_loss)
plt.figure(figsize=(10,6))
for (lr, bs), s in results.items():
    mt, mv = s['mean_train'], s['mean_val']
    label = f"lr={lr}, bs={bs}"
    plt.plot(mt, label=f"Train {label}")
    plt.plot(mv, '--', label=f"Val   {label}")
    # Marker an der Epoche minimaler mittlerer val_loss
    best_epoch = np.argmin(mv) + 1
    plt.scatter(best_epoch, mv[best_epoch-1], marker='o')
plt.title("Mittelwerte aller Loss-Kurven")
plt.xlabel("Epoche")
plt.ylabel("Binary Crossentropy Loss")
plt.legend()
plt.grid(True)

# 4) Vier Einzelplots mit Shading + Overlay aller Runs
for i, ((lr, bs), s) in enumerate(results.items(), 1):
    mt, mv = s['mean_train'], s['mean_val']
    tr, vr = s['all_train'], s['all_val']
    plt.figure(figsize=(6,4))
    # Hintergrund: alle Einzel-Läufe
    for run in vr:
        plt.plot(run, color='grey', alpha=0.3, linewidth=1)
    # Shading Min/Max
    val_arr = np.array(vr)
    min_curve = val_arr.min(axis=0)
    max_curve = val_arr.max(axis=0)
    plt.fill_between(range(1, epochs+1), min_curve, max_curve, alpha=0.2)
    # Mittelwert-Linie
    plt.plot(mv, color='red', linewidth=2, label='Mean Val Loss')
    plt.plot(mt, color='blue', linewidth=2, label='Mean Train Loss')
    plt.title(f"lr={lr}, bs={bs}")
    plt.xlabel("Epoche")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)

# 5) Boxplots der minimalen und finalen Validation-Loss-Verteilungen
df_box = pd.DataFrame({
    f"{lr}_{bs}_min":  s['min_val_list']
    for (lr, bs), s in results.items()
})
df_box2 = pd.DataFrame({
    f"{lr}_{bs}_final": s['final_val_list']
    for (lr, bs), s in results.items()
})
plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
df_box.boxplot()
plt.title("Min. val_loss je Combo")
plt.ylabel("val_loss")
plt.xticks(rotation=45)
plt.subplot(1,2,2)
df_box2.boxplot()
plt.title("Finale val_loss je Combo")
plt.xticks(rotation=45)
plt.tight_layout()

# 6) Statistische Zusammenfassungstabelle ausgeben
summary = pd.DataFrame([
    {
        "lr": lr, "bs": bs,
        "MinLoss_mean":   s['min_val_mean'],
        "MinLoss_std":    s['min_val_std'],
        "FinalLoss_mean": s['final_val_mean'],
        "FinalLoss_std":  s['final_val_std'],
    }
    for (lr, bs), s in results.items()
])
print("\nStatistische Zusammenfassung:")
print(summary.to_string(index=False))

plt.show()
