import streamlit as st
import pandas as pd
import os

st.title("💰 급여 관리")

DATA_PATH = "data/salary.csv"

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame(columns=["사번", "이름", "기본급", "수당", "공제", "지급액"])

st.dataframe(df)

with st.form("add_salary"):
    st.subheader("➕ 급여 등록")
    col1, col2, col3 = st.columns(3)
    with col1:
        emp_id = st.text_input("사번")
        name = st.text_input("이름")
    with col2:
        base = st.number_input("기본급", min_value=0)
        bonus = st.number_input("수당", min_value=0)
    with col3:
        deduct = st.number_input("공제", min_value=0)

    if st.form_submit_button("저장"):
        total = base + bonus - deduct
        new_data = pd.DataFrame([[emp_id, name, base, bonus, deduct, total]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        st.success(f"{name}님의 급여 정보가 저장되었습니다.")
        st.experimental_rerun()
