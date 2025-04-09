import streamlit as st
import pandas as pd
import numpy as np
import json
from scipy.spatial.distance import euclidean

# Load centroids và scaler
with open("pyspark/centroids.json", "r") as f:
    centroids = np.array(json.load(f))

with open("pyspark/scaler_minmax.json", "r") as f:
    scaler = json.load(f)
    min_vals = np.array(scaler["min"])
    max_vals = np.array(scaler["max"])

# Hàm scale dữ liệu mới giống như MinMaxScaler của PySpark
def minmax_scale(row, min_vals, max_vals):
    return (row - min_vals) / (max_vals - min_vals + 1e-8)

# Hàm tính cụm gần nhất
def predict_cluster(point, centroids):
    distances = [euclidean(point, center) for center in centroids]
    return int(np.argmin(distances))

# Gợi ý theo từng nhóm (tuỳ chỉnh theo use-case của bạn)
cluster_suggestions = {
    1: "🟢 Nhóm tiềm năng cao - nên tập trung upsell hoặc giữ chân.",
    2: "🟡 Nhóm bình thường - có thể nuôi dưỡng thêm.",
    3: "🔴 Nhóm KH rời bỏ có giá trị thấp - cân nhắc chiến dịch khuyến mãi.",
    0: "🔵 Nhóm KH mới hoặc chưa rõ hành vi - nên theo dõi thêm.",
}

# Giao diện nhập liệu
st.title("📊 KMeans RFM Clustering (với MinMaxScaler)")

data = []
st.subheader("📥 Nhập dữ liệu 5 khách hàng")
for i in range(5):
    st.markdown(f"**Khách hàng {i+1}**")
    r = st.number_input(f"Recency {i+1}", min_value=0, value=10, key=f"r{i}")
    f_val = st.number_input(f"Frequency {i+1}", min_value=0, value=5, key=f"f{i}")
    m = st.number_input(f"Monetary {i+1}", min_value=0.0, value=100.0, key=f"m{i}")
    data.append([r, f_val, m])

if st.button("🔍 Dự đoán cụm"):
    df_new = pd.DataFrame(data, columns=["Recency", "Frequency", "Monetary"])
    
    # Scale dữ liệu
    scaled_data = df_new.apply(lambda row: minmax_scale(np.array(row), min_vals, max_vals), axis=1)
    scaled_data = np.vstack(scaled_data)

    # Dự đoán cụm
    clusters = [predict_cluster(x, centroids) for x in scaled_data]
    df_new["Cluster"] = clusters

    # Gợi ý cho từng nhóm
    df_new["Gợi ý hành động"] = df_new["Cluster"].apply(lambda x: cluster_suggestions.get(x, "Không xác định"))

    st.subheader("📈 Kết quả phân cụm & Gợi ý")
    st.dataframe(df_new)
