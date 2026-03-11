import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Talking Rabbitt 🐰")
st.write("Ask questions about your data using natural language.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())

    question = st.text_input("Ask a question about your data")

    if question:

        st.write("You asked:", question)

        # Example logic
        if "highest revenue" in question.lower():

            result = df.groupby("Region")["Revenue"].sum()

            max_region = result.idxmax()

            st.success(f"{max_region} region has the highest revenue.")

            st.subheader("Revenue by Region")

            fig, ax = plt.subplots()
            result.plot(kind="bar", ax=ax)

            st.pyplot(fig)