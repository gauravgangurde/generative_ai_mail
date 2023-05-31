import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import openai

image = Image.open('exl.png')


openai.api_key = st.secrets["chat_gpt_key"]

df = pd.read_csv('performance.csv')

def openai_response(query):
   response = openai.ChatCompletion.create(
   model="gpt-3.5-turbo",

   messages = [
       {"role":"system", "content":"You are helpful assistant."},
       {"role":"user","content": query}
   ]
   )
   return response.choices[0]['message']['content']   
    
with st.sidebar:
    st.image(image, width = 150)
    st.header('Generative AI')


st.header("Personalized communication ")

with st.form("my_form"):
   name = st.selectbox('Please select name',df["name"])
   intent_of_mail = st.text_input(label ="Intent of mail" , placeholder = 'Intent')
   category = df[df.name == name]['performance'].to_string(index=False)
   target = df[df.name == name]['target'].to_string(index=False)
   latest_performance = df[df.name == name]['latest_month_performance'].to_string(index=False)
   
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
    response = openai_response(f"""Write a {intent_of_mail} mail to a salesperson {name} as their employer based on following information starts and ends with triplle dashes marks,
Analyse the data to determine whether a salesperson's performance is above or below target and how it impacts the performance category,
offer some insight based on performance and their category,
--- {name} is {category} with their target, their latest target was {target} and latest performance was {latest_performance} ---
""")
    st.text(f"""Category : {category}\nTarget : {target}\nLatest performance : {latest_performance}""")
    st.write()
    st.markdown(response)

