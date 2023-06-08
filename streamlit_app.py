import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import openai
import ast
import csv
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

image = Image.open('exl.png')
workbook = Workbook()
sheet = workbook.active

openai.api_key = st.secrets["chat_gpt_key"]

df = pd.read_csv('report.csv')



with open("output.xlsx", "rb") as file:
	st.download_button(
		label="Download data as CSV",
		data=file,
		file_name='data.xlsx'
	)
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


if st.button("generate"):
	for i in range(1):#len(df)):
		df2 = df.iloc[[i]]
		data = df2.to_dict()
		st.markdown(data)
		st.dataframe(df2)
		response = openai_response(f"""Your task is to write at least 250 word mail about their performance data delimited by three backticks,
					analysing performance, give feedback based on category, suggesting improvement areas, and it should include 2 sales trainng article or link references based on the performance and category
					Please keep the mail concise and sign it as 'Manager'
					Provide output in mail only, do not embed input data
					data: ```{data} ``` """)
		st.markdown(response)
		
		#res = ast.literal_eval(response)#.replace('\n','\\n'))
		df2['Mail'] = response
		st.write(df2)
		for row in dataframe_to_rows(df2, index=False, header=False):
    			sheet.append(row)
	
	workbook.save('output.xlsx')
