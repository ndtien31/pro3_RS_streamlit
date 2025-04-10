import streamlit as st
import os
from PIL import Image
import streamlit as st

st.subheader("🎯 Phân Tích Nhóm Khách Hàng Theo RFM")
st.write("Phân tích dựa trên 3,898 khách hàng:")

# Định nghĩa các nhóm với tên gọi trực quan
cluster_data = {
    2: {"name": "KHÁCH VIP (Top 12%)", "desc": "🔸 Mua 19 đơn/gần nhất 89 ngày 🔸 Chi $189/đơn", "action": "🎖️ Tặng voucher mua hàng cao cấp"},
    0: {"name": "KHÁCH QUEN", "desc": "🔸 Mua 12 đơn/gần nhất 124 ngày 🔸 Chi $108/đơn", "action": "🛒 Combo tích điểm 'Mua 9 tặng 1' cho rau củ"},
    1: {"name": "KHÁCH MỚI TIỀM NĂNG", "desc": "🔸 Mua 6 đơn/gần nhất 127 ngày 🔸 Chi $50/đơn", "action": "🌱 Gói chào mừng giảm 30% đơn đầu"},
    3: {"name": "KHÁCH NGỪNG MUA", "desc": "🔸 Không mua 433 ngày 🔸 Chỉ 5 đơn", "action": "🚫 Khảo sát qua SMS kèm quà tặng"}
}

# Hiển thị metrics
col1, col2 = st.columns(2)
with col1:
    st.metric(label=f"**{cluster_data[2]['name']}**", value="484 KH", help=cluster_data[2]['desc'])
    st.metric(label=f"**{cluster_data[0]['name']}**", value="1,266 KH", help=cluster_data[0]['desc'])
with col2:
    st.metric(label=f"**{cluster_data[1]['name']}**", value="1,293 KH", help=cluster_data[1]['desc'])
    st.metric(label=f"**{cluster_data[3]['name']}**", value="855 KH", help=cluster_data[3]['desc'])

# Hiển thị chiến lược
st.success("🚀 **Chiến lược tiếp thị:**")
for cluster in [2, 0, 1, 3]:
    st.markdown(f"**{cluster_data[cluster]['name']}**  \n{cluster_data[cluster]['action']}")

# Visual phân bố
st.progress(100)
st.caption(
    f"Phân bố khách hàng: "
    f"{cluster_data[2]['name']} 12% | "
    f"{cluster_data[0]['name']} 32% | "
    f"{cluster_data[1]['name']} 33% | "
    f"{cluster_data[3]['name']} 22%"
)
IMAGE_FOLDER = "images_ml"  # đổi lại nếu bạn dùng folder khác

# Hiển thị tiêu đề
st.title("CÁC BIỂU ĐỒ:")

# Lấy danh sách file ảnh từ folder
if os.path.exists(IMAGE_FOLDER):
    image_files = [f for f in os.listdir(IMAGE_FOLDER)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    image_files.sort()

    if image_files:
        for img_file in image_files:
            img_path = os.path.join(IMAGE_FOLDER, img_file)
            image = Image.open(img_path)
            st.markdown(f"### 📁 {img_file}")
            st.image(image, use_column_width=True)
    else:
        st.warning("Không tìm thấy file ảnh trong thư mục.")
else:
    st.error(f"Thư mục `{IMAGE_FOLDER}` không tồn tại.")
