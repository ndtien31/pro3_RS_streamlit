import streamlit as st
import os
from PIL import Image

# Đường dẫn tới folder chứa ảnh
IMAGE_FOLDER = "pyspark"  # đổi lại nếu bạn dùng folder khác

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
