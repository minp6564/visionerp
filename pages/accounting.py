import streamlit as st
import pandas as pd
from datetime import datetime

# 스타일 설정
st.markdown("""
    <style>
        .title { color: #2F4F4F; font-size: 40px; font-weight: bold; text-align: center; margin-top: 20px; }
        .sub-title { color: #5F6368; font-size: 30px; text-align: center; }
        .section-header { color: #00796B; font-size: 20px; font-weight: bold; margin-top: 20px; }
        .footer { text-align: center; margin-top: 50px; font-size: 14px; color: #00796B; }
        .positive { color: green; }
        .negative { color: red; }
    </style>
""", unsafe_allow_html=True)

# 세션 초기화
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
    st.session_state.assets = {
        '현금': 300000, '매출채권': 150000, '재고자산': 200000,
        '선급금': 50000, '선급비용': 30000, '기타유동자산': 25000,
        '건물': 500000, '토지': 600000, '기계장치': 400000
    }
    st.session_state.liabilities = {
        '매입채무': 100000, '미지급금': 50000, '단기차입금': 80000,
        '미지급비용': 30000, '선수금': 20000, '예수금': 15000,
        '장기차입금': 120000, '사채': 100000, '충당부채': 40000, '기타비유동부채': 30000
    }
    st.session_state.equity = {
        '자본금': 700000, '이익잉여금': 200000, '자본잉여금': 150000,
        '기타포괄손익누계액': 50000, '자기주식': -10000
    }

# 수동 입력 함수
def manual_entry():
    st.markdown('<div class="section-header">항목별 값 수동 입력</div>', unsafe_allow_html=True)

    with st.form("manual_input_form"):
        for category, group in zip(
            ['자산', '부채', '자본'],
            [st.session_state.assets, st.session_state.liabilities, st.session_state.equity]
        ):
            st.subheader(category)
            for name in group:
                group[name] = st.number_input(f"{name}", value=group[name], key=f"{category}_{name}")

        submitted = st.form_submit_button("입력 완료 ✅")
        if submitted:
            st.success("입력한 값이 반영되었습니다!")

# 재무상태표 출력 함수
def balance_sheet():
    st.write("### 재무상태표")
    total_assets = sum(st.session_state.assets.values())
    total_liabilities = sum(st.session_state.liabilities.values())
    total_equity = sum(st.session_state.equity.values())
    net_assets = total_assets - total_liabilities

    st.write(f"### 자산")
    for name, value in st.session_state.assets.items():
        st.write(f"{name}: {value:,.0f} 원")
    st.write(f"**총 자산**: {total_assets:,.0f} 원 💰")

    st.write(f"### 부채")
    for name, value in st.session_state.liabilities.items():
        st.write(f"{name}: {value:,.0f} 원")
    st.write(f"**총 부채**: {total_liabilities:,.0f} 원 💳")

    st.write(f"### 자본")
    for name, value in st.session_state.equity.items():
        st.write(f"{name}: {value:,.0f} 원")
    st.write(f"**총 자본**: {total_equity:,.0f} 원 💵")

    st.write(f"### 순자산")
    st.write(f"**순자산**: {net_assets:,.0f} 원 💸")

# 메인 UI 함수
def main():
    st.markdown('<div class="title">회계 시스템</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">직접 값을 입력하고 재무상태표를 확인하세요!</div>', unsafe_allow_html=True)

    manual_entry()

    if st.button("재무상태표 조회 📊"):
        balance_sheet()

    st.markdown('<div class="footer">회계 시스템을 사용해 주셔서 감사합니다! ✨</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
