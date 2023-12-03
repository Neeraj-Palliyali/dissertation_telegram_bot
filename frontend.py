import streamlit as st
import pandas as pd
import sqlite3
from keys import hg_token
import pandas as pd


def query(payload, model_id, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
	response = requests.post(API_URL, headers=headers, json=payload)

	return response.json()

    

from tqdm import tqdm
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


col1, col2 = st.columns([4,1])

with col1:
    # The message and nested widget will remain on the page
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
                width=300,
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
with col2:   
    st.write("""## Chat with the bot!!""")
    input_text = st.text_input("Enter toxic text!!", key="text")

    if input_text:
        import requests


        model_id = "NeerajPalliyali/t5_toxic_rephraser"
        api_token = hg_token # get yours at hf.co/settings/tokens
        data = query(input_text, model_id, api_token)
        text = data
        if text[0].get('estimated_time'):
             st.write("Wait for the model to load approx 60s")
        else:
            st.write(f"Neutered text: {text[0].get('generated_text')}")
