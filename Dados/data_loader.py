import streamlit as st
import pandas as pd

def initialize_session_kapthae():
    if 'kapthae' not in st.session_state:
        df = pd.read_csv("Dados/Kaptha-Enterprise-Meta-Dados.csv")
        st.session_state['kapthae'] = df

def initialize_session_leads():
    if'leads' not in st.session_state:
        df = pd.read_csv("Dados/Leads-Data-Data.csv")
        st.session_state['leads'] = df