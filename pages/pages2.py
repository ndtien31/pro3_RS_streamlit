import streamlit as st
import pandas as pd
import os
import shutil
from datetime import datetime
from PIL import Image

# ============================================
# CẤU HÌNH HỆ THỐNG
# ============================================
DATA_FILE = "products.csv"
IMAGE_FOLDER = "product_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Danh mục sản phẩm
CATEGORIES = [
    "Điện thoại", "Laptop", "Tablet", "Tai nghe", 
    "Loa", "Smartwatch", "Phụ kiện", "Đồ gia dụng"
]

# ============================================
# KHỞI TẠO DỮ LIỆU MẪU VỚI HÌNH ẢNH THỰC TẾ
# ============================================
def init_sample_images():
    """Copy ảnh mẫu từ thư mục sample_images nếu chưa có"""
    sample_images = {
        "iphone13.jpg": "https://cdn.tgdd.vn/Products/Images/42/223602/iphone-13-1-1.jpg",
        "samsung_s21.jpg": "https://cdn.tgdd.vn/Products/Images/42/226935/samsung-galaxy-s21-ultra-1-1.jpg",
        "xiaomi_note10.jpg": "https://cdn.tgdd.vn/Products/Images/42/222912/xiaomi-redmi-note-10-5g-xanh-1-1.jpg",
        "macbook_air.jpg": "https://cdn.tgdd.vn/Products/Images/44/231244/macbook-air-m1-2020-gray-1-1.jpg",
        "airpods_pro.jpg": "https://cdn.tgdd.vn/Products/Images/54/236768/airpods-pro-2-2022-1-1.jpg"
    }
    
    for filename, url in sample_images.items():
        dest_path = os.path.join(IMAGE_FOLDER, filename)
        if not os.path.exists(dest_path):
            try:
                img = Image.open(requests.get(url, stream=True).raw)
                img.save(dest_path)
            except:
                pass

def init_data():
    if not os.path.exists(DATA_FILE):
        init_sample_images()
        
        sample_data = {
            "ID": [1, 2, 3, 4, 5],
            "Tên sản phẩm": [
                "iPhone 13 128GB", 
                "Samsung Galaxy S21 Ultra", 
                "Xiaomi Redmi Note 10 5G",
                "MacBook Air M1 2020",
                "AirPods Pro 2"
            ],
            "Loại": ["Điện thoại", "Điện thoại", "Điện thoại", "Laptop", "Tai nghe"],
            "Giá": [19990000, 24990000, 5990000, 23990000, 5990000],
            "Số lượng": [15, 8, 25, 12, 30],
            "Mô tả": [
                "iPhone 13 128GB - Chip A15 Bionic mạnh mẽ, camera kép 12MP, màn hình Super Retina XDR 6.1 inch",
                "Samsung Galaxy S21 Ultra 5G - Camera 108MP, màn hình Dynamic AMOLED 2X 6.8 inch, bút S Pen hỗ trợ",
                "Xiaomi Redmi Note 10 5G - Hiệu năng ổn định, màn hình 90Hz, pin 5000mAh, giá tốt",
                "MacBook Air M1 - Chip Apple M1, RAM 8GB, SSD 256GB, màn hình Retina 13.3 inch, thời lượng pin 18 giờ",
                "AirPods Pro 2 - Chống ồn chủ động, chất âm tuyệt vời, thiết kế nhỏ gọn, sạc không dây MagSafe"
            ],
            "Ngày nhập": ["2023-01-15", "2023-02-20", "2023-03-10", "2023-04-05", "2023-05-12"],
            "Ảnh": ["iphone13.jpg", "samsung_s21.jpg", "xiaomi_note10.jpg", "macbook_air.jpg", "airpods_pro.jpg"],
            "Đánh giá": [4.8, 4.7, 4.5, 4.9, 4.6]
        }
        df = pd.DataFrame(sample_data)
        df.to_csv(DATA_FILE, index=False)

# ============================================
# CÁC HÀM TIỆN ÍCH
# ============================================
def load_data():
    df = pd.read_csv(DATA_FILE)
    df['Ảnh'] = df['Ảnh'].fillna('').astype(str)
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def generate_id(df):
    return df["ID"].max() + 1 if not df.empty else 1

def save_uploaded_image(uploaded_file, product_id):
    if uploaded_file is not None:
        try:
            # Xóa ảnh cũ nếu tồn tại
            for ext in ['.jpg', '.jpeg', '.png']:
                old_path = os.path.join(IMAGE_FOLDER, f"{product_id}{ext}")
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            # Lưu ảnh mới
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            filename = f"{product_id}{file_ext}"
            filepath = os.path.join(IMAGE_FOLDER, filename)
            
            img = Image.open(uploaded_file)
            img.save(filepath)
            return filename
        except Exception as e:
            st.error(f"Lỗi khi lưu ảnh: {e}")
            return ""
    return ""

