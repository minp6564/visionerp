import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from data.dummy_data import inventory_logs

# 📅 날짜
today = datetime.date.today()

# -----------------------------
# 헤더 및 소개
# -----------------------------
st.set_page_config(page_title="🏭 ERP 홈 대시보드", layout="wide")
st.title("visionerp")
st.markdown("""
이 시스템은 소규모 제조기업을 위한 **경량 ERP 솔루션**입니다.

---

### 오늘의 주요 지표 요약
""")


# -----------------------------
# GPT API Key 입력 영역
# -----------------------------
st.divider()
st.subheader("🧠 GPT API 연결")

# ✅ API 키 유지
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

st.session_state.api_key = st.text_input(
    "🔑 OpenAI API Key",
    type="password",
    value=st.session_state.api_key,
    placeholder="sk-로 시작하는 키 입력"
)

if st.session_state.api_key:
    st.success("✅ API 키가 세션에 저장되었습니다.")
else:
    st.info("⚠️ GPT 기능을 사용하려면 API 키를 입력해야 합니다.")

# -----------------------------
# 더미 데이터
# -----------------------------
production_today = 4
stock_summary = {'원자재': 24, '완제품': 8}
monthly_sales = {'건수': 102, '매출': 9400000}
pending_io = {'입고': 2, '출고': 1}

production_log = pd.DataFrame({
    '날짜': pd.date_range(end=today, periods=7),
    '생산량': [80, 120, 90, 100, 130, 110, 150]
})

# -----------------------------
# KPI 지표
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👷 오늘의 생산계획", f"{production_today} 건")

with col2:
    st.metric("📦 원자재", f"{stock_summary['원자재']} 종")
    st.metric("📦 완제품", f"{stock_summary['완제품']} 종")

with col3:
    st.metric("💰 판매건수", f"{monthly_sales['건수']} 건")
    st.metric("💵 월 매출", f"₩{monthly_sales['매출']:,}")

with col4:
    st.metric("⏳ 입고 대기", f"{pending_io['입고']} 건")
    st.metric("📤 출고 대기", f"{pending_io['출고']} 건")

st.divider()

# -----------------------------
# 생산량 → 수익 추이로 대체
# -----------------------------
df = inventory_logs.copy()
df["날짜"] = pd.to_datetime(df["날짜"])
df["월"] = df["날짜"].dt.to_period("M").astype(str)

# 🔧 숫자형 변환 (빈칸 → 0)
df["입고단가"] = pd.to_numeric(df["입고단가"], errors="coerce").fillna(0)
df["출고단가"] = pd.to_numeric(df["출고단가"], errors="coerce").fillna(0)
df["수량"] = pd.to_numeric(df["수량"], errors="coerce").fillna(0)

# ✅ 수익 계산
df["수익"] = df.apply(
    lambda r: (r["출고단가"] - r["입고단가"]) * r["수량"] if r["구분"] == "출고" else 0,
    axis=1
)

monthly_profit = df.groupby("월")["수익"].sum().reset_index()

# 📈 시각화
fig_profit = px.bar(
    monthly_profit,
    x="월", y="수익",
    title="📈 월별 수익 추이",
    labels={"수익": "수익 (원)"},
    text="수익"
)
fig_profit.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_profit.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

st.subheader("📈 월별 수익 추이")
st.plotly_chart(fig_profit, use_container_width=True)


# -----------------------------
# 안내 및 TODO
# -----------------------------
st.info("📌 좌측 메뉴에서 다른 기능으로 이동하세요.")
