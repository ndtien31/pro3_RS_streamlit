import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Mapping cluster ID -> tên nhóm
cluster_labels = {
    3: "Khách hàng Rời bỏ",
    1: "Khách hàng Mới",
    0: "Khách hàng Bình thường",
    2: "Khách hàng VIP"
}

# Mapping chiến lược theo phân khúc
retention_strategies = {
    "Khách hàng Rời bỏ": "Gửi email giảm giá, khảo sát lý do rời đi, chăm sóc lại bằng voucher.",
    "Khách hàng Mới": "Gửi welcome email, giới thiệu sản phẩm hot, chính sách ưu đãi lần đầu.",
    "Khách hàng Bình thường": "Gửi bản tin định kỳ, chương trình tích điểm, gợi ý sản phẩm phù hợp.",
    "Khách hàng VIP": "Tặng quà tri ân, ưu đãi độc quyền, hỗ trợ nhanh chóng, tổ chức sự kiện riêng."
}

# Load model và scaler
@st.cache_resource
def load_model():
    import joblib
    data = joblib.load('rfm_clustering_model.pkl')
    return data['kmeans'], data['scaler']

model, scaler = load_model()

st.title("🔍 Dự đoán Phân khúc Khách hàng theo RFM")

st.write("Nhập thông tin cho 5 khách hàng:")

# Tạo form nhập dữ liệu
rfm_data = []
for i in range(5):
    st.subheader(f"Khách hàng {i+1}")
    recency = st.number_input(f"Recency (ngày) - KH {i+1}", min_value=0, value=30, key=f"r{i}")
    frequency = st.number_input(f"Frequency (số lần mua) - KH {i+1}", min_value=0, value=5, key=f"f{i}")
    monetary = st.number_input(f"Monetary (giá trị mua hàng) - KH {i+1}", min_value=0.0, value=1000.0, key=f"m{i}")
    rfm_data.append([recency, frequency, monetary])

if st.button("📊 Dự đoán cụm khách hàng"):
    rfm_df = pd.DataFrame(rfm_data, columns=["Recency", "Frequency", "Monetary"])
    rfm_scaled = scaler.transform(rfm_df)
    clusters = model.predict(rfm_scaled)

    st.subheader("🎯 Kết quả dự đoán:")
    rfm_df["Cụm"] = clusters
    rfm_df["Phân loại"] = rfm_df["Cụm"].map(cluster_labels)
    rfm_df["Chiến lược giữ chân"] = rfm_df["Phân loại"].map(retention_strategies)

    st.dataframe(rfm_df)
