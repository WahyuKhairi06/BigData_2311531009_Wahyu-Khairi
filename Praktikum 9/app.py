import streamlit as st
import pandas as pd
import joblib

# ==== Load Pipeline Model (HANYA SATU FILE) ====
try:
    pipeline = joblib.load("heart_disease_pipeline.joblib")
except FileNotFoundError:
    st.error("Error: File 'heart_disease_pipeline.joblib' tidak ditemukan. Pastikan Anda sudah menjalankan train_lr.py.")
    st.stop()

# ==== Title & Description ====
st.set_page_config(page_title="Prediksi Penyakit Jantung", layout="wide")
st.title("🔍 Prediksi Risiko Penyakit Jantung")
st.write("Masukkan data pasien untuk memprediksi risiko penyakit jantung menggunakan **Logistic Regression Pipeline**.")

# ==== 2 Kolom Input Form ====
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (tahun)", min_value=1, max_value=120, value=50)
    
    # Input kategorikal
    sex_label = st.selectbox("Sex", ["Female (0)", "Male (1)"])
    sex = 1 if "Male" in sex_label else 0 

    cp_label = st.selectbox("Chest Pain Type (cp)", [
        "typical angina (0)", "atypical angina (1)", "non-anginal pain (2)", "asymptomatic (3)"
    ])
    cp = int(cp_label.split('(')[1].split(')')[0]) # Ambil nilai numerik 0, 1, 2, atau 3

    trestbps = st.number_input("Resting Blood Pressure (trestbps) [mmHg]", min_value=50, max_value=250, value=120)
    chol = st.number_input("Cholesterol (chol) [mg/dl]", min_value=50, max_value=700, value=250)
    
    fbs_label = st.selectbox("Fasting Blood Sugar > 120mg/ml (fbs)", ["No (0)", "Yes (1)"])
    fbs = 1 if "Yes" in fbs_label else 0 

with col2:
    restecg_label = st.selectbox("Resting ECG (restecg)", [
        "Normal (0)", "ST-T wave abnormality (1)", "left ventricular hypertrophy (2)"
    ])
    restecg = int(restecg_label.split('(')[1].split(')')[0])

    thalach = st.number_input("Max Heart Rate Achieved (thalach)", min_value=50, max_value=250, value=150)

    exang_label = st.selectbox("Exercise Induced Angina (exang)", ["No (0)","Yes (1)"])
    exang = 1 if "Yes" in exang_label else 0

    oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=10.0, step=0.1, value=1.0)

    slope_label = st.selectbox("Slope of Peak Exercise (slope)", ["upsloping (0)","flat (1)","downsloping (2)"])
    slope = int(slope_label.split('(')[1].split(')')[0])

    ca = st.selectbox("Number of Major Vessels (ca)", [0,1,2,3])

    thal_label = st.selectbox("Thalassemia (thal)", ["normal (1)","fixed defect (2)","reversible defect (3)"])
    thal = int(thal_label.split('(')[1].split(')')[0])

# ==========================================================
# Siapkan Data Input MENTAH
# ==========================================================
# Data harus dikumpulkan dalam urutan yang sama dengan kolom di heart_clean.csv
input_df = pd.DataFrame([{
    "age": age,
    "sex": sex,
    "cp": cp,
    "trestbps": trestbps,
    "chol": chol,
    "fbs": fbs,
    "restecg": restecg,
    "thalach": thalach,
    "exang": exang,
    "oldpeak": oldpeak,
    "slope": slope,
    "ca": ca,
    "thal": thal
}])

# ==== Prediction ====
st.markdown("---")
if st.button("Prediksi Risiko Penyakit Jantung"):
    
    # Pipeline akan mengurus scaling dan encoding secara internal sebelum prediksi
    pred = pipeline.predict(input_df)[0]
    probability = pipeline.predict_proba(input_df)[0, 1]  # Probabilitas kelas 1 (Penyakit Jantung)

    st.subheader("📌 Hasil Prediksi")
    st.write(f"### Probabilitas Penyakit Jantung: **{probability*100:.2f}%**")

    if pred == 1:
        st.error(f"⚠ Pasien **BERISIKO TINGGI** mengidap Penyakit Jantung.")
    else:
        st.success("✔ Pasien **TIDAK BERISIKO** Penyakit Jantung.")