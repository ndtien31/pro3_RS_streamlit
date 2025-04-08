import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image
import base64

# Tên file lưu trữ dữ liệu
DATA_FILE = "products.csv"
IMAGE_FOLDER = "product_images"

# Tạo thư mục lưu ảnh nếu chưa tồn tại
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Khởi tạo dữ liệu nếu file chưa tồn tại
def init_data():
    if not os.path.exists(DATA_FILE):
        sample_data = {
            "ID": [1, 2, 3],
            "Tên sản phẩm": ["iPhone 13", "Samsung Galaxy S21", "Xiaomi Redmi Note 10"],
            "Loại": ["Điện thoại", "Điện thoại", "Điện thoại"],
            "Giá": [20000000, 18000000, 5000000],
            "Số lượng": [10, 15, 20],
            "Mô tả": [
                "iPhone 13 với màn hình Super Retina XDR, chip A15 Bionic",
                "Samsung Galaxy S21 với camera ấn tượng và hiệu năng mạnh mẽ",
                "Xiaomi Redmi Note 10 giá rẻ nhưng chất lượng"
            ],
            "Ngày nhập": ["2023-01-15", "2023-02-20", "2023-03-10"],
            "Ảnh": ["", "", ""]
        }
        df = pd.DataFrame(sample_data)
        df.to_csv(DATA_FILE, index=False)

# Đọc dữ liệu từ file
def load_data():
    return pd.read_csv(DATA_FILE)

# Lưu dữ liệu vào file
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Tạo ID mới
def generate_id(df):
    return df["ID"].max() + 1 if not df.empty else 1

# Lưu ảnh và trả về tên file
def save_uploaded_image(uploaded_file, product_id):
    if uploaded_file is not None:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        filename = f"{product_id}{file_ext}"
        filepath = os.path.join(IMAGE_FOLDER, filename)
        
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return filename
    return ""

# Hiển thị ảnh
def display_image(image_path, width=200):
    if image_path and os.path.exists(os.path.join(IMAGE_FOLDER, image_path)):
        img = Image.open(os.path.join(IMAGE_FOLDER, image_path))
        st.image(img, width=width)
    else:
        st.image("https://via.placeholder.com/200?text=No+Image", width=width)

# Hiển thị sản phẩm dạng grid
def display_products_grid(df):
    cols_per_row = 3
    cols = st.columns(cols_per_row)
    
    for idx, row in df.iterrows():
        with cols[idx % cols_per_row]:
            st.markdown(f"**{row['Tên sản phẩm']}**")
            display_image(row['Ảnh'])
            st.markdown(f"**Giá:** {row['Giá']:,.0f} VND")
            st.markdown(f"**Số lượng:** {row['Số lượng']}")
            
            if st.button(f"Xem chi tiết", key=f"view_{row['ID']}"):
                st.session_state['view_product'] = row['ID']
            
            st.markdown("---")

# Hiển thị chi tiết sản phẩm
def display_product_detail(product_id, df):
    product = df[df["ID"] == product_id].iloc[0]
    st.subheader(product["Tên sản phẩm"])
    
    col1, col2 = st.columns(2)
    with col1:
        display_image(product["Ảnh"], width=300)
    with col2:
        st.markdown(f"**Loại:** {product['Loại']}")
        st.markdown(f"**Giá:** {product['Giá']:,.0f} VND")
        st.markdown(f"**Số lượng:** {product['Số lượng']}")
        st.markdown(f"**Ngày nhập:** {product['Ngày nhập']}")
        st.markdown("**Mô tả:**")
        st.write(product["Mô tả"])
    
    if st.button("Quay lại danh sách"):
        st.session_state.pop('view_product', None)
        st.experimental_rerun()

