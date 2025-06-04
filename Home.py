
import streamlit as st
import pandas as pd

st.set_page_config(page_title="제품 등록", layout="centered")
st.title("📝 제품 등록")

# -----------------------------
# 제품 등록 입력 폼
# -----------------------------
with st.form("product_form"):
    st.subheader("📦 제품 기본 정보")

    product_code = st.text_input("제품 코드", placeholder="예: P-001")
    product_name = st.text_input("제품명", placeholder="예: 기어모터")
    unit = st.selectbox("단위", ["EA", "BOX", "SET", "KG"])
    price = st.number_input("단가 (₩)", min_value=0, step=100)

    st.subheader("🧾 BOM 구성 (예정 기능)")
    st.text("※ 향후 원자재 구성 추가 기능 연결 예정입니다.")

    submitted = st.form_submit_button("✅ 저장")

    if submitted:
        if product_code and product_name:
            st.success(f"✅ '{product_name}' 제품이 저장되었습니다!")
            st.json({
                "제품코드": product_code,
                "제품명": product_name,
                "단위": unit,
                "단가": f"₩{int(price):,}"
            })
        else:
            st.error("❌ 제품 코드와 제품명을 모두 입력해야 합니다.")

