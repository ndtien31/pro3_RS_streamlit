import streamlit as st
import pandas as pd
import numpy as np
import joblib
# Giao diện Streamlit
st.set_page_config(page_title="Phân khúc khách hàng RFM", layout="wide")
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
    rfm = pd.read_csv("rfm.csv")
    data_th = pd.read_csv("data_th.csv")

    rfm_stats = {
        "recency_min": rfm["Recency"].min() * 0.5,
        "recency_max": rfm["Recency"].max() * 1.5,
        "frequency_min": rfm["Frequency"].min() * 0.5,
        "frequency_max": rfm["Frequency"].max() * 1.5,
        "monetary_min": rfm["Monetary"].min() * 0.5,
        "monetary_max": rfm["Monetary"].max() * 1.5,
    }

    return rfm, data_th, rfm_stats

# Tải model và dữ liệu
model, scaler = load_model()
rfm, data_th, rfm_stats = load_data()


st.title("🔍 Dự đoán Phân khúc Khách hàng theo RFM")

tab1, tab2 = st.tabs(["✍️ Nhập tay 5 khách hàng", "📁 Chọn khách hàng từ dữ liệu"])

# ====== TAB 1: NHẬP TAY BẰNG SLIDER ======
with tab1:
    st.write("Nhập thông tin RFM cho 5 khách hàng (dùng thanh trượt).")

    rfm_data = []
    for i in range(5):
        st.subheader(f"📌 Khách hàng {i+1}")
        st.markdown(f"""
        <div style='color:gray; font-size: 0.9em'>
        - Recency: {int(rfm_stats['recency_min'])} → {int(rfm_stats['recency_max'])}<br>
        - Frequency: {int(rfm_stats['frequency_min'])} → {int(rfm_stats['frequency_max'])}<br>
        - Monetary: {int(rfm_stats['monetary_min'])} → {int(rfm_stats['monetary_max'])}
        </div>
        """, unsafe_allow_html=True)

        recency = st.slider(
            f"Recency (ngày) - KH {i+1}",
            min_value=int(rfm_stats['recency_min']),
            max_value=int(rfm_stats['recency_max']),
            value=int((rfm_stats['recency_min'] + rfm_stats['recency_max']) // 2),
            key=f"r{i}"
        )

        frequency = st.slider(
            f"Frequency (số lần mua) - KH {i+1}",
            min_value=int(rfm_stats['frequency_min']),
            max_value=int(rfm_stats['frequency_max']),
            value=int((rfm_stats['frequency_min'] + rfm_stats['frequency_max']) // 2),
            key=f"f{i}"
        )

        monetary = st.slider(
            f"Monetary (giá trị mua hàng) - KH {i+1}",
            min_value=int(rfm_stats['monetary_min']),
            max_value=int(rfm_stats['monetary_max']),
            value=int((rfm_stats['monetary_min'] + rfm_stats['monetary_max']) // 2),
            key=f"m{i}"
        )

        rfm_data.append([recency, frequency, monetary])

    if st.button("📊 Dự đoán cụm khách hàng", key="btn_predict_5"):
        rfm_df = pd.DataFrame(rfm_data, columns=["Recency", "Frequency", "Monetary"])
        rfm_scaled = scaler.transform(rfm_df)
        clusters = model.predict(rfm_scaled)

        rfm_df["Cụm"] = clusters
        rfm_df["Phân loại"] = rfm_df["Cụm"].map(cluster_labels)
        rfm_df["Chiến lược giữ chân"] = rfm_df["Phân loại"].map(retention_strategies)

        st.subheader("🎯 Kết quả dự đoán:")
        st.dataframe(rfm_df)

# ====== TAB 2: CHỌN KHÁCH HÀNG TỪ DỮ LIỆU ======
with tab2:
    st.write("Chọn 1 trong 10 khách hàng đầu tiên từ tập dữ liệu để xem phân tích chi tiết.")

    top_10_members = rfm.head(10)
    member_list = top_10_members["Member_number"].tolist()
    selected_member = st.selectbox("🧑‍💼 Chọn khách hàng", member_list)

    if selected_member:
        member_info = rfm[rfm["Member_number"] == selected_member]
        rfm_values = member_info[["Recency", "Frequency", "Monetary"]]
        scaled = scaler.transform(rfm_values)
        cluster = model.predict(scaled)[0]
        label = cluster_labels[cluster]
        strategy = retention_strategies[label]

        st.subheader("📌 Thông tin RFM:")
        st.write(member_info)

        st.subheader("📦 Giao dịch chi tiết:")
        giao_dich = data_th[data_th["Member_number"] == selected_member]
        st.dataframe(giao_dich)

        st.subheader("🔮 Phân loại & Gợi ý chiến lược:")
        st.markdown(f"""
        - **Phân loại:** `{label}`  
        - **Chiến lược giữ chân:** {strategy}
        """)
