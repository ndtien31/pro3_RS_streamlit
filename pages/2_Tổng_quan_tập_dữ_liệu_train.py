import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="RFM Dashboard", layout="wide")

st.title("📊 RFM Analysis Dashboard import")

# --- Đọc file CSV từ ổ đĩa ---
try:
    df = pd.read_csv("rfm.csv")  # Thay bằng đường dẫn đúng nếu file ở thư mục khác

    st.subheader("📄 Preview of RFM Data import")
    st.dataframe(df.head())

    # --- Kiểm tra cột cần thiết ---
    if all(col in df.columns for col in ['Recency', 'Frequency', 'Monetary']):
        # --- Histogram ---
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
        st.subheader("🧮 Scatter Plot")
        fig_scatter = px.scatter(df, x='Recency', y='Monetary', size='Frequency',
                                 title='Recency vs Monetary (size by Frequency)',
                                 hover_data=df.columns)
        st.plotly_chart(fig_scatter, use_container_width=True)

        # --- Heatmap ---
        st.subheader("📌 Correlation Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(df[['Recency', 'Frequency', 'Monetary']].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    else:
        st.error("⚠️ File không chứa đầy đủ các cột: Recency, Frequency, Monetary.")

except FileNotFoundError:
    st.error("❌ Không tìm thấy file 'rfm.csv'. Vui lòng kiểm tra lại đường dẫn.")
