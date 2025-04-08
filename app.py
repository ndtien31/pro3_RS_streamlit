# Home.py
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Ứng Dụng MYSHOPE",
    page_icon="🏠",
    layout="centered"
)

# Nội dung trang chủ
st.title("Chào Mừng Đến Với Ứng Dụng MYSHOPE")
st.image("https://via.placeholder.com/800x200?text=Welcome+Banner", use_column_width=True)

st.markdown("""
## Giới Thiệu MYSHOPE.

## Hướng Dẫn Sử Dụng
1. Chọn trang bạn muốn từ thanh điều hướng bên trái
2. Mỗi trang có chức năng riêng
3. Có thể quay lại trang chủ bất cứ lúc nào

## Các Trang Chính
- 📊 Trang Thống Kê: Xem các báo cáo thống kê
- 📈 Trang Phân Tích: Phân tích dữ liệu
- 🔧 Trang Cài Đặt: Cấu hình ứng dụng
""")

# Thêm footer  git init
st.divider()
st.caption("© 2025 Bản quyền thuộc về tác giả.")