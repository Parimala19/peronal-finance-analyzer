import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Analyzer", page_icon="💸", layout="wide")
st.title("💸 Personal Finance Analyzer")
st.markdown("Upload your CSV file to analyze your spending.")

# Upload CSV
uploaded_file = st.file_uploader("Upload your expense CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Check required columns
    required_columns = {'Date', 'Category', 'Amount', 'Description'}
    if not required_columns.issubset(df.columns):
        st.error("CSV must contain columns: Date, Category, Amount, Description")
    else:
        # Convert date column
        df['Date'] = pd.to_datetime(df['Date'])

        # Tabs for different views
        tab1, tab2 = st.tabs(["📊 Summary", "📅 Monthly Trends"])

        with tab1:
            st.subheader("📊 Expense Summary")

            total_spent = df['Amount'].sum()
            top_categories = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

            st.success(f"**Total Expenses:** ₹{total_spent:,.2f}")

            st.markdown("#### Top Spending Categories")
            st.bar_chart(top_categories)

            with st.expander("📋 View Raw Data"):
                st.dataframe(df.sort_values("Date", ascending=False))

        with tab2:
            st.subheader("📅 Monthly Spending Overview")
            df['Month'] = df['Date'].dt.to_period('M').astype(str)
            monthly_total = df.groupby('Month')['Amount'].sum().reset_index()

            st.bar_chart(monthly_total.set_index('Month'))
            st.line_chart(monthly_total.set_index('Month'))

            with st.expander("📊 Show Monthly Totals Table"):
                st.dataframe(monthly_total)

else:
    st.info("Please upload a CSV file to get started.")
