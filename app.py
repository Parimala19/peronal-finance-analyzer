import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Analyzer", page_icon="💸", layout="wide")
st.title("💸 Personal Finance Analyzer")
st.markdown("Upload your expense CSV file to get smart insights about your spending.")

# File uploader
uploaded_file = st.file_uploader("📁 Upload your CSV file (with Date, Category, Amount, Description)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Ensure required columns are present
    required_columns = {'Date', 'Category', 'Amount', 'Description'}
    if not required_columns.issubset(df.columns):
        st.error("❌ CSV must contain these columns: Date, Category, Amount, Description")
    else:
        # Clean and process
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M').astype(str)

        total_spent = df['Amount'].sum()
        top_categories = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        monthly_total = df.groupby('Month')['Amount'].sum().reset_index()

        # Tabs
        tab1, tab2, tab3 = st.tabs(["📊 Summary", "📅 Monthly Trends", "💡 Smart Tips"])

        # 📊 Summary Tab
        with tab1:
            st.subheader("📊 Expense Summary")
            st.success(f"**Total Expenses:** ₹{total_spent:,.2f}")

            st.markdown("#### Top Spending Categories")
            st.bar_chart(top_categories)

            with st.expander("🔍 View Raw Data"):
                st.dataframe(df.sort_values("Date", ascending=False))

        # 📅 Monthly Trends Tab
        with tab2:
            st.subheader("📅 Monthly Spending Overview")
            st.bar_chart(monthly_total.set_index('Month'))
            st.line_chart(monthly_total.set_index('Month'))

            with st.expander("📊 View Monthly Totals Table"):
                st.dataframe(monthly_total)

        # 💡 Smart Tips Tab
        with tab3:
            st.subheader("💡 Smart Spending Tips")

            top_category = top_categories.idxmax()
            top_amount = top_categories.max()
            threshold = total_spent * 0.3

            st.markdown(f"### 📌 Top Category: **{top_category}** (₹{top_amount:,.2f})")

            if top_amount > threshold:
                st.warning(f"⚠️ You're spending more than 30% of your budget on **{top_category}**. Consider reducing it.")
            else:
                st.success(f"✅ Your spending on **{top_category}** seems balanced.")

            st.markdown("#### 📝 General Budgeting Tips")
            st.markdown("""
            - Track expenses monthly and compare trends.
            - Try the **50/30/20 rule**: 50% needs, 30% wants, 20% savings.
            - Set limits on categories where you overspend.
            - Review subscriptions or recurring charges.
            - Use tools like this to stay accountable.
            """)
else:
    st.info("Please upload a CSV file to begin analysis.")
