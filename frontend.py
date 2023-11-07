import streamlit as st
import pandas as pd
import sqlite3
import pandas as pd

# Create your connection.
db = sqlite3.connect('toxic.db')
df = pd.read_sql_query("SELECT * FROM messages", db)
df['incident_date'] = pd.to_datetime(df['incident_date'])
df.sort_values(by='id', ascending =False, inplace=True)

st.markdown('''<style> 
            .st-emotion-cache-1y4p8pa {
            max-width: 83rem;
            } 
            </style>''', unsafe_allow_html=True)


st.write("""# Incident Report""")

st.data_editor(
    df,
    num_rows=15,
    column_config={
        "incident_date": st.column_config.DateColumn(
            "Incident Date",
            format="HH:MM- DD/MM/YYYY",
        ),
        'toxic_text': st.column_config.Column(
            "Toxic Text",
            width=400,
        ),
        'neutered_text': st.column_config.Column(
            "Neutered Text",
        ),
        'sender': st.column_config.Column(
            "Username",
        ),
    },
    hide_index=True,
)
