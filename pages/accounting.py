import streamlit as st
import pandas as pd
from datetime import datetime

# 데이터 저장을 위한 변수 설정 (SQLite 대신 메모리 사용)
if 'transactions' not in st.session_state:
    st.session_state.transactions = []  # 거래 내역을 저장
    st.session_state.accounts = {}  # 각 항목의 잔액을 저장

# 거래 추가 함수 (입금, 출금으로 단순화)
def add_transaction(date, account, description, amount_in, amount_out, transaction_type):
    """
    거래 추가
    - transaction_type: '수익' 또는 '비용'으로 거래의 유형을 구분
    """
    transaction = {
        "날짜": date,
        "항목": account,
        "설명": description,
        "입금": amount_in,
        "출금": amount_out,
        "유형": transaction_type  # '수익' 또는 '비용'
    }
    st.session_state.transactions.append(transaction)

    # 항목 잔액 업데이트
    if account not in st.session_state.accounts:
        st.session_state.accounts[account] = 0
    st.session_state.accounts[account] += amount_in - amount_out

# 계좌 현황 (Balance Sheet) 조회 함수
def balance_sheet():
    balance_data = pd.DataFrame(
        [(account, balance) for account, balance in st.session_state.accounts.items()],
        columns=["항목", "잔액"]
    )
    st.write("### 계좌 현황")
    st.dataframe(balance_data)

# 수익과 비용 (Income Statement) 조회 함수
def income_statement():
    total_income = sum(entry['입금'] for entry in st.session_state.transactions if entry['유형'] == '수익')
    total_expense = sum(entry['출금'] for entry in st.session_state.transactions if entry['유형'] == '비용')
    net_income = total_income - total_expense
    st.write("### 수익과 비용
