import pandas as pd
import numpy as np
import streamlit as st

# Dataset laden
file_path = "/mnt/data/Sociale impact CHATGPT.xlsx"
df_cleaned = pd.read_excel(file_path, sheet_name='Blad1', skiprows=1)

# Kolommen corrigeren
corrected_columns = [
    "Item", "Fictieve data", "Onbekend1", "Afstand tot Natura 2000 gebied", "Afstand tot kust",
    "Culturele evenementen", "Supermarkten", "Cafés", "Misdaadcijfers", "Basisscholen",
    "Gemiddelde woningprijzen", "Woning type", "Eigendomssituatie", "Woonoppervlakte",
    "Aantal Kamers", "Energielabel", "WOZ-waarde", "Whooz-label", "Leeftijd",
    "Opleidingsniveau", "Gezinsgrootte", "Inkomen", "Woonlasten"
]
df_cleaned.columns = corrected_columns
df_cleaned = df_cleaned.drop(columns=["Fictieve data", "Onbekend1", "Item"])

# Numerieke kolommen
numeric_columns = [
    "Afstand tot Natura 2000 gebied", "Afstand tot kust", "Culturele evenementen", 
    "Supermarkten", "Cafés", "Misdaadcijfers", "Basisscholen", "Gemiddelde woningprijzen", 
    "Woonoppervlakte", "Aantal Kamers", "WOZ-waarde", "Leeftijd", "Gezinsgrootte", "Inkomen", "Woonlasten"
]
for col in numeric_columns:
    df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors="coerce")

# Normalisatie
for col in numeric_columns:
    df_cleaned[col] = (df_cleaned[col] - df_cleaned[col].min()) / (df_cleaned[col].max() - df_cleaned[col].min())

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

# Streamlit-app
st.title("Social Impact Score Dashboard")
st.write("Pas de gewichten aan en bekijk de impact op de score.")

# Schuifregelaars voor gewichten
for col in weights.keys():
    weights[col] = st.slider(f"{col}", min_value=-0.2, max_value=0.2, value=weights[col], step=0.05)

# Berekening Social Impact Score
df_cleaned["Social Impact Score"] = sum(df_cleaned[col] * weights[col] for col in weights.keys())

# Weergave
st.dataframe(df_cleaned[["Social Impact Score"] + numeric_columns])

# Visualisatie
st.bar_chart(df_cleaned["Social Impact Score"])
