import streamlit as st
import os
from PIL import Image
import streamlit as st
import pandas as pd
import plotly.express as px

# ====================
# 1. THIẾT LẬP DỮ LIỆU
# ====================
segments = {
    0.0: {
        "label": "KHÁCH MỚI/THƯỜNG XUYÊN",
        "days": 82,
        "orders": 9,
        "spending": 68,
        "count": 1473,
        "color": "#4CAF50",
        "icon": "🛒",
        "description": "Khách mua đều đặn nhưng chi tiêu trung bình"
    },
    1.0: {
        "label": "KHÁCH VIP",
        "days": 94,
        "orders": 17,
        "spending": 160,
        "count": 926,
        "color": "#FF5722",
        "icon": "🎖️",
        "description": "Khách chi tiêu cao và mua thường xuyên"
    },
    2.0: {
        "label": "KHÁCH BÌNH THƯỜNG/MUA THEO MÙA",
        "days": 279,
        "orders": 8,
        "spending": 66,
        "count": 1008,
        "color": "#2196F3",
        "icon": "🌦️",
        "description": "Khách chỉ mua theo lịch"
    },
    3.0: {
        "label": "KHÁCH NGỪNG MUA",
        "days": 504,
        "orders": 5,
        "spending": 37,
        "count": 491,
        "color": "#9E9E9E",
        "icon": "💤",
        "description": "Khách không còn giao dịch trong 6 tháng"
    }
}

# ====================
# 2. GIAO DIỆN CHÍNH
# ====================
st.set_page_config(layout="wide", page_title="Phân Tích Khách Hàng", page_icon="🍎")
st.title("🍎 PHÂN TÍCH KHÁCH HÀNG CỬA HÀNG THỰC PHẨM")

# ----- Phần 1: Tổng quan -----
st.header("1. Tổng Quan Phân Khúc", divider="rainbow")

# Tính toán các chỉ số
total_customers = sum(data["count"] for data in segments.values())
vip_percentage = segments[1.0]["count"] / total_customers * 100
churned_percentage = segments[3.0]["count"] / total_customers * 100

# Hiển thị metrics
col1, col2, col3 = st.columns(3)
col1.metric("Tổng số khách hàng", f"{total_customers:,} KH")
col2.metric("Khách VIP", 
           f"{segments[1.0]['count']:,} KH", 
           f"{vip_percentage:.1f}%")
col3.metric("Khách ngừng mua", 
           f"{segments[3.0]['count']:,} KH", 
           f"{churned_percentage:.1f}%")

# ----- Phần 2: Chi tiết từng nhóm -----
st.header("2. Chi Tiết Từng Nhóm", divider="rainbow")

# Tạo 4 cột cho 4 nhóm
cols = st.columns(4)

for idx, (cluster, data) in enumerate(segments.items()):
    with cols[idx]:
        # Tạo container có border và màu sắc tương ứng
        container = st.container(border=True)
        
        # Header với icon và màu sắc
        container.markdown(
            f"<h3 style='color:{data['color']};text-align:center'>"
            f"{data['icon']} {data['label']}</h3>", 
            unsafe_allow_html=True
        )
        
        # Hiển thị các chỉ số
        container.metric("Số lượng", f"{data['count']:,} KH")
        container.metric("Lần cuối mua", f"{data['days']} ngày")
        container.metric("Số đơn TB", data['orders'])
        container.metric("Chi tiêu TB", f"${data['spending']}")
        
        # Mô tả ngắn
        container.caption(data["description"])

# ----- Phần 3: Trực quan hóa -----
st.header("3. Phân Bố Khách Hàng", divider="rainbow")

# Chuẩn bị dữ liệu cho biểu đồ
df = pd.DataFrame.from_dict(segments, orient='index')

# Biểu đồ Pie
fig_pie = px.pie(
    df, 
    values='count', 
    names='label',
    color='label',
    color_discrete_map={data['label']: data['color'] for data in segments.values()},
    hole=0.4,
    title="Tỷ lệ phân bố khách hàng"
)
fig_pie.update_traces(textposition='inside', textinfo='percent+label')

# Biểu đồ Radar so sánh 3 chỉ số RFM
fig_radar = px.line_polar(
    df.reset_index(), 
    r='spending', 
    theta='label',
    line_close=True,
    color_discrete_sequence=['#FF5722'],
    template="plotly_dark",
    title="So sánh mức chi tiêu giữa các nhóm"
)
fig_radar.update_traces(fill='toself')

# Hiển thị 2 biểu đồ cạnh nhau
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.plotly_chart(fig_pie, use_container_width=True)
with chart_col2:
    st.plotly_chart(fig_radar, use_container_width=True)

# ----- Phần 4: Chiến lược tiếp thị -----
st.header("4. Chiến Lược Tiếp Thị", divider="rainbow")

strategies = {
    "KHÁCH VIP": [
        "🎯 Combo cao cấp: Thịt bò Wagyu + Rượu vang hảo hạng",
        "💳 Thẻ thành viên VIP: Giảm 15% mọi đơn hàng",
        "🚚 Ưu tiên giao hàng trong 2 giờ",
        "🎁 Quà tặng đặc biệt dịp lễ tết"
    ],
    "KHÁCH THƯỜNG XUYÊN/MỚI": [
        "🔄 Chương trình tích điểm: 10 điểm = 1kg rau củ miễn phí",
        "📧 Gửi công thức nấu ăn hàng tuần",
        "🎁 Voucher $10 dịp sinh nhật",
        "📱 Ưu đãi đặc biệt khi đặt hàng qua App"
    ],
    "KHÁCH BÌNH THƯỜNG": [
        "🌧️ Ưu đãi theo mùa: Giảm 20% hải sản mùa mưa",
        "🍺 Combo bia + đồ nhậu cuối tuần",
        "📅 Nhắc lịch đặt hàng trước mùa cao điểm",
        "🎄 Combo đặc biệt dịp lễ"
    ],
    "KHÁCH NGỪNG MUA/RỜI BỎ": [
        "📞 Khảo sát qua điện thoại (tặng voucher $5)",
        "🔥 Ưu đãi comeback: Giảm 30% đơn đầu tiên",
        "💌 Email nhắc nhở với ưu đãi đặc biệt",
        "⏳ Ngừng tiếp thị nếu không phản hồi sau 3 tháng"
    ]
}

# Hiển thị chiến lược dưới dạng expander
for segment, action_list in strategies.items():
    with st.expander(f"{segment} {next(data['icon'] for data in segments.values() if data['label']==segment)}"):
        for action in action_list:
            st.markdown(f"- {action}")

# ====================
# 5. TÍNH NĂNG BỔ SUNG
# ====================
st.divider()

# Nút tải báo cáo
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Tải báo cáo đầy đủ (CSV)",
    data=csv,
    file_name='phan_khuc_khach_hang.csv',
    mime='text/csv',
    help="Tải về dữ liệu phân khúc khách hàng đầy đủ"
)

# Thông tin footer
st.caption("""
**Hướng dẫn sử dụng:**
- Nhấn vào từng nhóm khách hàng để xem chiến lược tiếp thị cụ thể
- Tải báo cáo để phân tích chi tiết hơn

""")
# Đường dẫn tới folder chứa ảnh
IMAGE_FOLDER = "pyspark"  # đổi lại nếu bạn dùng folder khác
# 1 vip 0 mới 3 rời 2 bình thường
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
