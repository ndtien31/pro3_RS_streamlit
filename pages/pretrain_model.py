import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import silhouette_score
from io import BytesIO
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ===================== ⚙️ Cấu hình =====================
MODEL_PATH = 'rfm_clustering_model.pkl'
OLD_DATA_PATH = 'rfm.csv'

# ===================== 🧠 Load mô hình =====================
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

# ===================== 🎨 Boxplot RFM =====================
def plot_rfm_boxplot(df):
    st.subheader("📊 Phân bố RFM theo cụm")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for i, col in enumerate(['Recency', 'Frequency', 'Monetary']):
        sns.boxplot(data=df, x='Cluster', y=col, ax=axes[i], palette='Set2')
        axes[i].set_title(f'{col} by Cluster')
    st.pyplot(fig)

# ===================== 💠 Bubble Chart =====================
def plot_bubble_chart(df):
    summary = df.groupby('Cluster').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean',
        'Cluster': 'count'
    }).rename(columns={'Cluster': 'Count'}).reset_index()

    summary['Label'] = summary.apply(lambda row:
        f"Cluster {int(row['Cluster'])}<br>"
        f"Recency={int(row['Recency'])}<br>"
        f"Frequency={int(row['Frequency'])}<br>"
        f"Monetary={int(row['Monetary'])}<br>"
        f"Customers={int(row['Count'])}", axis=1)

    fig = px.scatter(
        summary,
        x='Recency',
        y='Frequency',
        size='Monetary',
        color='Cluster',
        hover_name='Label',
        title='Customer Segments Bubble Chart',
        size_max=100,
        template='plotly_white'
    )
    fig.update_layout(
        xaxis_title='Recency Mean',
        yaxis_title='Frequency Mean'
    )
    st.plotly_chart(fig)

# ===================== 🎯 Giao diện chính =====================
st.set_page_config(page_title="RFM Clustering Retrainer", layout="wide")
st.title("🔁 RFM Clustering Retrainer with Streamlit")

with st.sidebar:
    st.header("⚙️ Tùy chọn huấn luyện")
    n_clusters = st.slider("Số cụm (n_clusters)", min_value=2, max_value=10, value=4)
    use_log = st.checkbox("Dùng Log Transform", value=True)

uploaded_file = st.file_uploader("📤 Tải lên file CSV mới", type='csv')

if uploaded_file:
    # Đọc dữ liệu
    df_new = pd.read_csv(uploaded_file)
    st.success("✅ Dữ liệu mới đã được tải lên!")

    # Tải dữ liệu cũ và mô hình
    df_old = pd.read_csv(OLD_DATA_PATH)
    model_package = load_model()
    scaler = model_package['scaler']

    # Tiền xử lý
    rfm_old = df_old[['Recency', 'Frequency', 'Monetary']].copy()
    rfm_new = df_new[['Recency', 'Frequency', 'Monetary']].copy()
    rfm_combined = pd.concat([rfm_old, rfm_new], ignore_index=True)

    # Log transform nếu chọn
    if use_log:
        rfm_combined = np.log1p(rfm_combined)

    # Scale với scaler cũ
    rfm_scaled = scaler.transform(rfm_combined)

    # Huấn luyện lại KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=1)
    clusters = kmeans.fit_predict(rfm_scaled)

    # Gán cụm
    df_combined = pd.concat([df_old, df_new], ignore_index=True)
    df_combined['Cluster'] = clusters

    # Đánh giá
    sil_score = silhouette_score(rfm_scaled, clusters)
    inertia = kmeans.inertia_

    st.subheader("📈 Kết quả mô hình mới")
    st.write(f"✅ Silhouette Score: `{sil_score:.4f}`")
    st.write(f"✅ Inertia: `{inertia:.2f}`")

    # Hiển thị bảng dữ liệu
    st.subheader("📋 Dữ liệu đầu ra (hiển thị 20 dòng đầu)")
    st.dataframe(df_combined.head(20), use_container_width=True)

    # Biểu đồ
    plot_rfm_boxplot(df_combined)
    plot_bubble_chart(df_combined)

    # Lưu model mới
    model_package_new = {
        'kmeans': kmeans,
        'scaler': scaler,
        'log_transform': use_log
    }
    joblib.dump(model_package_new, 'rfm_clustering_model_retrained.pkl')
    st.success("💾 Đã lưu mô hình mới vào `rfm_clustering_model_retrained.pkl`")

    # Xuất file
    csv_buffer = BytesIO()
    df_combined.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Tải file kết quả CSV",
        data=csv_buffer.getvalue(),
        file_name='rfm_clustered_combined.csv',
        mime='text/csv'
    )
