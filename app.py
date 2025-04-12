# Home.py
import streamlit as st
# https://pro3rsapp-5mtc9l6ey9fgkhr73dbca9.streamlit.app/
# Cấu hình trang
st.set_page_config(
    page_title="Ứng Dụng SEGMENT CUSTOMER",
    page_icon="🏠",
    layout="centered"
)

# Nội dung trang chủ
st.title("Chào Mừng Đến Với Ứng Dụng SEGMENT CUSTOMER")
st.image("image_tt.png", use_column_width=True)

st.markdown("""
## Giới Thiệu SEGMENT CUSTOMER.

## Hướng Dẫn Sử Dụng
1. Chọn chức năng bạn muốn từ thanh điều hướng bên trái
2. ứng dụng có 2 phần: Machine learning và Machine learning Pyspark
3. Có thể quay lại trang chủ bất cứ lúc nào
""")
st.markdown("""
###- Khóa học:               Đồ án Tốt nghiệp Data Science
###- Mã lớp:                   DL07_302T37_ON            
## Thành viên nhóm:
1. Ngô Duy Tiến
2. Phạm Quốc Bình
Ngày BC: 12/04/2025            
""")
# Thêm footer  git init
st.divider()
st.caption("© 2025 Bản quyền thuộc về tác giả.")