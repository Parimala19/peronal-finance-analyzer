import streamlit as st
import pandas as pd

st.set_page_config(page_title="💸 Personal Finance Analyzer", page_icon="📊")

st.title("💸 Personal Finance Analyzer")
st.markdown("Upload your expenses CSV to get smart insights about your spending.")

# File uploader
uploaded_file = st.file_uploader("Upload your expenses CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("📄 Uploaded Data")
        st.dataframe(df)

        # Preview total spending
        total = df['Amount'].sum()
        st.success(f"Total Spending: ₹{total}")
    except Exception as e:
        st.error("Something went wrong. Please upload a valid CSV file.")
        st.exception(e)
else:
    st.info("Please upload a CSV file to proceed.")
