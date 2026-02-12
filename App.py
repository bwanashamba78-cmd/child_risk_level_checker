import streamlit as st
import pandas as pd
import joblib

# Load model and encoder
model = joblib.load("childrisklevel.pkl")
decode_map = {0: "Low", 1: "Medium", 2: "High"}


# Language selection
language = st.selectbox("Select Language / Chagua Lugha", ["English", "Swahili"])

# Translation dictionary
texts = {
    "title": {"English": "Child Illness Risk Checker", "Swahili": "Kikokotoo cha Hatari ya Ugonjwa wa Mtoto"},
    "enter_details": {"English": "Enter Child Details", "Swahili": "Weka Taarifa za Mtoto"},
    "child_name": {"English": "Child Name", "Swahili": "Jina la Mtoto"},
    "child_age": {"English": "Child Age (years)", "Swahili": "Umri wa Mtoto (miaka)"},
    "select_symptoms": {"English": "Select Symptoms", "Swahili": "Chagua Dalili"},
    "predict_button": {"English": "Predict Risk Level", "Swahili": "Kadiria Hatari"},
    "error_name": {"English": "Please enter the child's name.", "Swahili": "Tafadhali weka jina la mtoto."},
    "low_risk": {"English": "Low Risk", "Swahili": "Hatari Ndogo"},
    "medium_risk": {"English": "Medium Risk", "Swahili": "Hatari ya Kati"},
    "high_risk": {"English": "High Risk", "Swahili": "Hatari Kubwa"},
    "probability_breakdown": {"English": "Probability Breakdown", "Swahili": "Ufafanuzi wa Uwezekano"},
    "disclaimer": {
        "English": "This App supports decision-making but does NOT replace a healthcare professional",
        "Swahili": "App hii inasaidia kufanya maamuzi lakini HAIJABADILI mtaalamu wa afya"
    },
    "warning_high": {
        "English": "🚨 HIGH RISK: Please visit a nearby healthcare facility immediately!",
        "Swahili": "🚨 HATARI KUBWA: Tafadhali tembelea kituo cha afya mara moja!"
    },
    "warning_medium": {
        "English": "⚠️ MEDIUM RISK: Monitor symptoms and consider seeing a clinician soon.",
        "Swahili": "⚠️ HATARI YA KATI: Fuatilia dalili na fikiria kumuona daktari."
    },
    "warning_low": {
        "English": "✅ LOW RISK: Continue home care and monitor symptoms.",
        "Swahili": "✅ HATARI NDOGO: Endelea na uangalizi nyumbani na fuatilia dalili."
    },
    # Symptoms translation
    "Fever": {"English": "Fever", "Swahili": "Homa"},
    "Cough": {"English": "Cough", "Swahili": "Kikohozi"},
    "Vomiting": {"English": "Vomiting", "Swahili": "Kutapika"},
    "Diarrhea": {"English": "Diarrhea", "Swahili": "Kuhara"},
    "Fatigue": {"English": "Fatigue", "Swahili": "Uchovu"},
    "Lethargy": {"English": "Lethargy", "Swahili": "Udhaifu"},
    "Rash": {"English": "Rash", "Swahili": "Vipere"}
}

# Helper function
def t(key):
    return texts[key][language]

# App title
st.title(t("title"))

# Input section
st.header(t("enter_details"))
child_name = st.text_input(t("child_name"))
child_age = st.number_input(t("child_age"), min_value=0, max_value=18, value=1)

st.subheader(t("select_symptoms"))
Fever = st.checkbox(f"{t('Fever')}")
Cough = st.checkbox(f"{t('Cough')}")
Vomiting = st.checkbox(f"{t('Vomiting')}")
Diarrhea = st.checkbox(f"{t('Diarrhea')}")
Fatigue = st.checkbox(f"{t('Fatigue')}")
Lethargy = st.checkbox(f"{t('Lethargy')}")
Rash = st.checkbox(f"{t('Rash')}")

# Predict button
if st.button(t("predict_button")):

    if child_name.strip() == "":
        st.error(t("error_name"))
    else:
        # Convert input to DataFrame
        user_input = pd.DataFrame([[ 
            child_age,
            int(Fever),
            int(Cough),
            int(Vomiting),
            int(Diarrhea),
            int(Fatigue),
            int(Lethargy),
            int(Rash)
        ]], columns=[
            'Age','Fever','Cough','Vomiting',
            'Diarrhea','Fatigue','Lethargy','Rash'
        ])

        # Predict
        prediction = model.predict(user_input)[0]
        probabilities = model.predict_proba(user_input)[0]

        # Decode prediction
        risk_level = decode_map.get(int(prediction), "Unknown")

        # Extract probabilities
        low_risk = probabilities[0] * 100
        medium_risk = probabilities[1] * 100
        high_risk = probabilities[2] * 100

        # Display result
        st.subheader(f"📋 Risk Assessment for {child_name} ({child_age} years)")
        st.write(f"### Risk Level: **{risk_level}**")

        st.markdown(f"📊 {t('probability_breakdown')}")
        st.write(f"🟢 {t('low_risk')}: {low_risk:.1f}%")
        st.write(f"🟡 {t('medium_risk')}: {medium_risk:.1f}%")
        st.write(f"🔴 {t('high_risk')}: {high_risk:.1f}%")

        # Medical guidance
        if risk_level == "High":
            st.warning(t("warning_high"))
        elif risk_level == "Medium":
            st.info(t("warning_medium"))
        else:
            st.success(t("warning_low"))

# Disclaimer
st.caption(t("disclaimer"))
