import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="RFM Dashboard", layout="wide")

st.title("📊 RFM Analysis Dashboard")

# --- Upload File ---
uploaded_file = st.file_uploader("📁 Upload RFM CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Preview of RFM Data")
    st.dataframe(df.head())

    # --- Check if columns exist ---
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