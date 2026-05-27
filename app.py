import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bienestar Estudiantil", layout="wide")

def limpiar_columnas(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

if 'datasets' not in st.session_state:
    try:
        df1 = pd.read_csv('datasets/StressLevelDataset_limpio.csv')
        df2 = pd.read_csv('datasets/student_mental_health_burnout_10k.csv')
        st.session_state.datasets = {
            'estres': limpiar_columnas(df1),
            'burnout': limpiar_columnas(df2)
        }
    except Exception as e:
        st.error(f"Error crítico: {e}")

st.title("🎓 Sistema de Bienestar Estudiantil")
