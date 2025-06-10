# pages/2_근태관리.py
import streamlit as st
import datetime

st.title("⏱ 근태 관리")

today = datetime.date.today()

st.date_input("날짜 선택", today)
st.text_input("사번")
st.selectbox("출근 상태", ["출근", "지각", "결근", "조퇴", "휴가"])

if st.button("기록 저장"):
    st.success("근태 기록이 저장되었습니다.")
