import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Tên file lưu trữ dữ liệu
DATA_FILE = "products.csv"

# Khởi tạo dữ liệu nếu file chưa tồn tại
def init_data():
    if not os.path.exists(DATA_FILE):
        sample_data = {
            "ID": [1, 2, 3],
            "Tên sản phẩm": ["iPhone 13", "Samsung Galaxy S21", "Xiaomi Redmi Note 10"],
            "Loại": ["Điện thoại", "Điện thoại", "Điện thoại"],
            "Giá": [20000000, 18000000, 5000000],
            "Số lượng": [10, 15, 20],
            "Ngày nhập": ["2023-01-15", "2023-02-20", "2023-03-10"]
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

# Giao diện chính
def main():
    st.title("📦 Quản lý Sản phẩm")
    st.write("Ứng dụng CRUDS (Create, Read, Update, Delete, Search) cho sản phẩm")

    # Khởi tạo dữ liệu
    init_data()
    df = load_data()

    # Sidebar cho các chức năng
    st.sidebar.title("Chức năng")
    menu = st.sidebar.radio(
        "Menu",
        ["Xem tất cả sản phẩm", "Thêm sản phẩm", "Cập nhật sản phẩm", "Xóa sản phẩm", "Tìm kiếm"]
    )

    # Xem tất cả sản phẩm
    if menu == "Xem tất cả sản phẩm":
        st.subheader("Danh sách sản phẩm")
        st.dataframe(df, use_container_width=True)

    # Thêm sản phẩm mới
    elif menu == "Thêm sản phẩm":
        st.subheader("Thêm sản phẩm mới")
        
        with st.form("add_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Tên sản phẩm")
                category = st.selectbox("Loại", ["Điện thoại", "Laptop", "Tablet", "Phụ kiện"])
            with col2:
                price = st.number_input("Giá", min_value=0)
                quantity = st.number_input("Số lượng", min_value=0)
            
            submitted = st.form_submit_button("Thêm")
            
            if submitted:
                if not name:
                    st.error("Tên sản phẩm không được để trống")
                else:
                    new_product = {
                        "ID": generate_id(df),
                        "Tên sản phẩm": name,
                        "Loại": category,
                        "Giá": price,
                        "Số lượng": quantity,
                        "Ngày nhập": datetime.now().strftime("%Y-%m-%d")
                    }
                    df = pd.concat([df, pd.DataFrame([new_product])], ignore_index=True)
                    save_data(df)
                    st.success("Đã thêm sản phẩm thành công!")
                    st.experimental_rerun()

    # Cập nhật sản phẩm
    elif menu == "Cập nhật sản phẩm":
        st.subheader("Cập nhật sản phẩm")
        
        selected_id = st.selectbox("Chọn ID sản phẩm cần cập nhật", df["ID"].values)
        product = df[df["ID"] == selected_id].iloc[0]
        
        with st.form("update_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Tên sản phẩm", product["Tên sản phẩm"])
                new_category = st.selectbox(
                    "Loại", 
                    ["Điện thoại", "Laptop", "Tablet", "Phụ kiện"],
                    index=["Điện thoại", "Laptop", "Tablet", "Phụ kiện"].index(product["Loại"]))
            with col2:
                new_price = st.number_input("Giá", min_value=0, value=product["Giá"])
                new_quantity = st.number_input("Số lượng", min_value=0, value=product["Số lượng"])
            
            submitted = st.form_submit_button("Cập nhật")
            
            if submitted:
                if not new_name:
                    st.error("Tên sản phẩm không được để trống")
                else:
                    df.loc[df["ID"] == selected_id, "Tên sản phẩm"] = new_name
                    df.loc[df["ID"] == selected_id, "Loại"] = new_category
                    df.loc[df["ID"] == selected_id, "Giá"] = new_price
                    df.loc[df["ID"] == selected_id, "Số lượng"] = new_quantity
                    save_data(df)
                    st.success("Đã cập nhật sản phẩm thành công!")
                    st.experimental_rerun()

    # Xóa sản phẩm
    elif menu == "Xóa sản phẩm":
        st.subheader("Xóa sản phẩm")
        
        selected_id = st.selectbox("Chọn ID sản phẩm cần xóa", df["ID"].values)
        product = df[df["ID"] == selected_id].iloc[0]
        
        st.write("Thông tin sản phẩm sẽ xóa:")
        st.write(product)
        
        if st.button("Xóa"):
            df = df[df["ID"] != selected_id]
            save_data(df)
            st.success("Đã xóa sản phẩm thành công!")
            st.experimental_rerun()

    # Tìm kiếm sản phẩm
    elif menu == "Tìm kiếm":
        st.subheader("Tìm kiếm sản phẩm")
        
        search_term = st.text_input("Nhập từ khóa tìm kiếm")
        search_by = st.selectbox("Tìm theo", ["Tên sản phẩm", "Loại"])
        
        if search_term:
            if search_by == "Tên sản phẩm":
                result = df[df["Tên sản phẩm"].str.contains(search_term, case=False)]
            else:
                result = df[df["Loại"].str.contains(search_term, case=False)]
            
            st.write(f"Kết quả tìm kiếm ({len(result)} sản phẩm):")
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("Vui lòng nhập từ khóa tìm kiếm")

if __name__ == "__main__":
    main()    