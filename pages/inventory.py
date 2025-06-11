import streamlit as st
import pandas as pd
from datetime import datetime
from data import dummy_data

st.set_page_config(page_title="재고 입출고", layout="wide")
st.title("📦 재고 입출고 등록")

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "inventory_logs" not in st.session_state:
    st.session_state.inventory_logs = dummy_data.inventory_logs.copy()

# -----------------------------
# 재고/입고 정보 계산 함수
# -----------------------------
def get_available_items():
    df = st.session_state.inventory_logs
    if df.empty:
        return {}

    stock = df.groupby(["품목명", "구분"])["수량"].sum().unstack().fillna(0)
    stock["재고"] = stock.get("입고", 0) - stock.get("출고", 0)
    available = stock[stock["재고"] > 0]["재고"]
    return available.to_dict()

def get_latest_in_info(item_name):
    df = st.session_state.inventory_logs
    if df.empty:
        return 0, "정보 없음"

    df_item = df[(df["품목명"] == item_name) & (df["구분"] == "입고")]
    if df_item.empty:
        return 0, "정보 없음"
    
    latest_row = df_item.sort_values("날짜", ascending=False).iloc[0]
    return latest_row["입고단가"], latest_row["납품업체명"]

available_items = get_available_items()

# -----------------------------
# UI 입력 영역
# -----------------------------
st.subheader("📥 입출고 정보 입력")

col1, col2 = st.columns(2)
with col1:
    inout_type = st.selectbox("구분", ["입고", "출고"])

    # 품목 선택/입력
    if inout_type == "입고":
        item_name = st.text_input("품목명", placeholder="예: 철판 1.2T")
        in_price = st.number_input("입고 단가 (₩)", min_value=0, step=100)
        supplier = st.text_input("납품업체명", placeholder="예: ABC상사")
    else:
        if available_items:
            item_name = st.selectbox("품목명 (재고 있는 항목)", list(available_items.keys()))
            st.info(f"📦 현재 재고: {int(available_items[item_name])}개")
            # 자동 입력 (readonly)
            in_price, supplier = get_latest_in_info(item_name)
            st.text_input("입고 단가 (최근)", value=in_price, disabled=True)
            st.text_input("납품업체명 (최근)", value=supplier, disabled=True)
        else:
            item_name = None
            st.warning("⚠️ 출고 가능한 품목이 없습니다.")
            in_price, supplier = 0, ""

with col2:
    quantity = st.number_input("수량", min_value=1, step=1)
    out_price = st.number_input("출고 단가 (₩)", min_value=0, step=100)

    if inout_type == "입고":
        manager = st.text_input("입고 담당자", placeholder="예: 홍길동")
    else:
        manager = st.text_input("출고 담당자", placeholder="예: 이철수")

    remark = st.text_input("비고")

# -----------------------------
# 실시간 마진율 계산
# -----------------------------
st.divider()
margin_rate = None
if in_price > 0 and out_price > 0:
    margin_rate = round((out_price - in_price) / in_price * 100, 2)
    st.success(f"💹 실시간 마진율: `{margin_rate}%`")
else:
    st.info("마진율을 계산하려면 입고/출고 단가 모두 입력해야 합니다.")

if st.button("✅ 등록"):
    if inout_type == "출고":
        if not item_name:
            st.error("❌ 출고 가능한 품목이 없습니다.")
        elif quantity > available_items.get(item_name, 0):
            st.error("❌ 출고 수량이 재고를 초과합니다.")
        else:
            register = True
    else:
        register = True

    if 'register' in locals() and register:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        # ✅ 분기 처리: 입고 vs 출고
        if inout_type == "입고":
            new_log = {
                "날짜": now,
                "품목명": item_name,
                "구분": inout_type,
                "수량": quantity,
                "입고단가": in_price,
                "예상출고단가": expected_price,  # ✅ 입고 시만 입력
                "출고단가": 0,
                "마진율": "",
                "납품업체명": supplier,
                "담당자명": manager,
                "비고": remark
            }
        else:  # 출고
            new_log = {
                "날짜": now,
                "품목명": item_name,
                "구분": inout_type,
                "수량": quantity,
                "입고단가": in_price,
                "예상출고단가": "",
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
