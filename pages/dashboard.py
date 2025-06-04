
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# -----------------------------
# 📅 오늘 날짜
# -----------------------------
today = datetime.date.today()

# -----------------------------
# 📦 더미 데이터
# -----------------------------
production_today = 4

stock_summary = {
    '원자재': 24,
    '완제품': 8
}

monthly_sales = {
    '건수': 102,
    '매출': 9400000  # ₩
}

pending_io = {
    '입고': 2,
    '출고': 1
}

production_log = pd.DataFrame({
    '날짜': pd.date_range(end=today, periods=7),
    '생산량': [80, 120, 90, 100, 130, 110, 150]
})

# -----------------------------
# 📊 Streamlit 화면 구성
# -----------------------------
st.set_page_config(page_title="ERP 대시보드", layout="wide")

st.title("📊 소규모 제조업 ERP 대시보드")

# KPI 지표들
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👷 오늘의 생산계획", f"{production_today} 건")

with col2:
    st.metric("📦 원자재", f"{stock_summary['원자재']} 종")
    st.metric("📦 완제품", f"{stock_summary['완제품']} 종")

with col3:
    st.metric("💰 판매 건수", f"{monthly_sales['건수']} 건")
    st.metric("💵 월 매출", f"₩{monthly_sales['매출']:,}")

with col4:
    st.metric("⏳ 입고 대기", f"{pending_io['입고']} 건")
    st.metric("📤 출고 대기", f"{pending_io['출고']} 건")

st.divider()

# 생산량 추이 그래프
st.subheader("📈 최근 7일 생산량 추이")
fig = px.bar(production_log, x='날짜', y='생산량', title='최근 생산량', labels={'생산량': '단위: 개'})
st.plotly_chart(fig, use_container_width=True)

# 하단 TODO
st.info("💡 추후 기능 추가: 최근 주문 목록, 재고 부족 알림, 생산계획 바로가기 등")
