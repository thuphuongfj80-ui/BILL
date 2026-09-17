import streamlit as st
import pandas as pd
from datetime import datetime

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Nhà hàng Cỏ Bốn Lá",
    page_icon="🍀",
    layout="wide"
)

# =========================================================
# LOGO NHÀ HÀNG
# =========================================================

col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])

with col_logo2:
    st.image(
        "Logo1.JPG",
        use_container_width=True
    )

# =========================================================
# TÊN NHÀ HÀNG
# =========================================================

st.title("🍀 NHÀ HÀNG CỎ BỐN LÁ")
st.caption("Hệ thống Order - Thanh toán - Quản lý doanh thu")

st.divider()

# =========================================================
# KHỞI TẠO DỮ LIỆU
# =========================================================

if "orders" not in st.session_state:
    st.session_state.orders = {}

if "bills" not in st.session_state:
    st.session_state.bills = []

# =========================================================
# DANH SÁCH BÀN
# =========================================================

danh_sach_ban = [
    f"Bàn {i}" for i in range(1, 21)
]

# =========================================================
# MENU NHÀ HÀNG
# =========================================================

menu = {

    "🍜 Món ăn": {

        "Pizza Hải Sản": 120000,
        "Mì Ý Bò Bằm": 50000,
        "Burger Gà": 65000,
        "Salad Trộn": 50000,
        "Bít Tết Bò Mỹ": 250000,
        "Sườn Nướng BBQ": 180000,
        "Cánh Gà Chiên Mắm": 75000,
        "Lẩu Cá Diêu Hồng": 200000,
        "Lẩu Thái Hải Sản": 300000,
        "Lẩu Cá Kèo": 140000

    },

    "🥤 Thức uống": {

        "Coca Cola": 20000,
        "Pepsi": 20000,
        "Trà Đào Cam Sả": 35000,
        "Cà Phê Sữa": 25000,
        "Nước Suối": 10000,
        "Sinh Tố Bơ": 45000,
        "Nước Ép Cam": 40000,
        "Mojito Chanh Dây": 55000

    },

    "🍰 Tráng miệng": {

        "Bánh Flan": 25000,
        "Kem Vani": 30000,
        "Chè Khúc Bạch": 35000,
        "Trái Cây": 40000

    }
}

# =========================================================
# HÀM TÍNH TIỀN
# =========================================================

def tinh_tien(ban):

    if ban not in st.session_state.orders:
        return 0, 0, 0

    tam_tinh = 0

    for mon in st.session_state.orders[ban].values():

        tam_tinh += (
            mon["Đơn giá"] *
            mon["Số lượng"]
        )

    # Giảm 5% nếu hóa đơn từ 1.000.000 VNĐ
    if tam_tinh >= 1000000:
        giam_gia = tam_tinh * 0.05
    else:
        giam_gia = 0

    tong_tien = tam_tinh - giam_gia

    return tam_tinh, giam_gia, tong_tien


# =========================================================
# MENU BÊN TRÁI
# =========================================================

trang = st.sidebar.radio(
    "📋 CHỨC NĂNG",
    [
        "🍽️ Order",
        "🧾 Hóa đơn",
        "📊 Doanh thu"
    ]
)

st.sidebar.divider()

st.sidebar.write("🍀 **NHÀ HÀNG CỎ BỐN LÁ**")
st.sidebar.caption(
    "Chúc quý khách ngon miệng!"
)

# =========================================================
# TRANG ORDER
# =========================================================

