import streamlit as st
import os
import sqlite3

import google.generativeai as genai
from langchain_community.utilities import SQLDatabase
## Configure Genai Key

genai.configure(api_key="AIzaSyCDh2UWso_kv9n0CEINwb3MnsTBWryNMm8")

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

def get_schema(conn):
    return conn.get_table_info()


def run_query(conn, query):
    return conn.run(query)

## Define Your Prompt

def get_prompt(schema, question):
    prompt=[
        f"""
        You are an expert in converting English questions to SQLite query!
        Based on the table schema below, write a SQLite query that would answer the user's question:
        {schema}

        Question: {question}
        SQL Query:

        """
    ]

    return prompt

def format_response(response):
    response = response.replace("```sql", "")
    response = response.replace("```", "")
    return str(response)
## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Retrieve SQL Data using Text prompts")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:

    with st.spinner("Fetching data......"):
        db = "temperature_data.db"
        conn = SQLDatabase.from_uri("sqlite:///temperature_data.db")
        table_info = get_schema(conn)
        response=get_gemini_response(question,get_prompt(table_info, question))
        #print(response)
        response = format_response(response)
        print(response)
        response=read_sql_query(response,db)
        st.subheader("The Response is")
        for row in response:
            print(row)
            st.header(row)