# Giao diện chính
def main():
    st.title("🛍️ Cửa hàng Sản phẩm")
    st.write("Ứng dụng quản lý sản phẩm với giao diện thương mại điện tử")

    # Khởi tạo dữ liệu
    init_data()
    df = load_data()

    # Sidebar cho các chức năng
    st.sidebar.title("Chức năng")
    menu_options = [
        "Trang chủ - Xem sản phẩm",
        "Thêm sản phẩm",
        "Cập nhật sản phẩm",
        "Xóa sản phẩm",
        "Tìm kiếm sản phẩm"
    ]
    menu = st.sidebar.radio("Menu", menu_options)

    # Xử lý xem chi tiết sản phẩm
    if 'view_product' in st.session_state:
        display_product_detail(st.session_state['view_product'], df)
        return

    # Trang chủ - Hiển thị sản phẩm
    if menu == "Trang chủ - Xem sản phẩm":
        st.subheader("Danh sách sản phẩm")
        display_products_grid(df)

    # Thêm sản phẩm mới
    elif menu == "Thêm sản phẩm":
        st.subheader("Thêm sản phẩm mới")
        
        with st.form("add_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Tên sản phẩm*")
                category = st.selectbox("Loại*", ["Điện thoại", "Laptop", "Tablet", "Phụ kiện"])
                price = st.number_input("Giá*", min_value=0)
            with col2:
                quantity = st.number_input("Số lượng*", min_value=0)
                image = st.file_uploader("Ảnh sản phẩm", type=["jpg", "jpeg", "png"])
                date = st.date_input("Ngày nhập*", datetime.now())
            
            description = st.text_area("Mô tả sản phẩm")
            
            submitted = st.form_submit_button("Thêm sản phẩm")
            
            if submitted:
                if not name:
                    st.error("Vui lòng nhập tên sản phẩm")
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
                        "Ảnh": image_filename
                    }
                    df = pd.concat([df, pd.DataFrame([new_product])], ignore_index=True)
                    save_data(df)
                    st.success("Đã thêm sản phẩm thành công!")
                    st.balloons()
                    st.experimental_rerun()

    # Cập nhật sản phẩm
    elif menu == "Cập nhật sản phẩm":
        st.subheader("Cập nhật sản phẩm")
        
        selected_id = st.selectbox("Chọn ID sản phẩm cần cập nhật", df["ID"].values)
        product = df[df["ID"] == selected_id].iloc[0]
        
        with st.form("update_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Tên sản phẩm*", product["Tên sản phẩm"])
                new_category = st.selectbox(
                    "Loại*", 
                    ["Điện thoại", "Laptop", "Tablet", "Phụ kiện"],
                    index=["Điện thoại", "Laptop", "Tablet", "Phụ kiện"].index(product["Loại"]))
                new_price = st.number_input("Giá*", min_value=0, value=product["Giá"])
            with col2:
                new_quantity = st.number_input("Số lượng*", min_value=0, value=product["Số lượng"])
                new_image = st.file_uploader("Cập nhật ảnh", type=["jpg", "jpeg", "png"])
                new_date = st.date_input("Ngày nhập*", datetime.strptime(product["Ngày nhập"], "%Y-%m-%d"))
            
            new_description = st.text_area("Mô tả", product["Mô tả"])
            
            submitted = st.form_submit_button("Cập nhật")
            
            if submitted:
                if not new_name:
                    st.error("Tên sản phẩm không được để trống")
                else:
                    # Cập nhật thông tin
                    df.loc[df["ID"] == selected_id, "Tên sản phẩm"] = new_name
                    df.loc[df["ID"] == selected_id, "Loại"] = new_category
                    df.loc[df["ID"] == selected_id, "Giá"] = new_price
                    df.loc[df["ID"] == selected_id, "Số lượng"] = new_quantity
                    df.loc[df["ID"] == selected_id, "Mô tả"] = new_description
                    df.loc[df["ID"] == selected_id, "Ngày nhập"] = new_date.strftime("%Y-%m-%d")
                    
                    # Cập nhật ảnh nếu có
                    if new_image is not None:
                        # Xóa ảnh cũ nếu tồn tại
                        old_image = df.loc[df["ID"] == selected_id, "Ảnh"].values[0]
                        if old_image and os.path.exists(os.path.join(IMAGE_FOLDER, old_image)):
                            os.remove(os.path.join(IMAGE_FOLDER, old_image))
                        
                        # Lưu ảnh mới
                        image_filename = save_uploaded_image(new_image, selected_id)
                        df.loc[df["ID"] == selected_id, "Ảnh"] = image_filename
                    
                    save_data(df)
                    st.success("Đã cập nhật sản phẩm thành công!")
                    st.experimental_rerun()

    # Xóa sản phẩm
    elif menu == "Xóa sản phẩm":
        st.subheader("Xóa sản phẩm")
        
        selected_id = st.selectbox("Chọn ID sản phẩm cần xóa", df["ID"].values)
        product = df[df["ID"] == selected_id].iloc[0]
        
        st.write("Thông tin sản phẩm sẽ xóa:")
        col1, col2 = st.columns(2)
        with col1:
            display_image(product["Ảnh"])
        with col2:
            st.markdown(f"**Tên:** {product['Tên sản phẩm']}")
            st.markdown(f"**Loại:** {product['Loại']}")
            st.markdown(f"**Giá:** {product['Giá']:,.0f} VND")
        
        if st.button("Xác nhận xóa"):
            # Xóa ảnh nếu tồn tại
            if product["Ảnh"] and os.path.exists(os.path.join(IMAGE_FOLDER, product["Ảnh"])):
                os.remove(os.path.join(IMAGE_FOLDER, product["Ảnh"]))
            
            # Xóa sản phẩm khỏi dataframe
            df = df[df["ID"] != selected_id]
            save_data(df)
            st.success("Đã xóa sản phẩm thành công!")
            st.experimental_rerun()

    # Tìm kiếm sản phẩm
    elif menu == "Tìm kiếm sản phẩm":
        st.subheader("Tìm kiếm sản phẩm")
        
        search_term = st.text_input("Nhập từ khóa tìm kiếm")
        search_by = st.selectbox("Tìm theo", ["Tên sản phẩm", "Loại", "Mô tả"])
        
        if search_term:
            if search_by == "Tên sản phẩm":
                result = df[df["Tên sản phẩm"].str.contains(search_term, case=False)]
            elif search_by == "Loại":
                result = df[df["Loại"].str.contains(search_term, case=False)]
            else:
                result = df[df["Mô tả"].str.contains(search_term, case=False)]
            
            st.write(f"Kết quả tìm kiếm ({len(result)} sản phẩm):")
            display_products_grid(result)
        else:
            st.warning("Vui lòng nhập từ khóa tìm kiếm")

if __name__ == "__main__":
    main()