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
	for i in range(1,2):#len(df)):
		df2 = df.loc[i]
		data = df2.to_dict()
		#st.markdown(data)
		st.dataframe(df2)
		
		#based on performance category choose query
		if df2.loc[0, 'Category'] == 'Consistent Performer':
			query = """Your task is to write mail to insurance salesman about their performance data delimited by three backticks,
				analysing performance using their total sales, target and sales achieved percentages, give feedback based on performance category, congratulate and motivate them along with motivational quotes,
				offer some insight based on their performance
				Please keep the mail concise and sign it as 'Manager'
				"""
		elif df2.loc[0, 'Category'] == 'Consistent Non-performer':
			query ="""Your task is to write mail to salesman about their performance data delimited by three backticks,
				analysing performance using their total sales, target and sales achieved percentages, give feedback based on performance, suggesting improvement areas, and it should include 2 sales trainng article or link references based on the performance and category
				also include motivational quotes to motivate them
				Please keep the mail concise and sign it as 'Manager'
				""" 
		elif df2.loc[0, 'Category'] == 'Performer to Non-performer':
			query = """Your task is to write mail to salesman about their performance data delimited by three backticks,
				analysing performance using their total sales, target and sales achieved percentages, give feedback based on performance as their performance recentley dropped, suggesting improvement areas, and it should include 2 sales trainng article or link references based on the performance to improve it
				also include motivational quotes to motivate them
				Please keep the mail concise and sign it as 'Manager'
				"""
		elif df2.loc[0, 'Category'] == 'Non-performer to Performer':
			query = """Your task is to write mail to salesman about their performance data delimited by three backticks,
				analysing performance using their total sales, target and sales achieved percentages, give feedback based on performance as their performance recentley improved, suggesting improvement areas, and it should include 2 sales trainng article or link references based on the performance to further improve it
				also include motivational quotes to motivate them
				Please keep the mail concise and sign it as 'Manager'
				"""
		else:
			query = 'show message : category is not correct'
			
		response = openai_response(query + f"""\ndata: ```{data} ``` """)
		#st.markdown(response)
		
		#df2['Mail'] = response
		#st.write(df2)
		for row in dataframe_to_rows(df2, index=False, header=False):
    			sheet.append(row)
	
	workbook.save('output1.xlsx')
	with open("output1.xlsx", "rb") as file:
		st.download_button(
			label="Download data",
			data=file,
			file_name='data.xlsx'
		)
