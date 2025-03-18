import pandas as pd
import numpy as np
import streamlit as st

# Titel van de app
st.title("📊 Social Impact Score Dashboard")
st.write("Pas de gewichten aan en bekijk de impact op de Social Impact Score (SIS).")

# Laden van dataset
@st.cache_data
def load_data():
    file_path = "Sociale impact CHATGPT.xlsx"  # Zorg ervoor dat dit bestand in je repo staat
    df = pd.read_excel(file_path, sheet_name='Blad1', skiprows=1)
    return df

df = load_data()

# Kolommen corrigeren
corrected_columns = [
    "Item", "Fictieve data", "Onbekend1", "Afstand tot Natura 2000 gebied", "Afstand tot kust",
    "Culturele evenementen", "Supermarkten", "Cafés", "Misdaadcijfers", "Basisscholen",
    "Gemiddelde woningprijzen", "Woning type", "Eigendomssituatie", "Woonoppervlakte",
    "Aantal Kamers", "Energielabel", "WOZ-waarde", "Whooz-label", "Leeftijd",
    "Opleidingsniveau", "Gezinsgrootte", "Inkomen", "Woonlasten"
]
df.columns = corrected_columns
df = df.drop(columns=["Fictieve data", "Onbekend1", "Item"])

# Numerieke kolommen
numeric_columns = [
    "Afstand tot Natura 2000 gebied", "Afstand tot kust", "Culturele evenementen", 
    "Supermarkten", "Cafés", "Misdaadcijfers", "Basisscholen", "Gemiddelde woningprijzen", 
    "Woonoppervlakte", "Aantal Kamers", "WOZ-waarde", "Leeftijd", "Gezinsgrootte", "Inkomen", "Woonlasten"
]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Normalisatie (0-1 schaal)
for col in numeric_columns:
    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

# Standaardgewichten
weights = {
    "Afstand tot Natura 2000 gebied": -0.1,
    "Afstand tot kust": -0.1,
    "Culturele evenementen": 0.1,
    "Supermarkten": 0.15,
    "Cafés": 0.1,
    "Misdaadcijfers": -0.2,
    "Basisscholen": 0.1,
    "Gemiddelde woningprijzen": 0.05,
    "Woonoppervlakte": 0.15,
    "Aantal Kamers": 0.1,
    "WOZ-waarde": 0.05,
    "Leeftijd": -0.05,
    "Gezinsgrootte": 0.05,
    "Inkomen": 0.2,
    "Woonlasten": -0.1
}

# Interactieve gewichtsinstellingen met sliders
st.sidebar.header("⚖️ Pas de gewichten aan")
for col in weights.keys():
    weights[col] = st.sidebar.slider(f"{col}", min_value=-0.2, max_value=0.2, value=weights[col], step=0.05)

# Berekening Social Impact Score
df["Social Impact Score"] = sum(df[col] * weights[col] for col in weights.keys())

# Weergave van resultaten
st.subheader("📊 Resultaten")
st.write("Hieronder zie je de berekende Social Impact Score per locatie.")
st.dataframe(df[["Social Impact Score"] + numeric_columns])

# Grafiek van de Social Impact Score
st.subheader("📈 Visualisatie van de Social Impact Score")
st.bar_chart(df["Social Impact Score"])