if trang == "🍽️ Order":

    st.header("🍽️ GỌI MÓN")

    # Chọn bàn
    ban = st.selectbox(
        "🪑 Chọn bàn",
        danh_sach_ban
    )

    st.divider()

    col1, col2 = st.columns([1, 1.5])

    # -----------------------------------------------------
    # CHỌN MÓN
    # -----------------------------------------------------

    with col1:

        st.subheader("🍴 Chọn món")

        nhom_mon = st.selectbox(
            "Loại món",
            list(menu.keys())
        )

        ten_mon = st.selectbox(
            "Tên món",
            list(menu[nhom_mon].keys())
        )

        gia_mon = menu[nhom_mon][ten_mon]

        st.info(
            f"💰 Giá: **{gia_mon:,.0f} VNĐ**"
        )

        so_luong = st.number_input(
            "Số lượng",
            min_value=1,
            max_value=100,
            value=1,
            step=1
        )

        if st.button(
            "➕ THÊM MÓN",
            use_container_width=True
        ):

            if ban not in st.session_state.orders:
                st.session_state.orders[ban] = {}

            if ten_mon in st.session_state.orders[ban]:

                st.session_state.orders[ban][ten_mon][
                    "Số lượng"
                ] += so_luong

            else:

                st.session_state.orders[ban][ten_mon] = {

                    "Tên món": ten_mon,

                    "Đơn giá": gia_mon,

                    "Số lượng": so_luong

                }

            st.success(
                f"✅ Đã thêm {so_luong} x {ten_mon}"
            )

            st.rerun()

    # -----------------------------------------------------
    # GIỎ HÀNG
    # -----------------------------------------------------

    with col2:

        st.subheader(
            f"🛒 Đơn hàng - {ban}"
        )

        if (
            ban in st.session_state.orders
            and st.session_state.orders[ban]
        ):

            danh_sach_mon = []

            for mon in st.session_state.orders[ban].values():

                thanh_tien = (
                    mon["Đơn giá"] *
                    mon["Số lượng"]
                )

                danh_sach_mon.append({

                    "Tên món": mon["Tên món"],

                    "Đơn giá": mon["Đơn giá"],

                    "SL": mon["Số lượng"],

                    "Thành tiền": thanh_tien

                })

            df = pd.DataFrame(danh_sach_mon)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            tam_tinh, giam_gia, tong_tien = tinh_tien(ban)

            st.divider()

            st.write(
                f"**Tạm tính:** {tam_tinh:,.0f} VNĐ"
            )

            st.write(
                f"**Giảm giá:** {giam_gia:,.0f} VNĐ"
            )

            st.success(
                f"## 💰 Thanh toán: {tong_tien:,.0f} VNĐ"
            )

            col_a, col_b = st.columns(2)

            # -------------------------------------------------
            # THANH TOÁN
            # -------------------------------------------------

            with col_a:

                if st.button(
                    "💰 THANH TOÁN",
                    use_container_width=True
                ):

                    hoa_don = {

                        "Bàn": ban,

                        "Thời gian":
                            datetime.now().strftime(
                                "%d/%m/%Y %H:%M:%S"
                            ),

                        "Chi tiết":
                            danh_sach_mon,

                        "Tạm tính":
                            tam_tinh,

                        "Giảm giá":
                            giam_gia,

                        "Tổng tiền":
                            tong_tien
                    }

                    st.session_state.bills.append(
                        hoa_don
                    )

                    del st.session_state.orders[ban]

                    st.success(
                        "✅ Thanh toán thành công!"
                    )

                    st.rerun()

            # -------------------------------------------------
            # XÓA ĐƠN
            # -------------------------------------------------

            with col_b:

                if st.button(
                    "🗑️ XÓA ĐƠN",
                    use_container_width=True
                ):

                    del st.session_state.orders[ban]

                    st.warning(
                        "Đã xóa đơn của bàn."
                    )

                    st.rerun()

        else:

            st.info(
                "🛒 Bàn này chưa có món."
            )


# =========================================================
# TRANG HÓA ĐƠN
# =========================================================

elif trang == "🧾 Hóa đơn":

    st.header("🧾 QUẢN LÝ HÓA ĐƠN")

    if not st.session_state.bills:

        st.info(
            "Chưa có hóa đơn."
        )

    else:

        hoa_don_df = pd.DataFrame([

            {
                "STT": i + 1,
                "Bàn": bill["Bàn"],
                "Thời gian": bill["Thời gian"],
                "Tạm tính": bill["Tạm tính"],
                "Giảm giá": bill["Giảm giá"],
                "Tổng tiền": bill["Tổng tiền"]
            }

            for i, bill in enumerate(
                st.session_state.bills
            )

        ])

        st.dataframe(
            hoa_don_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader(
            "🔎 Chi tiết hóa đơn"
        )

        for i, bill in enumerate(
            st.session_state.bills
        ):

            with st.expander(
                f"🧾 Hóa đơn #{i + 1} - "
                f"{bill['Bàn']} - "
                f"{bill['Thời gian']}"
            ):

                detail_df = pd.DataFrame(
                    bill["Chi tiết"]
                )

                st.dataframe(
                    detail_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.write(
                    f"**Tạm tính:** "
                    f"{bill['Tạm tính']:,.0f} VNĐ"
                )

                st.write(
                    f"**Giảm giá:** "
                    f"{bill['Giảm giá']:,.0f} VNĐ"
                )

                st.success(
                    f"### Tổng thanh toán: "
                    f"{bill['Tổng tiền']:,.0f} VNĐ"
                )


# =========================================================
# TRANG DOANH THU
# =========================================================

else:

    st.header("📊 DOANH THU NHÀ HÀNG")

    if not st.session_state.bills:

        st.info(
            "Chưa có dữ liệu doanh thu."
        )

    else:

        tong_doanh_thu = sum(
            bill["Tổng tiền"]
            for bill in st.session_state.bills
        )

        so_hoa_don = len(
            st.session_state.bills
        )

        tong_giam_gia = sum(
            bill["Giảm giá"]
            for bill in st.session_state.bills
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "💰 Tổng doanh thu",
                f"{tong_doanh_thu:,.0f} VNĐ"
            )

        with col2:

            st.metric(
                "🧾 Số hóa đơn",
                so_hoa_don
            )

        with col3:

            st.metric(
                "🎁 Tổng giảm giá",
                f"{tong_giam_gia:,.0f} VNĐ"
            )

        st.divider()

        st.subheader(
            "📋 Danh sách doanh thu"
        )

        doanh_thu_df = pd.DataFrame([

            {
                "Bàn": bill["Bàn"],
                "Thời gian": bill["Thời gian"],
                "Tổng tiền": bill["Tổng tiền"]
            }

            for bill in st.session_state.bills

        ])

        st.dataframe(
            doanh_thu_df,
            use_container_width=True,
            hide_index=True
        )
