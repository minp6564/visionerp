import streamlit as st
import pandas as pd
from datetime import datetime
from data.dummy_data import inventory_logs

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
        '현금': 0, '매출채권': 0, '재고자산': 0,
        '선급금': 0, '선급비용': 0, '기타유동자산': 0,
        '건물': 0, '토지': 0, '기계장치': 0
    }
    st.session_state.liabilities = {
        '매입채무': 0, '미지급금': 0, '단기차입금': 0,
        '미지급비용': 0, '선수금': 0, '예수금': 0,
        '장기차입금': 0, '사채': 0, '충당부채': 0, '기타비유동부채': 0
    }
    st.session_state.equity = {
        '자본금': 0, '이익잉여금': 0, '자본잉여금': 0,
        '기타포괄손익누계액': 0, '자기주식': 0
    }

# dummy_data.py의 inventory_logs를 이용해 거래 데이터 불러오기

def load_dummy_data_from_py():
    if 'dummy_loaded' not in st.session_state:
        for _, row in inventory_logs.iterrows():
            if row['구분'] == '입고':
                st.session_state.assets['재고자산'] += row['수량'] * row['입고단가']
            elif row['구분'] == '출고':
                st.session_state.assets['재고자산'] -= row['수량'] * row['출고단가']
        st.session_state.dummy_loaded = True
        st.success("dummy_data.py로부터 데이터를 성공적으로 불러왔습니다.")

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
    st.markdown('<div class="sub-title">입출고 데이터를 불러와 재무상태표를 확인하세요!</div>', unsafe_allow_html=True)

    if st.button("더미 데이터(PY) 불러오기 🐍"):
        load_dummy_data_from_py()

    if st.button("재무상태표 조회 📊"):
        balance_sheet()

    st.markdown('<div class="footer">회계 시스템을 사용해 주셔서 감사합니다! ✨</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
