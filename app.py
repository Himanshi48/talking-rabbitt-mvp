import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page config
st.set_page_config(
    page_title="Talking Rabbitt",
    page_icon="🐰",
    layout="wide"
)

st.title("🐰 Talking Rabbitt")
st.caption("Talk to your business data in seconds.")

st.write("Upload a CSV and ask questions like a conversation.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    question = st.text_input("Ask a question about your data")

    if question:

        data_sample = df.head(20).to_string()

        prompt = f"""
You are a business data analyst.

Here is a sample of the dataset:

{data_sample}

User question:
{question}

Give a clear short answer based on the data.
"""

        try:

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            answer = response.choices[0].message.content

        except Exception:

            answer = "⚠️ AI quota exceeded. Showing basic data insights instead."

        st.success(answer)

        # Automated visualization example
        if "Region" in df.columns and "Revenue" in df.columns:

            chart_data = df.groupby("Region")["Revenue"].sum()

            fig, ax = plt.subplots()
            chart_data.plot(kind="bar", ax=ax)

            st.subheader("Revenue by Region")
            st.pyplot(fig)