def display_image(image_path, width=200):
    try:
        image_path = str(image_path).strip()
        if image_path and os.path.exists(os.path.join(IMAGE_FOLDER, image_path)):
            img = Image.open(os.path.join(IMAGE_FOLDER, image_path))
            st.image(img, width=width)
        else:
            st.image("https://via.placeholder.com/300?text=No+Image", width=width)
    except Exception as e:
        st.error(f"Lỗi khi hiển thị ảnh: {e}")
        st.image("https://via.placeholder.com/300?text=Error", width=width)

# ============================================
# GIAO DIỆN HIỂN THỊ SẢN PHẨM
# ============================================
def display_product_card(product, cols=3):
    with st.container():
        st.markdown(f"### {product['Tên sản phẩm']}")
        display_image(product['Ảnh'], width=250)
        
        # Hiển thị rating bằng stars
        stars = "⭐" * int(product['Đánh giá']) + "☆" * (5 - int(product['Đánh giá']))
        st.caption(f"{stars} {product['Đánh giá']}/5")
        
        st.markdown(f"**Giá:** {product['Giá']:,.0f} VND")
        st.markdown(f"**Tồn kho:** {product['Số lượng']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Xem chi tiết", key=f"view_{product['ID']}"):
                st.session_state['view_product'] = product['ID']
        with col2:
            if st.button("Thêm vào giỏ", key=f"cart_{product['ID']}"):
                if 'cart' not in st.session_state:
                    st.session_state['cart'] = []
                st.session_state['cart'].append(product['ID'])
                st.success(f"Đã thêm {product['Tên sản phẩm']} vào giỏ hàng!")

def display_products_grid(df, cols=3):
    columns = st.columns(cols)
    for idx, product in df.iterrows():
        with columns[idx % cols]:
            display_product_card(product)

def display_product_detail(product_id, df):
    product = df[df["ID"] == product_id].iloc[0]
    
    st.button("← Quay lại danh sách", on_click=lambda: st.session_state.pop('view_product'))
    
    col1, col2 = st.columns([1, 2])
    with col1:
        display_image(product["Ảnh"], width=400)
    with col2:
        st.markdown(f"# {product['Tên sản phẩm']}")
        
        # Hiển thị rating
        stars = "⭐" * int(product['Đánh giá']) + "☆" * (5 - int(product['Đánh giá']))
        st.markdown(f"**Đánh giá:** {stars} {product['Đánh giá']}/5")
        
        st.markdown(f"**Loại:** {product['Loại']}")
        st.markdown(f"**Giá:** {product['Giá']:,.0f} VND")
        st.markdown(f"**Số lượng tồn kho:** {product['Số lượng']}")
        st.markdown(f"**Ngày nhập:** {product['Ngày nhập']}")
        
        if st.button("Thêm vào giỏ hàng", type="primary"):
            if 'cart' not in st.session_state:
                st.session_state['cart'] = []
            st.session_state['cart'].append(product['ID'])
            st.success(f"Đã thêm {product['Tên sản phẩm']} vào giỏ hàng!")
        
        st.markdown("### Mô tả sản phẩm")
        st.write(product["Mô tả"])
    
    # Thêm các sản phẩm cùng loại
    st.markdown("### Sản phẩm tương tự")
    similar_products = df[(df["Loại"] == product["Loại"]) & (df["ID"] != product["ID"])]
    if not similar_products.empty:
        display_products_grid(similar_products)
    else:
        st.info("Hiện không có sản phẩm cùng loại")

# ============================================
# CÁC CHỨC NĂNG QUẢN LÝ
# ============================================
def add_product_form(df):
    with st.form("add_form", clear_on_submit=True):
        st.subheader("Thêm sản phẩm mới")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Tên sản phẩm*", placeholder="iPhone 15 Pro Max")
            category = st.selectbox("Danh mục*", CATEGORIES)
            price = st.number_input("Giá bán*", min_value=0, step=100000, format="%d")
        with col2:
            quantity = st.number_input("Số lượng*", min_value=0, step=1)
            image = st.file_uploader("Ảnh sản phẩm*", type=["jpg", "jpeg", "png"])
            rating = st.slider("Đánh giá", 1.0, 5.0, 4.0, 0.1)
        
        description = st.text_area("Mô tả chi tiết*", height=150)
        date = st.date_input("Ngày nhập*", datetime.now())
        
        submitted = st.form_submit_button("Thêm sản phẩm", type="primary")
        
        if submitted:
            if not all([name, description, image]):
                st.error("Vui lòng điền đầy đủ các trường bắt buộc (*)")
            else:
                new_id = generate_id(df)
                image_filename = save_uploaded_image(image, new_id)
                
                new_product = {
                    "ID": new_id,
                    "Tên sản phẩm": name,
                    "Loại": category,
                    "Giá": price,
                    "Số lượng": quantity,
                    "Mô tả": description,
                    "Ngày nhập": date.strftime("%Y-%m-%d"),
                    "Ảnh": image_filename,
                    "Đánh giá": rating
                }
                
                df = pd.concat([df, pd.DataFrame([new_product])], ignore_index=True)
                save_data(df)
                st.success("✅ Sản phẩm đã được thêm thành công!")
                st.balloons()
                st.experimental_rerun()

