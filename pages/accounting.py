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

# 거래 추가 함수
def add_transaction(date, description, amount_in, amount_out, transaction_type, category, memo):
    transaction = {
        "날짜": date, "설명": description, "입금": amount_in, "출금": amount_out,
        "유형": transaction_type, "카테고리": category, "메모": memo
    }
    st.session_state.transactions.append(transaction)

    if category in st.session_state.assets:
        st.session_state.assets[category] += amount_in
    elif category in st.session_state.liabilities:
        st.session_state.liabilities[category] += amount_out
    elif category in st.session_state.equity:
        st.session_state.equity[category] += amount_in

# 거래 유형에 따른 카테고리 매핑
def get_category_options(transaction_type):
    if transaction_type == "자산":
        return list(st.session_state.assets.keys())
    elif transaction_type == "부채":
        return list(st.session_state.liabilities.keys())
    elif transaction_type == "자본":
        return list(st.session_state.equity.keys())
    else:
        return []

# 더미 데이터 불러오기
from data.dummy_data_document import dummy_data

def load_dummy_data():
    if 'dummy_loaded' not in st.session_state:
        for entry in dummy_data:
            add_transaction(
                pd.to_datetime(entry["날짜"]),
                entry["설명"],
                entry["입금"],
                entry["출금"],
                entry["유형"],
                entry["카테고리"],
                entry["메모"]
            )
        st.session_state.dummy_loaded = True
        st.success("더미 데이터를 성공적으로 불러왔습니다.")

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
    st.markdown('<div class="sub-title">재무상태표를 확인하세요!</div>', unsafe_allow_html=True)

    if st.button("거래 더미 데이터 불러오기"):
        load_dummy_data()

    if st.button("재무상태표 조회 📊"):
        balance_sheet()

    st.markdown('<div class="footer">회계 시스템을 사용해 주셔서 감사합니다! ✨</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
