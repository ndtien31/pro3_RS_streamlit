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
    data = joblib.load('rfm_clustering_model.pkl')
    return data['kmeans'], data['scaler']

# Load dữ liệu RFM và giao dịch + thống kê RFM
@st.cache_data
def load_data():
    df_rfm = pd.read_csv("rfm.csv")
    df_giaodich = pd.read_csv("data_th.csv")

    rfm_stats = {
        "recency_min": df_rfm["Recency"].min(),
        "recency_max": df_rfm["Recency"].max(),
        "frequency_min": df_rfm["Frequency"].min(),
        "frequency_max": df_rfm["Frequency"].max(),
        "monetary_min": df_rfm["Monetary"].min(),
        "monetary_max": df_rfm["Monetary"].max(),
    }

    return df_rfm, df_giaodich, rfm_stats

# Tải model và dữ liệu
model, scaler = load_model()
df_rfm, df_giaodich, rfm_stats = load_data()

# Tính giới hạn nhập
min_recency = max(0, rfm_stats["recency_min"] * 0.5)
max_recency = rfm_stats["recency_max"] * 1.5

min_frequency = max(0, rfm_stats["frequency_min"] * 0.5)
max_frequency = rfm_stats["frequency_max"] * 1.5

min_monetary = max(0, rfm_stats["monetary_min"] * 0.5)
max_monetary = rfm_stats["monetary_max"] * 1.5

# Giao diện Streamlit
st.title("🔍 Dự đoán Phân khúc Khách hàng theo RFM")

tab1, tab2 = st.tabs(["✍️ Nhập tay 5 khách hàng", "📁 Chọn khách hàng từ dữ liệu"])

# ====== TAB 1: NHẬP TAY ======
with tab1:
    st.write("Nhập thông tin RFM cho 5 khách hàng. (Giới hạn theo dữ liệu huấn luyện)")

    rfm_data = []
    for i in range(5):
        st.subheader(f"📌 Khách hàng {i+1}")
        st.markdown(f"""
        <div style='color:gray; font-size: 0.9em'>
        - Recency: {int(min_recency)} → {int(max_recency)}<br>
        - Frequency: {int(min_frequency)} → {int(max_frequency)}<br>
        - Monetary: {int(min_monetary)} → {int(max_monetary)}
        </div>
        """, unsafe_allow_html=True)

        recency = st.number_input(
            f"Recency (ngày) - KH {i+1}", 
            min_value=int(min_recency), 
            max_value=int(max_recency), 
            value=int((min_recency + max_recency) // 2), 
            key=f"r{i}"
        )

        frequency = st.number_input(
            f"Frequency (số lần mua) - KH {i+1}", 
            min_value=int(min_frequency), 
            max_value=int(max_frequency), 
            value=int((min_frequency + max_frequency) // 2), 
            key=f"f{i}"
        )

        monetary = st.number_input(
            f"Monetary (giá trị mua hàng) - KH {i+1}", 
            min_value=float(min_monetary), 
            max_value=float(max_monetary), 
            value=float((min_monetary + max_monetary) / 2), 
            key=f"m{i}"
        )

        rfm_data.append([recency, frequency, monetary])

    if st.button("📊 Dự đoán cụm khách hàng", key="btn_predict_5"):
        rfm_df = pd.DataFrame(rfm_data, columns=["Recency", "Frequency", "Monetary"])
        rfm_scaled = scaler.transform(rfm_df)
        clusters = model.predict(rfm_scaled)

        st.subheader("🎯 Kết quả dự đoán:")
        rfm_df["Cụm"] = clusters
        rfm_df["Phân loại"] = rfm_df["Cụm"].map(cluster_labels)
        rfm_df["Chiến lược giữ chân"] = rfm_df["Phân loại"].map(retention_strategies)

        st.dataframe(rfm_df)

# ====== TAB 2: CHỌN KHÁCH HÀNG TỪ DỮ LIỆU ======
with tab2:
    st.write("Chọn 1 trong 10 khách hàng đầu tiên từ tập dữ liệu để xem phân tích chi tiết.")

    top_10_customers = df_rfm.head(10)
    customer_list = top_10_customers["Member_number"].tolist()
    selected_customer = st.selectbox("🧑‍💼 Chọn khách hàng", customer_list)

    if selected_customer:
        customer_info = df_rfm[df_rfm["Member_number"] == selected_customer]
        rfm_values = customer_info[["Recency", "Frequency", "Monetary"]]
        scaled = scaler.transform(rfm_values)
        cluster = model.predict(scaled)[0]
        label = cluster_labels[cluster]
        strategy = retention_strategies[label]

        st.subheader("📌 Thông tin RFM:")
        st.write(customer_info)

        st.subheader("📦 Giao dịch chi tiết:")
        giao_dich = df_giaodich[df_giaodich["Member_number"] == selected_customer]
        st.dataframe(giao_dich)

        st.subheader("🔮 Phân loại & Gợi ý chiến lược:")
        st.markdown(f"""
        - **Phân loại:** `{label}`  
        - **Chiến lược giữ chân:** {strategy}
        """)
