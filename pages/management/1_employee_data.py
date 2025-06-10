import streamlit as st
import pandas as pd
import os

DATA_PATH = "data/employees.csv"

st.title("👨‍💼 직원 정보 관리")

# 데이터 로딩
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame(columns=["사번", "이름", "부서", "직위", "입사일", "연락처"])

st.dataframe(df)

# 신규 등록
with st.form("add_employee"):
    st.subheader("➕ 신규 직원 등록")
    col1, col2 = st.columns(2)
    with col1:
        emp_id = st.text_input("사번")
        name = st.text_input("이름")
        dept = st.text_input("부서")
    with col2:
        title = st.text_input("직위")
        hire_date = st.date_input("입사일")
        contact = st.text_input("연락처")
    
    submitted = st.form_submit_button("등록")
    if submitted:
        new_data = pd.DataFrame([[emp_id, name, dept, title, hire_date, contact]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        st.success("직원이 등록되었습니다.")
        st.experimental_rerun()
