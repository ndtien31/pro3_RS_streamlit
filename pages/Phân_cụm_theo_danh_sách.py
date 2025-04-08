import streamlit as st
import pandas as pd
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
    data = joblib.load('rfm_clustering_model.pkl')
    return data['kmeans'], data['scaler']

model, scaler = load_model()

st.title("📁 Dự đoán Phân khúc Khách hàng từ File RFM")

# 👉 File mẫu
sample_data = pd.DataFrame({
    "Recency": [30, 7, 90, 10, 45],
    "Frequency": [5, 15, 2, 20, 4],
    "Monetary": [1200, 8000, 500, 15000, 950]
})

csv_sample = sample_data.to_csv(index=False).encode('utf-8-sig')
st.download_button("📥 Tải file mẫu RFM (.csv)", data=csv_sample, file_name="rfm_sample.csv", mime="text/csv")

st.markdown("---")

# Upload dữ liệu
uploaded_file = st.file_uploader("Tải lên file Excel hoặc CSV chứa dữ liệu RFM", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            rfm_df = pd.read_csv(uploaded_file)
        else:
            rfm_df = pd.read_excel(uploaded_file)

        expected_cols = {"Recency", "Frequency", "Monetary"}
        if not expected_cols.issubset(rfm_df.columns):
            st.error("❌ File phải có đủ 3 cột: Recency, Frequency, Monetary")
        else:
            st.success("✅ Dữ liệu đã được tải thành công!")
            st.write("📄 Dữ liệu đầu vào:")
            st.dataframe(rfm_df)

            # Chuẩn hóa và dự đoán
            rfm_scaled = scaler.transform(rfm_df[["Recency", "Frequency", "Monetary"]])
            clusters = model.predict(rfm_scaled)

            # Kết quả
            rfm_df["Cụm"] = clusters
            rfm_df["Phân loại"] = rfm_df["Cụm"].map(cluster_labels)
            rfm_df["Chiến lược giữ chân"] = rfm_df["Phân loại"].map(retention_strategies)

            st.subheader("🎯 Kết quả phân cụm & chiến lược:")
            st.dataframe(rfm_df)

            # Tải kết quả
            result_csv = rfm_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("⬇️ Tải kết quả CSV", data=result_csv, file_name="rfm_result.csv", mime='text/csv')

    except Exception as e:
        st.error(f"❌ Lỗi xử lý file: {e}")
