import streamlit as st
import os
from PIL import Image
import streamlit as st

st.subheader("📊 Kết quả phân khúc RFM")
st.write("Dựa trên lịch sử mua hàng, khách hàng được chia thành 4 nhóm chính:")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="**Nhóm Ưu Tiên (Cluster 2)**", value="484 KH", 
             help=f"Chi tiêu cao nhất ({'$189/đơn'}), mua thường xuyên (19 đơn) và gần đây (89 ngày).")
    st.metric(label="**Nhóm Trung Thành (Cluster 0)**", value="1,266 KH", 
             help="Mua hàng rất thường xuyên (12 đơn) nhưng chi tiêu trung bình ($108).")

with col2:
    st.metric(label="**Nhóm Mới Giảm Sút (Cluster 1)**", value="1,293 KH", 
             help="Ít mua gần đây (127 ngày), tần suất thấp (6 đơn), cần kích hoạt lại.")
    st.metric(label="**Nhóm Ngủ Đông (Cluster 3)**", value="855 KH", 
             help="Không mua từ lâu (433 ngày), ít đơn (5 đơn), có thể loại bỏ khỏi CRM.")

st.warning("💡 **Gợi ý hành động:**")
st.write("""
- **Cluster 2 (Ưu tiên):** Tặng voucher bia/rượu cao cấp hoặc combo thịt cá đắt tiền.  
- **Cluster 0 (Trung thành):** Ưu đãi tích điểm đổi quà để tăng chi tiêu.  
- **Cluster 1 (Giảm sút):** Gửi email giảm giá 20% rau củ quả để kéo về.  
- **Cluster 3 (Ngủ đông):** Khảo sát lý do hoặc ngừng tiếp thị nếu không hiệu quả.
""")
# Đường dẫn tới folder chứa ảnh
IMAGE_FOLDER = "images_ml"  # đổi lại nếu bạn dùng folder khác

# Hiển thị tiêu đề
st.title("Hiển thị ảnh từ thư mục")

# Lấy danh sách file ảnh từ folder
if os.path.exists(IMAGE_FOLDER):
    image_files = [f for f in os.listdir(IMAGE_FOLDER)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

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
