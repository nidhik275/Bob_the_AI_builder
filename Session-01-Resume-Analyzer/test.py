import streamlit as st
import PyPDF2
import os
import io
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title='AI resume Analyser',layout='centered')

st.title("AI resume Analyser")
st.markdown("upload your resume and get AI powered feedback tailored to your need")

upload_file = st.file_uploader("upload resume")
job_desc = st.text_input("Enter job description")

submit = st.button('Analyse')

if submit and upload_file:
    file_content = upload_file.read().decode('utf-8')
    
    prompt = f""" Please analyse this resume and provide constructive feebback. 
    Focus on the following:
    1: content clarity and impact
    2. skill presentation
    3. experience description
    4. specific improvement for {job_desc}
    
    resume content: {file_content}
    
    Please provide your analysis in a clear, structured format with specific recommendations."""
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    st.markdown("### Analysis Results")
    st.markdown(response.choices[0].message.content)
    