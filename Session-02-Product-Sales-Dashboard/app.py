import os
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # reads OPENAI_API_KEY (and OPENAI_MODEL) from a .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="👷", layout="centered")
st.title("👷 Product Sales Dashboard + AI Q&A")

#upload the scrapped csv data file
st.subheader("Upload Data")
upload_file = st.file_uploader("Upload a CSV file", type="csv")
 
if upload_file:    
    ref_data = pd.read_csv(upload_file)

    st.subheader("Data")
    st.dataframe(ref_data, width='stretch')

#most sold product
    st.subheader("Which Brand Sold the Most product")
    fig1 = px.pie(ref_data, names="Brand", values="Bought past month")
    st.plotly_chart(fig1, width='stretch')

#Review products
    st.subheader("Reviews per Product")
    reviews = ref_data.set_index("Brand")["Reviews"].sort_values(ascending=False)
    st.bar_chart(reviews)

#Ai powered Q&A
    with st.sidebar:
        question = st.text_area("Ask me anything", placeholder="e.g. Which brand sold the most units this month?", height=120)
    
        if st.button("Enter") and question:
            # We hand the AI the exact data it's allowed to use, as plain text.
            data_as_text = ref_data.to_csv(index=False)

            system_prompt = (
                "You are a data analyst. Answer ONLY using the CSV data provided below. "
                "If the answer cannot be found in the data, say so clearly instead of guessing. "
                "Do not use any outside knowledge about products, brands, or prices.\n\n"
                f"DATA:\n{data_as_text}"
            )

            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question},
                    ],
                )
                answer = response.choices[0].message.content

            st.success(answer)