import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="RFM Analysis Dashboard", layout="wide")

st.title("📊 RFM Analysis Dashboard")

# --- Add a button to download sample CSV ---
@st.cache
def generate_sample_csv():
    # Create a sample DataFrame
    data = {
        'Member_number': [100, 20, 3, 4, 5],
        'TransactionDate': [
            '2025-01-01', '2025-02-15', '2025-03-20', '2025-04-10', '2025-04-05'
        ],
        'Amount': [100, 250, 150, 300, 200]
    }
    df_sample = pd.DataFrame(data)
    return df_sample

st.download_button(
    label="📥 Download Sample CSV",
    data=generate_sample_csv().to_csv(index=False),
    file_name="sample_customer_transactions.csv",
    mime="text/csv"
)

# --- Upload File ---
uploaded_file = st.file_uploader("📁 Upload Customer Transaction CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Preview of Customer Transaction Data")
    st.dataframe(df.head())

    # --- Check if required columns exist ---
    if 'Member_number' in df.columns and 'TransactionDate' in df.columns and 'Amount' in df.columns:
        # --- Convert 'TransactionDate' to datetime ---
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])

        # --- Calculate Recency, Frequency, and Monetary ---
        snapshot_date = df['TransactionDate'].max() + pd.Timedelta(days=1)  # Next day after last transaction

        # Recency: Days since last transaction
        recency = df.groupby('Member_number')['TransactionDate'].max().reset_index()
        recency['Recency'] = (snapshot_date - recency['TransactionDate']).dt.days

        # Frequency: Number of transactions
        frequency = df.groupby('Member_number')['TransactionDate'].count().reset_index()
        frequency['Frequency'] = frequency['TransactionDate']

        # Monetary: Total spending
        monetary = df.groupby('Member_number')['Amount'].sum().reset_index()
        monetary['Monetary'] = monetary['Amount']

        # Merging Recency, Frequency, and Monetary
        rfm_df = recency[['Member_number', 'Recency']].merge(frequency[['Member_number', 'Frequency']], on='Member_number')
        rfm_df = rfm_df.merge(monetary[['Member_number', 'Monetary']], on='Member_number')

        # --- Display the RFM Data ---
        st.subheader("📊 RFM Data")
        st.dataframe(rfm_df.head())

        # --- Save the RFM Data to a new CSV file ---
        output_file = "rfm_data.csv"
        rfm_df.to_csv(output_file, index=False)

        st.download_button(label="Download RFM CSV", data=rfm_df.to_csv(index=False), file_name=output_file, mime="text/csv")

        st.success("RFM data has been processed and saved. You can download the file now.")

    else:
        st.warning("CSV file must contain 'Member_number', 'TransactionDate', and 'Amount' columns.")

else:
    st.info("Please upload a customer transaction CSV file to start.")

df=rfm_df
st.subheader("📄 Preview of RFM Data")
st.dataframe(df.head())

    # --- Check if columns exist ---
if 1==1:    
    if all(col in df.columns for col in ['Recency', 'Frequency', 'Monetary']):
        # --- Histograms ---
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

        # --- Scatter Plot ---
        st.subheader("🧮 Scatter Plots")

        fig_scatter = px.scatter(df, x='Recency', y='Monetary', size='Frequency',
                                 title='Recency vs Monetary (size by Frequency)',
                                 hover_data=df.columns)
        st.plotly_chart(fig_scatter, use_container_width=True)

        # --- Correlation Heatmap ---
        st.subheader("📌 Correlation Heatmap")
        corr = df[['Recency', 'Frequency', 'Monetary']].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    else:
        st.warning("CSV file must contain 'Recency', 'Frequency', and 'Monetary' columns.")

else:
    st.info("Please upload a CSV file to start.")