import streamlit as st
import pandas as pd
import numpy as np
import json
from io import StringIO
from scipy.spatial.distance import euclidean

# Load centroids và scaler
with open("pyspark/centroids.json", "r") as f:
    centroids = np.array(json.load(f))

with open("pyspark/scaler_minmax.json", "r") as f:
    scaler = json.load(f)
    min_vals = np.array(scaler["min"])
    max_vals = np.array(scaler["max"])

# Hàm scale dữ liệu
def minmax_scale(row, min_vals, max_vals):
    return (row - min_vals) / (max_vals - min_vals + 1e-8)

# Dự đoán cụm
def predict_cluster(point, centroids):
    distances = [euclidean(point, center) for center in centroids]
    return int(np.argmin(distances))

# Gợi ý cho từng cụm
cluster_suggestions = {
    1: "🟢 Nhóm tiềm năng cao - nên tập trung upsell hoặc giữ chân.",
    2: "🟡 Nhóm bình thường - có thể nuôi dưỡng thêm.",
    3: "🔴 Nhóm có giá trị thấp - cân nhắc chiến dịch khuyến mãi.",
    0: "🔵 Nhóm mới hoặc chưa rõ hành vi - nên theo dõi thêm.",
}

# Giao diện chính
st.title("📊 Dự đoán phân cụm khách hàng RFM (KMeans)")

st.markdown("### 📥 Bước 1: Tải file CSV mẫu")
csv_template = "Recency,Frequency,Monetary\n10,5,100\n30,2,40\n7,8,300\n15,4,120\n90,1,20"
st.download_button(
    label="⬇️ Tải file mẫu (.csv)",
    data=csv_template,
    file_name="rfm_template.csv",
    mime="text/csv"
)

st.markdown("### 📤 Bước 2: Tải lên file bạn đã điền")
uploaded_file = st.file_uploader("📁 Chọn file CSV", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("📋 Dữ liệu bạn đã tải lên:")
        st.dataframe(df)

        if st.button("🔍 Dự đoán cụm"):
            # Scale dữ liệu
            scaled_data = df.apply(lambda row: minmax_scale(np.array(row), min_vals, max_vals), axis=1)
            scaled_data = np.vstack(scaled_data)

            # Dự đoán cụm
            clusters = [predict_cluster(x, centroids) for x in scaled_data]
            df["Cluster"] = clusters
            df["Gợi ý hành động"] = df["Cluster"].apply(lambda x: cluster_suggestions.get(x, "Không xác định"))

            st.success("✅ Đã phân cụm xong!")
            st.markdown("### 📈 Kết quả phân cụm và gợi ý:")
            st.dataframe(df)

            # Cho tải kết quả về
            csv_result = df.to_csv(index=False).encode("utf-8")
            st.download_button("📤 Tải kết quả về", csv_result, file_name="rfm_cluster_result.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Lỗi khi xử lý file: {e}")
