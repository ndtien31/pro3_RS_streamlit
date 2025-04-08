# Home.py
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Ứng Dụng SEGMENT CUSTOMER",
    page_icon="🏠",
    layout="centered"
)

# Nội dung trang chủ
st.title("Chào Mừng Đến Với Ứng Dụng SEGMENT CUSTOMER")
st.image("https://via.placeholder.com/800x200?text=Welcome+Banner", use_column_width=True)

st.markdown("""
## Giới Thiệu MYSHOPE.

## Hướng Dẫn Sử Dụng
1. Chọn trang bạn muốn từ thanh điều hướng bên trái
2. Mỗi trang có chức năng riêng
3. Có thể quay lại trang chủ bất cứ lúc nào
""")

# Thêm footer  git init
st.divider()
st.caption("© 2025 Bản quyền thuộc về tác giả.")