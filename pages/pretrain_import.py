import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from datetime import datetime

st.set_page_config(page_title="RFM Analysis Dashboard", layout="wide")
st.title("📊 RFM Analysis Dashboard")

# --- Sample CSV for download ---
@st.cache
def generate_sample_csv():
    data = {
        'Member_number': [100, 20, 3, 4, 5],
        'TransactionDate': ['2025-01-01', '2025-02-15', '2025-03-20', '2025-04-10', '2025-04-05'],
        'Amount': [100, 250, 150, 300, 200]
    }
    return pd.DataFrame(data)

st.download_button(
    label="📥 Download Sample CSV",
    data=generate_sample_csv().to_csv(index=False),
    file_name="sample_customer_transactions.csv",
    mime="text/csv"
)

# --- Upload File ---
uploaded_file = st.file_uploader("📁 Upload Customer Transaction CSV file", type=["csv"])

if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)

    st.subheader("📄 Preview of Customer Transaction Data")
    st.dataframe(df_raw.head())

    # --- Check required columns ---
    required_cols = ['Member_number', 'TransactionDate', 'Amount']
    if all(col in df_raw.columns for col in required_cols):
        # --- Convert TransactionDate ---
        df_raw['TransactionDate'] = pd.to_datetime(df_raw['TransactionDate'])

        # --- RFM Processing ---
        snapshot_date = df_raw['TransactionDate'].max() + pd.Timedelta(days=1)

        recency = df_raw.groupby('Member_number')['TransactionDate'].max().reset_index()
        recency['Recency'] = (snapshot_date - recency['TransactionDate']).dt.days

        frequency = df_raw.groupby('Member_number')['TransactionDate'].count().reset_index()
        frequency['Frequency'] = frequency['TransactionDate']

        monetary = df_raw.groupby('Member_number')['Amount'].sum().reset_index()
        monetary['Monetary'] = monetary['Amount']

        # Merge RFM
        rfm_df = recency[['Member_number', 'Recency']].merge(
            frequency[['Member_number', 'Frequency']], on='Member_number'
        ).merge(
            monetary[['Member_number', 'Monetary']], on='Member_number'
        )

        st.subheader("📊 RFM Data")
        st.dataframe(rfm_df.head())

        st.download_button(
            label="📥 Download RFM CSV",
            data=rfm_df.to_csv(index=False),
            file_name="rfm_data.csv",
            mime="text/csv"
        )

        st.success("✅ RFM data has been processed and is ready for analysis.")

        # === Visualizations ===
        df = rfm_df  # Gán để tiện dùng

        if all(col in df.columns for col in ['Recency', 'Frequency', 'Monetary']):
            st.subheader("🔍 Distribution Plots")

            col1, col2, col3 = st.columns(3)
            with col1:
                fig_r = px.histogram(df, x='Recency', nbins=30, title='Recency Distribution')
                st.plotly_chart(fig_r, use_container_width=True)
            with col2:
                fig_f = px.histogram(df, x='Frequency', nbins=30, title='Frequency Distribution')
                st.plotly_chart(fig_f, use_container_width=True)
            with col3:
                fig_m = px.histogram(df, x='Monetary', nbins=30, title='Monetary Distribution')
                st.plotly_chart(fig_m, use_container_width=True)

            st.subheader("🧮 Scatter Plot: Recency vs Monetary (size = Frequency)")
            fig_scatter = px.scatter(df, x='Recency', y='Monetary', size='Frequency',
                                     title='Recency vs Monetary',
                                     hover_data=df.columns)
            st.plotly_chart(fig_scatter, use_container_width=True)

            st.subheader("📌 Correlation Heatmap")
            corr = df[['Recency', 'Frequency', 'Monetary']].corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)

    else:
        st.warning("❌ CSV file must contain columns: 'Member_number', 'TransactionDate', and 'Amount'.")

else:
    st.info("📂 Please upload a customer transaction CSV file to begin.")
