import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
import numpy as np
import joblib

# Load dataset
df = pd.read_csv("gesture_data.csv", header=None)

X = df.iloc[:, :-1].values  # all landmark coords
y = df.iloc[:, -1].values   # gesture labels

# Encode labels (convert text → numbers)
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Save encoder (needed during prediction)
joblib.dump(encoder, "label_encoder.pkl")

# Convert labels to one-hot for ANN
y_categorical = to_categorical(y_encoded)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_categorical, test_size=0.2, random_state=42
)

# ANN Model
model = Sequential([
    Dense(128, activation='relu', input_shape=(X.shape[1],)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(y_categorical.shape[1], activation='softmax')
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train model
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# Save trained model
model.save("gesture_model.h5")

print("Training complete! Model saved as gesture_model.h5")
 