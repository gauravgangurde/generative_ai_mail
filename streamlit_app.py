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
	],
	temperature = 0,
	)
	return response.choices[0]['message']['content']  
	
def row_converter(row, listy):
	#convert pandas row to a dictionary
	#requires a list of columns and a row as a tuple
	count = 1
	pictionary = {}
	pictionary['Index'] = row[0]
	for item in listy:
		pictionary[item] = row[count]
		count += 1
	print(pictionary)
	return pictionary
	
with st.sidebar:
	st.image(image, width = 150)
	st.header('Generative AI')


st.header("Personalized communication ")

with st.form("my_form"):
	name = st.selectbox('Please select name',df['performance'])
	df = df[df['performance']==name]
	intent_of_mail = st.text_input(label ="Intent of mail" , placeholder = 'Intent')
	category = df[df.name == name]['performance'].to_string(index=False)
	target = df[df.name == name]['target'].to_string(index=False)
	latest_performance = df[df.name == name]['latest_month_performance'].to_string(index=False)
	
	# Every form must have a submit button.
	submitted = st.form_submit_button("Submit")
	if submitted:
		data = []
		listy = df.columns
		for row in df.itertuples():
			data.append(row_converter(row, listy))
		st.markdown(data)
		response = openai_response(f"""Your task is to write feedback mail to agents in {category} performance category as their manager.
				Write a seperate mail for each agent with same email body only thing differentiate between them is their sales performance and target.
				Use data delimited by triple backticks.
				Provide output in JSON format with following keys:
				name, performance category,mail
				data: ```{data} ``` """)
		st.write()
		st.markdown(response)
