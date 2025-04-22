import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Dummy Training Data (Replace with real data)
data = pd.DataFrame({
    "volatility": [0.12, 0.05, 0.18, 0.09, 0.15, 0.22, 0.07, 0.03, 0.25, 0.1],
    "return": [0.08, 0.02, 0.12, 0.03, 0.07, 0.15, 0.01, 0.02, 0.18, 0.04],
    "risk_label": [1, 0, 1, 0, 1, 1, 0, 0, 1, 0]  # 1: High risk, 0: Low risk
})

X = data[["volatility", "return"]]
y = data["risk_label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save Model
joblib.dump(model, "app/ml/risk_model.pkl")

# Print Accuracy
predictions = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, predictions))