def update_product_form(df):
    st.subheader("Cập nhật sản phẩm")
    selected_id = st.selectbox("Chọn sản phẩm cần cập nhật", df["ID"].values)
    product = df[df["ID"] == selected_id].iloc[0]
    
    with st.form("update_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Tên sản phẩm*", product["Tên sản phẩm"])
            new_category = st.selectbox(
                "Danh mục*", 
                CATEGORIES,
                index=CATEGORIES.index(product["Loại"]))
            new_price = st.number_input("Giá bán*", min_value=0, value=product["Giá"], step=100000, format="%d")
        with col2:
            new_quantity = st.number_input("Số lượng*", min_value=0, value=product["Số lượng"])
            new_image = st.file_uploader("Cập nhật ảnh", type=["jpg", "jpeg", "png"])
            new_rating = st.slider("Đánh giá", 1.0, 5.0, float(product["Đánh giá"]), 0.1)
        
        new_description = st.text_area("Mô tả chi tiết*", product["Mô tả"], height=150)
        new_date = st.date_input("Ngày nhập*", datetime.strptime(product["Ngày nhập"], "%Y-%m-%d"))
        
        submitted = st.form_submit_button("Cập nhật", type="primary")
        
        if submitted:
            if not all([new_name, new_description]):
                st.error("Vui lòng điền đầy đủ các trường bắt buộc (*)")
            else:
                # Cập nhật thông tin cơ bản
                df.loc[df["ID"] == selected_id, "Tên sản phẩm"] = new_name
                df.loc[df["ID"] == selected_id, "Loại"] = new_category
                df.loc[df["ID"] == selected_id, "Giá"] = new_price
                df.loc[df["ID"] == selected_id, "Số lượng"] = new_quantity
                df.loc[df["ID"] == selected_id, "Mô tả"] = new_description
                df.loc[df["ID"] == selected_id, "Ngày nhập"] = new_date.strftime("%Y-%m-%d")
                df.loc[df["ID"] == selected_id, "Đánh giá"] = new_rating
                
                # Cập nhật ảnh nếu có
                if new_image is not None:
                    image_filename = save_uploaded_image(new_image, selected_id)
                    df.loc[df["ID"] == selected_id, "Ảnh"] = image_filename
                
                save_data(df)
                st.success("✅ Sản phẩm đã được cập nhật thành công!")
                st.experimental_rerun()

def delete_product_form(df):
    st.subheader("Xóa sản phẩm")
    selected_id = st.selectbox("Chọn sản phẩm cần xóa", df["ID"].values)
    product = df[df["ID"] == selected_id].iloc[0]
    
    st.warning("Bạn đang chuẩn bị xóa sản phẩm sau:")
    col1, col2 = st.columns(2)
    with col1:
        display_image(product["Ảnh"], width=250)
    with col2:
        st.markdown(f"**Tên:** {product['Tên sản phẩm']}")
        st.markdown(f"**Loại:** {product['Loại']}")
        st.markdown(f"**Giá:** {product['Giá']:,.0f} VND")
        st.markdown(f"**Số lượng tồn:** {product['Số lượng']}")
    
    if st.button("Xác nhận xóa", type="primary"):
        # Xóa ảnh nếu tồn tại
        if product["Ảnh"] and os.path.exists(os.path.join(IMAGE_FOLDER, product["Ảnh"])):
            os.remove(os.path.join(IMAGE_FOLDER, product["Ảnh"]))
        
        # Xóa sản phẩm khỏi dataframe
        df = df[df["ID"] != selected_id]
        save_data(df)
        st.success("✅ Sản phẩm đã được xóa thành công!")
        st.experimental_rerun()

