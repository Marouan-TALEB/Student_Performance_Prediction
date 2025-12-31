import streamlit as st
import joblib
import pandas as pd

# ================= CONFIGURATION =================
st.set_page_config(
    page_title="Prédiction de la performance",
    page_icon="🎓",
    layout="centered"
)

# ================= CHARGEMENT DU MODÈLE =================
linear_model = joblib.load("model.pkl")

# ================= FONCTION DE PRÉDICTION =================
def predict_score(hours_studied, previous_scores, sleep_hours,
                  papers_practiced, extracurricular):

    new_data = pd.DataFrame({
        "Hours Studied": [hours_studied],
        "Previous Scores": [previous_scores],
        "Sleep Hours": [sleep_hours],
        "Sample Question Papers Practiced": [papers_practiced],
        "Extracurricular Activities": [extracurricular]
    })

    predicted_score = linear_model.predict(new_data)[0]
    predicted_score = max(0, min(100, predicted_score))
    return predicted_score

# ================= INTERFACE =================
# Titre principal sans background
st.markdown(
    """
    <h1 style='text-align: center; color: #4B0082; font-weight: bold;'>
        🎓 Prédiction de la performance des étudiants
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: #555555;'>Entrez vos informations pour obtenir votre score prédit.</p>",
    unsafe_allow_html=True
)

st.write("---")

# ================= INPUTS =================
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        hours_studied = st.number_input("📘 Heures d’étude", 0.0, 24.0, step=0.5)
        previous_scores = st.number_input("📝 Note précédente", 0, 100)
        papers_practiced = st.number_input("📄 Sujets d’examen pratiqués", 0, 50)
        
    with col2:
        sleep_hours = st.number_input("😴 Heures de sommeil", 0.0, 24.0, step=0.5)
        extracurricular = st.selectbox("🏃 Activités extrascolaires", ["No", "Yes"])

st.write("---")

# ================= PRÉDICTION =================
if st.button("🔮 Prédire", use_container_width=True):
    predicted_score = predict_score(
        hours_studied,
        previous_scores,
        sleep_hours,
        papers_practiced,
        extracurricular
    )

    # Affichage du score
    st.markdown(
        f"<h2 style='text-align: center; color:#4B0082;'>📊 Score prédit : {predicted_score:.1f}</h2>",
        unsafe_allow_html=True
    )
    st.progress(int(predicted_score))

    # Message selon le score
    if predicted_score >= 75:
        st.success("🌟 Excellente performance attendue !")
    elif predicted_score >= 50:
        st.warning("🙂 Performance moyenne attendue.")
    else:
        st.error("⚠️ Performance faible — des efforts sont nécessaires.")
