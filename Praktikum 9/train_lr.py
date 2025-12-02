import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib

# 1. Load Dataset
data = pd.read_csv("heart_clean.csv")
print("Data Loaded. Shape:", data.shape)

X = data.drop("target", axis=1)
y = data["target"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 2. Definisikan fitur numerik & kategorikal
numeric_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']

categorical_features = [
    'sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'
]

# 3. Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ],
    remainder='drop'
)

# 4. Pipeline (preprocessor → model)
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000, random_state=42))
])

# 5. Train model
print("Melatih Pipeline...")
pipeline.fit(X_train, y_train)

# 6. Evaluasi dan simpan model
pred = pipeline.predict(X_test)

print("\n--- Hasil Evaluasi Pipeline ---")
print(f"Accuracy: {accuracy_score(y_test, pred):.4f}")

joblib.dump(pipeline, "heart_disease_pipeline.joblib")
print("\nPipeline berhasil disimpan sebagai 'heart_disease_pipeline.joblib'")
