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
이 시스템은 소규모 유통기업을 위한 ERP입니다.

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
# KPI 지표 계산 (수정 반영)
# -----------------------------
df = inventory_logs.copy()
df["날짜"] = pd.to_datetime(df["날짜"])
df["월"] = df["날짜"].dt.to_period("M").astype(str)

# 숫자형 변환
df["입고단가"] = pd.to_numeric(df["입고단가"], errors="coerce").fillna(0)
df["출고단가"] = pd.to_numeric(df["출고단가"], errors="coerce").fillna(0)
df["수량"] = pd.to_numeric(df["수량"], errors="coerce").fillna(0)

# 오늘/이번달 필터
today = datetime.date.today()
df_today = df[df["날짜"].dt.date == today]
current_month = today.strftime("%Y-%m")
df_month = df[df["월"] == current_month]

# KPI 계산
raw_materials = df["납품업체명"].nunique()
finished_goods = df["품목명"].nunique()
monthly_sales_count = df_month[df_month["구분"] == "출고"].shape[0]
monthly_sales_amount = (
    df_month[df_month["구분"] == "출고"]
    .eval("출고단가 * 수량")
    .sum()
)

# 대기 항목은 임시 값 유지
pending_io = {"입고": 2, "출고": 1}

# -----------------------------
# KPI 지표 표시 (3열 구성)
# -----------------------------
col2, col3, col4 = st.columns(3)

with col2:
    st.metric("📦 거래처", f"{raw_materials} 곳")
    st.metric("📦 상품 종류", f"{finished_goods} 종")

with col3:
    st.metric("💰 판매건수", f"{monthly_sales_count} 건")
    st.metric("💵 월 매출", f"₩{int(monthly_sales_amount):,}")

with col4:
    st.metric("⏳ 입고 대기", f"{pending_io['입고']} 건")
    st.metric("📤 출고 대기", f"{pending_io['출고']} 건")

st.divider()


# -----------------------------
# 수익 추이
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
