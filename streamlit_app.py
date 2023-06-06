import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import openai
import ast
import csv

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
	temperature = 0.6,
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

# to convert dictionary to '|' delimited csv
def dicts_to_csv(list_of_dicts, filename):
    keys = list_of_dicts[0].keys()

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys, delimiter='|')
        writer.writeheader()
        writer.writerows(list_of_dicts)
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
		response = openai_response(f"""Your task is to write mail to agents in {category} performance category about their performance data delimited by three backticks,
					generate new mail for each agent with keeping content of body similar,
					giving feedback, suggesting improvment areas, and it should include 2 sales improvement article or training link references based on performance category
					Please keep the mail concise and sign it as 'Manager'
					Provide output in JSON format only with following keys:
					name, performance category,mail
					data: ```{data} ``` """)
		res = ast.literal_eval(response.replace('\n','\\n'))
		
		for i in res.keys():
			df = (pd.DataFrame.from_dict(res[i]))
			dicts_to_csv(res[i], 'mails_data.csv')
			st.dataframe(pd.read_csv('mails_data.csv', sep = '|'))
