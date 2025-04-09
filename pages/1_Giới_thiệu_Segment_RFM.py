import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Giới Thiệu Segment RFM",
    page_icon="🛒",
    layout="wide"
)

# Tiêu đề
st.title("🛒 Ứng Dụng Phân Khúc Khách Hàng RFM Cho Cửa Hàng Thực Phẩm")

st.markdown("""
## Giới Thiệu Bài Toán Segment RFM

RFM (Recency, Frequency, Monetary) là một mô hình phân khúc khách hàng cực kỳ hiệu quả 
trong lĩnh vực bán lẻ, đặc biệt là với các cửa hàng thực phẩm như rau củ quả, thịt cá, bia rượu.
""")

# Phần 1: RFM là gì?
st.header("1. RFM Là Gì?")
st.markdown("""
- **Recency (Độ mới)**: Thời gian kể từ lần mua hàng cuối cùng của khách
- **Frequency (Tần suất)**: Số lần mua hàng trong một khoảng thời gian
- **Monetary (Giá trị)**: Tổng số tiền khách hàng đã chi tiêu

Bằng cách phân tích 3 yếu tố này, chúng ta có thể phân loại khách hàng thành các nhóm có hành vi mua sắm khác nhau.
""")

# Phần 2: Tại sao RFM quan trọng với cửa hàng thực phẩm?
st.header("2. Tại Sao RFM Quan Trọng Với Cửa Hàng Thực Phẩm?")
st.markdown("""
Đối với cửa hàng rau củ quả, thịt cá, bia rượu.....:
- Khách hàng thường mua sắm theo thói quen và có tính lặp lại cao
- Giá trị mỗi đơn hàng thường không quá lớn nhưng tần suất quan trọng
- Dễ dàng xác định khách hàng trung thành vs khách hàng có nguy cơ rời bỏ
- Giúp tối ưu hóa chiến dịch marketing và chương trình khuyến mãi
""")

# Phần 3: Các phân khúc RFM điển hình
st.header("3. Các Phân Khúc RFM Điển Hình")
st.markdown("""
Với mỗi chỉ số RFM, chúng ta thường chia thành 3-5 mức độ (ví dụ: 1-5 điểm). 
Kết hợp 3 chỉ số sẽ tạo ra các phân khúc như:

| Phân Khúc       | Đặc Điểm                                                                 | Chiến Lược Ứng Dụng |
|------------------|--------------------------------------------------------------------------|---------------------|
| **Kim Cương**    | Mua gần đây, thường xuyên, chi tiêu nhiều (R cao, F cao, M cao)          | Ưu tiên giữ chân   |
| **Tiềm Năng**    | Chi tiêu nhiều nhưng ít mua gần đây (R thấp, F trung bình, M cao)        | Kích hoạt lại      |
| **Trung Thành**   | Mua thường xuyên nhưng giá trị thấp (R cao, F cao, M thấp)                | Tăng giá trị đơn hàng |
| **Nguy Cơ**      | Lâu không mua, tần suất thấp (R thấp, F thấp, M trung bình)              | Ưu đãi đặc biệt    |
| **Mới**          | Mua gần đây nhưng chưa rõ tần suất và giá trị (R cao, F thấp, M thấp)    | Chăm sóc đặc biệt  |
""")
st.markdown("""### Hoặc dùng các model để phân cụm khách hàng tự động dựa vào các chỉ số RFM""")
# Phần 4: Lợi ích khi áp dụng RFM
st.header("4. Lợi Ích Khi Áp Dụng RFM")
st.markdown("""
- **Tăng doanh thu**: Tập trung vào nhóm khách hàng có tiềm năng nhất
- **Tiết kiệm chi phí**: Giảm chi cho các khách hàng ít có khả năng quay lại
- **Cá nhân hóa**: Gửi các ưu đãi phù hợp với từng nhóm khách hàng
- **Giữ chân khách**: Nhận biết sớm khách hàng có nguy cơ rời bỏ
- **Tối ưu hàng tồn**: Dự đoán nhu cầu theo từng nhóm khách hàng
""")

# Kết luận
st.header("Kết Luận")
st.success("""
Phân khúc RFM là công cụ mạnh mẽ giúp cửa hàng thực phẩm hiểu rõ hơn về tập khách hàng của mình, 
từ đó đưa ra các chiến lược kinh doanh và marketing hiệu quả, tăng doanh thu và lợi nhuận.
""")

st.markdown("---")
st.caption("© 2025 Ứng Dụng Phân Tích Khách Hàng - Dành cho cửa hàng rau củ quả, thịt cá, bia rượu")