import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

class TitanicNN:
    def __init__(self, csv_path):
        # Daten einlesen und splitten
        df = pd.read_csv(csv_path)
        train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)
        
        # Missing Values für 'Age' durch Median ersetzen
        median_age = train_df["Age"].median(skipna=True)
        train_df["Age"] = train_df["Age"].fillna(median_age)
        val_df["Age"]   = val_df["Age"].fillna(median_age)
        
        # Features auswählen und Dummy-Kodierung (drop_first=True)
        features = ["Pclass", "Sex", "Age", "Cabin", "Embarked"]
        self.X_train = pd.get_dummies(train_df[features], drop_first=True)
        self.X_val   = pd.get_dummies(val_df  [features], drop_first=True)
        # Spalten angleichen
        self.X_val = self.X_val.reindex(columns=self.X_train.columns, fill_value=0)
        
        self.y_train = train_df["Survived"]
        self.y_val   = val_df["Survived"]
        
        self.model = None
        self.history = None

    def build_model(self):
        # Zwei Hidden Layers und Output-Layer
        input_dim = self.X_train.shape[1]
        model = Sequential([
            Dense(16, activation='relu', input_dim=input_dim),
            Dense(8, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(
            loss=tf.keras.losses.BinaryCrossentropy(),
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
            metrics=['accuracy']
        )
        self.model = model

    def train(self, epochs, batch_size=32):
        # Training mit Validierungsdaten
        self.history = self.model.fit(
            self.X_train, self.y_train,
            validation_data=(self.X_val, self.y_val),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )

    def plot_loss(self):
        # Loss-Kurve zeichnen
        plt.figure()
        plt.plot(self.history.history['loss'],     label='Trainingsverlust')
        plt.plot(self.history.history['val_loss'], label='Validierungsverlust')
        plt.xlabel('Epoche')
        plt.ylabel('Verlust (binäre Kreuzentropie)')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    nn = TitanicNN('ki-main/titanic/data/train.csv')
    nn.build_model()
    nn.train(epochs=100)

    # --- neu: Accuracy auf dem Validierungsset ausgeben ---
    loss_val, acc_val = nn.model.evaluate(nn.X_val, nn.y_val)
    print(f"Finale Validierungs-Accuracy: {acc_val:.4f}")

    nn.plot_loss()