def search_products(df):
    st.subheader("Tìm kiếm sản phẩm")
    
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("Nhập từ khóa tìm kiếm", placeholder="Tên sản phẩm, mô tả...")
    with col2:
        search_by = st.selectbox("Tìm theo", ["Tất cả", "Tên sản phẩm", "Loại", "Mô tả"])
    
    price_range = st.slider(
        "Khoảng giá (VND)", 
        min_value=0, 
        max_value=100000000, 
        value=(0, 50000000), 
        step=1000000,
        format="%d"
    )
    
    if search_term:
        if search_by == "Tất cả":
            result = df[
                (df["Tên sản phẩm"].str.contains(search_term, case=False, na=False)) |
                (df["Loại"].str.contains(search_term, case=False, na=False)) |
                (df["Mô tả"].str.contains(search_term, case=False, na=False))
            ]
        elif search_by == "Tên sản phẩm":
            result = df[df["Tên sản phẩm"].str.contains(search_term, case=False, na=False)]
        elif search_by == "Loại":
            result = df[df["Loại"].str.contains(search_term, case=False, na=False)]
        else:
            result = df[df["Mô tả"].str.contains(search_term, case=False, na=False)]
        
        # Lọc theo khoảng giá
        result = result[(result["Giá"] >= price_range[0]) & (result["Giá"] <= price_range[1])]
        
        st.write(f"**Tìm thấy {len(result)} sản phẩm**")
        display_products_grid(result)
    else:
        # Hiển thị tất cả sản phẩm nếu không có từ khóa tìm kiếm
        result = df[(df["Giá"] >= price_range[0]) & (df["Giá"] <= price_range[1])]
        st.write(f"**Tất cả sản phẩm ({len(result)})**")
        display_products_grid(result)

# ============================================
# GIAO DIỆN CHÍNH
# ============================================
def main():
    # Cấu hình trang
    st.set_page_config(
        page_title="TechStore - Quản lý sản phẩm",
        page_icon="🛒",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Khởi tạo dữ liệu
    init_data()
    df = load_data()
    
    # Sidebar
    st.sidebar.title("🛍️ TechStore")
    st.sidebar.markdown("---")
    
    # Giỏ hàng
    if 'cart' in st.session_state and st.session_state['cart']:
        st.sidebar.subheader(f"🛒 Giỏ hàng ({len(st.session_state['cart'])})")
        for product_id in st.session_state['cart']:
            product = df[df["ID"] == product_id].iloc[0]
            st.sidebar.markdown(f"- {product['Tên sản phẩm']} ({product['Giá']:,.0f} VND)")
        
        total = sum(df[df["ID"].isin(st.session_state['cart'])]["Giá"])
        st.sidebar.markdown(f"**Tổng cộng:** {total:,.0f} VND")
        
        if st.sidebar.button("Thanh toán", type="primary"):
            st.sidebar.success("Đơn hàng đã được ghi nhận!")
            st.session_state['cart'] = []
    else:
        st.sidebar.subheader("🛒 Giỏ hàng trống")
        st.sidebar.info("Thêm sản phẩm vào giỏ hàng để thanh toán")
    
    st.sidebar.markdown("---")
    
    # Menu chức năng
    menu_options = [
        "🏠 Trang chủ",
        "🔍 Tìm kiếm sản phẩm",
        "➕ Thêm sản phẩm",
        "✏️ Cập nhật sản phẩm",
        "🗑️ Xóa sản phẩm"
    ]
    menu = st.sidebar.radio("Menu chức năng", menu_options)
    
    # Xử lý xem chi tiết sản phẩm
    if 'view_product' in st.session_state:
        display_product_detail(st.session_state['view_product'], df)
        return
    
    # Trang chủ
    if menu == "🏠 Trang chủ":
        st.title("🛍️ TechStore - Cửa hàng điện tử")
        st.markdown("---")
        
        # Hiển thị sản phẩm nổi bật
        st.subheader("🔥 Sản phẩm nổi bật")
        featured = df.sort_values("Đánh giá", ascending=False).head(6)
        display_products_grid(featured)
        
        # Hiển thị theo danh mục
        st.subheader("📦 Danh mục sản phẩm")
        selected_category = st.selectbox("Chọn danh mục", ["Tất cả"] + CATEGORIES)
        
        if selected_category == "Tất cả":
            display_products_grid(df)
        else:
            category_products = df[df["Loại"] == selected_category]
            if not category_products.empty:
                st.write(f"**{selected_category} ({len(category_products)})**")
                display_products_grid(category_products)
            else:
                st.info(f"Không có sản phẩm nào trong danh mục {selected_category}")
    
    # Tìm kiếm sản phẩm
    elif menu == "🔍 Tìm kiếm sản phẩm":
        search_products(df)
    
    # Thêm sản phẩm
    elif menu == "➕ Thêm sản phẩm":
        add_product_form(df)
    
    # Cập nhật sản phẩm
    elif menu == "✏️ Cập nhật sản phẩm":
        update_product_form(df)
    
    # Xóa sản phẩm
    elif menu == "🗑️ Xóa sản phẩm":
        delete_product_form(df)

if __name__ == "__main__":
    import requests
    main()