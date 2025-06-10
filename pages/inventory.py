import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="재고 입출고", layout="wide")
st.title("📦 재고 입출고 등록")

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "inventory_logs" not in st.session_state:
    st.session_state.inventory_logs = pd.DataFrame(
        columns=["날짜", "품목명", "구분", "수량", "입고단가", "출고단가", "마진율", "납품업체명", "담당자명", "비고"]
    )

# -----------------------------
# 입출고 등록 폼
# -----------------------------
with st.form("inventory_form"):
    col1, col2 = st.columns(2)
    with col1:
        item_name = st.text_input("품목명", placeholder="예: 철판 1.2T")
        inout_type = st.selectbox("구분", ["입고", "출고"])
        supplier = st.text_input("납품업체명", placeholder="예: ABC상사")
        in_price = st.number_input("입고 단가 (₩)", min_value=0, step=100)
    with col2:
        quantity = st.number_input("수량", min_value=1, step=1)
        manager = st.text_input("담당자명", placeholder="예: 홍길동")
        remark = st.text_input("비고")
        out_price = st.number_input("출고 단가 (₩)", min_value=0, step=100)

    # -----------------------------
    # 💹 실시간 마진율 계산
    # -----------------------------
    margin_rate = None
    if in_price > 0 and out_price > 0:
        margin_rate = round((out_price - in_price) / in_price * 100, 2)

    col_submit, col_margin = st.columns([1, 2])
    with col_submit:
        submitted = st.form_submit_button("✅ 등록")

    with col_margin:
        if margin_rate is not None:
            st.markdown(f"**💹 마진율:** `{margin_rate}%`")
        else:
            st.markdown("💹 마진율: 계산 불가")

    if submitted:
        new_log = {
            "날짜": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "품목명": item_name,
            "구분": inout_type,
            "수량": quantity,
            "입고단가": in_price,
            "출고단가": out_price,
            "마진율": margin_rate if margin_rate is not None else "",
            "납품업체명": supplier,
            "담당자명": manager,
            "비고": remark
        }

        st.session_state.inventory_logs = pd.concat(
            [st.session_state.inventory_logs, pd.DataFrame([new_log])],
            ignore_index=True
        )

        st.success(f"✅ {inout_type} 등록 완료: {item_name} {int(quantity)}개")

# -----------------------------
# 입출고 내역 테이블
# -----------------------------
st.subheader("📋 입출고 내역")

if st.session_state.inventory_logs.empty:
    st.info("입출고 내역이 아직 없습니다.")
else:
    st.dataframe(
        st.session_state.inventory_logs.sort_values(by="날짜", ascending=False),
        use_container_width=True
    )
