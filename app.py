import streamlit as st
import pandas as pd

# Función para estandarizar nombres de columnas
def limpiar_nombres(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

if 'datasets' not in st.session_state:
    df1 = pd.read_csv('datasets/StressLevelDataset_limpio.csv')
    df2 = pd.read_csv('datasets/student_mental_health_burnout_10k.csv')
    
    st.session_state.datasets = {
        'estres': limpiar_nombres(df1),
        'burnout': limpiar_nombres(df2)
    }
