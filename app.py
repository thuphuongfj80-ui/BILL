import streamlit as st
st.image("logo1.jpg")
import pandas as pd
from datetime import datetime
st.set_page_config(page_title="Order Nhà Hàng", layout="wide")
 
st.title("🍽️ Hệ thống Order Nhà Hàng - VŨ ĐỨC BÌNH")
 
# ==========================
# Khởi tạo dữ liệu
# ==========================
if "order_dict" not in st.session_state:
   st.session_state.order_dict = {}
 
if "bills" not in st.session_state:
   st.session_state.bills = []
 
# ==========================
# Menu
# ==========================
menu = {
   "Đồ ăn": {
       "Pizza Hải Sản": 120000,
       "Mì Ý Bò Bằm": 50000,
       "Burger Gà": 65000,
       "Salad Trộn": 50000,
       "Bít tết Bò Mỹ": 250000,
       "Sườn nướng BBQ": 180000,
       "Cánh gà chiên mắm": 75000,
       "Lẩu cá diêu hồng": 200000,
       "Lẩu Thái hải sản": 300000,
       "Lẩu cá kèo": 140000
   },
   "Thức uống": {
       "Coca Cola": 20000,
       "Pepsi": 20000,
       "Trà Đào Cam Sả": 35000,
       "Cà Phê Sữa": 25000,
       "Nước Suối": 10000,
       "Sinh tố Bơ": 45000,
       "Nước ép cam": 40000,
       "Mojito chanh dây": 55000,
       "Bia Heineken": 30000
   }
}
 
# ==========================
# Menu bên trái
# ==========================
page = st.sidebar.radio("Chức năng", ["🍽️ Order", "📋 Admin"])
 
# ==========================================================
# TRANG ORDER
# ==========================================================
if page == "🍽️ Order":
 
   table_number = st.number_input(
       "Số bàn",
       min_value=1,
       step=1,
       value=1
   )
 
   col1, col2 = st.columns([1, 1.5])
 
   with col1:
 
       st.subheader("Chọn món")
 
       category = st.selectbox(
           "Loại món",
           list(menu.keys())
       )
 
       item = st.selectbox(
           "Tên món",
           list(menu[category].keys())
       )
 
       quantity = st.number_input(
           "Số lượng",
           min_value=1,
           value=1
       )
 
       if st.button("➕ Thêm món"):
 
           price = menu[category][item]
 
           if item in st.session_state.order_dict:
 
               st.session_state.order_dict[item]["Số lượng"] += quantity
 
               st.session_state.order_dict[item]["Thành tiền"] = (
                   st.session_state.order_dict[item]["Số lượng"] * price
               )
 
           else:
 
               st.session_state.order_dict[item] = {
                   "Tên món": item,
                   "Đơn giá": price,
                   "Số lượng": quantity,
                   "Thành tiền": price * quantity
               }
 
           st.success("Đã thêm món.")
 
   with col2:
 
       st.subheader(f"Giỏ hàng - Bàn {table_number}")
 
       if st.session_state.order_dict:
 
           df = pd.DataFrame.from_dict(
               st.session_state.order_dict,
orient="index"
           )
 
           st.table(df)
 
           tam_tinh = df["Thành tiền"].sum()
 
           giam = tam_tinh * 0.05 if tam_tinh > 1000000 else 0
 
           tong = tam_tinh - giam
 
           st.write(f"### Tạm tính: {tam_tinh:,.0f} VNĐ")
 
           st.write(f"### Giảm giá: {giam:,.0f} VNĐ")
 
           st.success(f"### Tổng thanh toán: {tong:,.0f} VNĐ")
 
           colA, colB = st.columns(2)
 
           with colA:
 
               if st.button("💰 Thanh toán"):
 
                   st.session_state.bills.append({
 
                       "Bàn": table_number,
 
                       "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
 
                       "Chi tiết": df.to_dict("records"),
 
                       "Tổng tiền": tong
                   })
 
                   st.success("Đã thanh toán.")
 
                   st.session_state.order_dict = {}
 
                   st.rerun()
 
           with colB:
 
               if st.button("🗑️ Xóa giỏ"):
 
                   st.session_state.order_dict = {}
 
                   st.rerun()
 
       else:
 
           st.info("Chưa có món.")
 
# ==========================================================
# TRANG ADMIN
# ==========================================================
else:
 
   st.header("📋 Quản lý hóa đơn")
 
   if len(st.session_state.bills) == 0:
 
       st.info("Chưa có hóa đơn.")
 
   else:
 
       bill_df = pd.DataFrame([
           {
               "Bàn": b["Bàn"],
               "Thời gian": b["Thời gian"],
               "Tổng tiền": b["Tổng tiền"]
           }
           for b in st.session_state.bills
       ])
 
       st.dataframe(
           bill_df,
           use_container_width=True
       )
 
       st.metric(
           "Tổng doanh thu",
           f"{bill_df['Tổng tiền'].sum():,.0f} VNĐ"
       )
 
       st.divider()
 
       st.subheader("Chi tiết hóa đơn")
 
       for i, bill in enumerate(st.session_state.bills):
 
           with st.expander(
               f"Bàn {bill['Bàn']} - {bill['Thời gian']}"
           ):
 
               detail = pd.DataFrame(bill["Chi tiết"])
 
               st.table(detail)
 
               st.write(
                   f"### Tổng tiền: {bill['Tổng tiền']:,.0f} VNĐ"
               )
